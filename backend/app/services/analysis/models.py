from pydantic import BaseModel


class Metrics(BaseModel):
    experiments_count: int
    references_count: int
    run_results_count: int
