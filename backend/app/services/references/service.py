from app.services.references.models import Reference, ReferenceUpdate, ReferenceRead
from app.services.experiments.service import ExperimentsService
from app.utils.query import QueryBuilder
from sqlmodel import select
from fastapi import HTTPException
from app.db import AsyncSession

class ReferenceService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, reference_id: int | str) -> Reference:
        """Get a reference by id or short name"""
        sel = select(Reference)
        if isinstance(reference_id, str):
            sel = sel.where(Reference.reference == reference_id)
        else:
            sel = sel.where(Reference.id == reference_id)
        res = await self.session.exec(sel)
        reference = res.one_or_none()
        if not reference:
            raise HTTPException(status_code=404, detail="Reference not found")

        return reference
    
    async def find(self, filter: dict | str, sort: list | str, range: list | str) -> list[int, int, int, Reference]:
        """Get all references matching filter and range"""
        builder = QueryBuilder(Reference, filter, sort, range)

        # Do a query to satisfy total count for "Content-Range" header
        count_query = builder.build_count_query()
        total_count_query = await self.session.exec(count_query)
        total_count = total_count_query.one()

        # Main query
        start, end, query = builder.build_query(total_count)

        # Execute query
        results = await self.session.exec(query)
        references = results.all()

        return [start, end, total_count, references]
    
    async def create(self, reference: Reference) -> ReferenceRead:
        """Create a reference"""
        self.session.add(reference)
        await self.session.commit()
        await self.session.refresh(reference)
        return reference
    
    async def patch(self, reference_id: int, reference: ReferenceUpdate) -> ReferenceRead:
        """Update a reference"""
        res = await self.session.exec(
            select(Reference).where(Reference.id == reference_id)
        )
        reference_db = res.one()
        if not reference_db:
            raise HTTPException(status_code=404, detail="Reference not found")

        reference_data = reference.dict(exclude_unset=True)
        for key, value in reference_data.items():
            setattr(reference_db, key, value)

        await self.session.commit()
        await self.session.refresh(reference_db)

        return reference_db
    
    async def delete(self, reference_id: int, recursive: bool = False) -> None:
        """Delete a reference by id"""
        res = await self.session.exec(
            select(Reference).where(Reference.id == reference_id)
        )
        reference = res.one_or_none()
        if reference:
            if recursive:
                # Delete all experiments that reference this reference
                service = ExperimentsService(self.session)
                await service.delete_by_reference(reference_id, recursive)

            await self.session.delete(reference)
            await self.session.commit()