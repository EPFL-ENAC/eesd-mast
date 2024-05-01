from app.services.runresults.models import RunResult, RunResultUpdate, RunResultVulnerability, RunResultFragility
from app.services.experiments.models import Experiment
from app.utils.query import QueryBuilder
from sqlmodel import select, join, not_
from sqlalchemy.sql import text
from fastapi import HTTPException
from app.db import AsyncSession
from scipy.stats import lognorm
import statsmodels.api as sm
import numpy as np


class RunResultsService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def count(self) -> int:
        """Count all run results"""
        count = (await self.session.exec(text("select count(id) from runresult"))).scalar()
        return count

    async def vulnerability(self, filter: dict | str) -> list[RunResultVulnerability]:
        """Get vulnerabilities from all run results"""
        query = select(RunResult.nominal_pga_x, RunResult.nominal_pga_y, RunResult.dg_derived, RunResult.dg_reported) \
            .select_from(join(RunResult, Experiment)) \
            .where(RunResult.nominal_pga_x.isnot(None) | RunResult.nominal_pga_y.isnot(None)) \
            .where(RunResult.dg_derived.isnot(None) | RunResult.dg_reported.isnot(None)) \
            .where(not_(RunResult.run_id.in_(['Initial', 'Final'])))

        builder = QueryBuilder(Experiment, filter, [], [])
        query = builder.build_filter_query(query)

        # Execute query
        results = await self.session.exec(query)
        data = {}
        for result in results.all():
            dg = result.dg_derived if result.dg_derived else result.dg_reported
            pga = result.nominal_pga_x if result.nominal_pga_x else result.nominal_pga_y
            if dg not in data:
                data[dg] = []
            else:
                data[dg].append(pga)

        vulnerabilities = []
        for dg, pgas in data.items():
            vulnerabilities.append(RunResultVulnerability(dg=dg, pgas=pgas))

        return vulnerabilities

    def fragility(self, vulnerabilities: list[RunResultVulnerability]) -> list[RunResultFragility]:
        """Compute fragility curves from vulnerabilities

        Args:
            vulnerabilities (_type_): PGA vs. DG values
        """

        # number of damage grades considered (5 according to EMS-98 (Grünthal et al., 1998))
        num_grades = 5

        # Define IM levels of interest
        PGA_thresh = np.arange(0.025, 1.275, 0.025)

        fragilities = []
        for i in range(1, num_grades + 1):
            # Compute the probability of exceedance for each damage grade
            p_exceed = []
            grade_pgas = list(
                map(lambda vul: vul.pgas, [v for v in vulnerabilities if v.dg == i]))
            if len(grade_pgas):
                for pga in PGA_thresh:
                    p_exceed.append(np.sum(grade_pgas <= pga) /
                                    np.sum(~np.isnan(grade_pgas)))

                # Fit a lognormal CDF to the data
                b, theta, beta = self.probit(PGA_thresh, p_exceed)

                x = np.linspace(0.0001, 1.25, 1000)
                data = lognorm.cdf(x, beta, scale=theta)

                # Store the results
                fragilities.append(RunResultFragility(
                    dg=i, thresh=PGA_thresh.tolist(), prob=p_exceed, x=x.tolist(), y=data.tolist()))

        return fragilities

    def probit(self, IM, p_exceed):
        """
        Fits a lognormal CDF to observed probability of collapse data using Probit regression.

        Inputs:
        num_gms: int or numpy array, number of ground motions used at each IM level
        num_collapse: numpy array, number of collapses observed at each IM level

        Outputs:
        theta: float, median of fragility function
        beta: float, lognormal standard deviation of fragility function
        """

        # Reshape vectors into column vectors
        IM = IM.reshape((-1, 1))
        p_exceed = np.array(p_exceed)
        p_exceed = p_exceed.reshape((-1, 1))

        # Probit regression
        X = np.log(IM)
        X = sm.add_constant(X)
        Y = p_exceed

        # , max_iter=100) #, cov_type='HC3')
        model = sm.GLM(Y, X, family=sm.families.Binomial(
            sm.families.links.probit()))
        # model = sm.GLM(Y, X, family=sm.families.Gaussian(sm.families.links.log())) #, cov_type='HC3')
        result = model.fit()

        # Show results of the probit regression
        # print(result.summary())

        b = result.params

        # Convert probit coefficients to lognormal distribution parameters
        theta = np.exp(-b[0] / b[1])
        beta = 1 / b[1]

        return b, theta, beta

    async def get(self, run_result_id: int) -> RunResult:
        """Get a run result by id"""
        res = await self.session.exec(
            select(RunResult).where(RunResult.id == run_result_id)
        )
        run_result = res.one_or_none()
        if not run_result:
            raise HTTPException(status_code=404, detail="Run result not found")

        return run_result

    async def find(self, filter: dict | str, sort: list | str, range: list | str) -> list[int, int, int, RunResult]:
        """Get all run results matching filter and range"""
        builder = QueryBuilder(RunResult, filter, sort, range)

        # Do a query to satisfy total count for "Content-Range" header
        count_query = builder.build_count_query()
        total_count_query = await self.session.exec(count_query)
        total_count = total_count_query.one()

        # Main query
        start, end, query = builder.build_query(total_count)

        # Execute query
        results = await self.session.exec(query)
        run_results = results.all()

        return [start, end, total_count, run_results]

    async def create(self, run_result: RunResult) -> RunResult:
        """Create a run result"""
        self.session.add(run_result)
        await self.session.commit()
        await self.session.refresh(run_result)
        return run_result

    async def patch(self, run_result_id: int, run_result: RunResultUpdate) -> RunResult:
        """Update a run result"""
        res = await self.session.exec(
            select(RunResult).where(RunResult.id == run_result_id)
        )
        run_result_db = res.one()
        run_result_data = run_result.dict(exclude_unset=True)

        if not run_result_db:
            raise HTTPException(status_code=404, detail="Run result not found")

        # Update the fields from the request
        for field, value in run_result_data.items():
            setattr(run_result_db, field, value)

        self.session.add(run_result_db)
        await self.session.commit()
        await self.session.refresh(run_result_db)
        return run_result_db

    async def delete(self, run_result_id: int) -> None:
        """Delete a run result by id"""
        res = await self.session.exec(
            select(RunResult).where(RunResult.id == run_result_id)
        )
        run_result = res.one_or_none()

        if run_result:
            await self.session.delete(run_result)
            await self.session.commit()

    async def delete_by_experiment(self, experiment_id: int) -> None:
        """Delete all run results by experiment id"""
        start, stop, total_count, run_results = await self.find(filter={"experiment_id": experiment_id}, sort=None, range=None)
        if run_results:
            [await self.session.delete(run_result) for run_result in run_results]
            await self.session.commit()
