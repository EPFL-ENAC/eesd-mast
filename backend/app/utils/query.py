from sqlmodel import SQLModel, select
from sqlalchemy import func
import json

class QueryBuilder:
    
    def __init__(self, model: SQLModel, filter: dict | str, sort: list | str, range: list | str):
        self.model = model
        self.filter = json.loads(filter) if filter and type(filter) == str else {}
        self.sort = json.loads(sort) if sort and type(sort) == str else []
        self.range = json.loads(range) if range and type(range) == str else []
        
    def build_count_query(self):
        return self._apply_filter(self.model, self.filter, select(func.count(self.model.id)))

    def build_query(self, total_count):
        query = self._apply_filter(self.model, self.filter, select(self.model))
        query = self._apply_sort(self.model, self.sort, query)
        return self._apply_range(self.range, total_count, query)

    def _apply_filter(self, model, filter, query):
        if len(filter):
            for field, value in filter.items():
                attr = getattr(model, field)
                if isinstance(value, list):
                    query = query.where(attr.in_(value))
                elif field == "id" or field == "reference_id" or isinstance(value, int):
                    query = query.where(attr == value)
                else:
                    query = query.where(
                        attr.ilike(f"%{value}%")
                    )
        return query

    def _apply_sort(self, model, sort, query):
        if len(sort) == 2:
            sort_field, sort_order = sort
            attr = getattr(model, sort_field)
            if sort_order == "ASC":
                query = query.order_by(attr)
            else:
                query = query.order_by(attr.desc())
        return query

    def _apply_range(self, range, total_count, query):
        if len(range) == 2:
            start, end = range
            query = query.offset(start).limit(end - start + 1)
            return start, end, query
        else:
            return 0, total_count, query