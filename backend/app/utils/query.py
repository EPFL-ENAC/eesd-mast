from sqlmodel import select
from sqlalchemy import func
import json

class QueryBuilder:
    
    def __init__(self, model, filter: str, sort: str, range: str):
        self.model = model
        self.filter = json.loads(filter) if filter else {}
        self.sort = json.loads(sort) if sort else []
        self.range = json.loads(range) if range else []
        
    def build_count_query(self):
        return self._apply_filter(self.model, self.filter, select(func.count(self.model.id)))

    def build_query(self, total_count):
        query = self._apply_filter(self.model, self.filter, select(self.model))
        query = self._apply_sort(self.model, self.sort, query)
        return self._apply_range(self.range, total_count, query)

    def _apply_filter(self, model, filter, query):
        if len(filter):
            for field, value in filter.items():
                if isinstance(value, list):
                    query = query.where(getattr(model, field).in_(value))
                elif field == "id" or field == "reference_id":
                    query = query.where(getattr(model, field) == value)
                else:
                    query = query.where(
                        getattr(model, field).ilike(f"%{value}%")
                    )
        return query

    def _apply_sort(self, model, sort, query):
        if len(sort) == 2:
            sort_field, sort_order = sort
            if sort_order == "ASC":
                query = query.order_by(getattr(model, sort_field))
            else:
                query = query.order_by(getattr(model, sort_field), getattr(model, sort_field).desc())
        return query

    def _apply_range(self, range, total_count, query):
        if len(range) == 2:
            start, end = range
            query = query.offset(start).limit(end - start + 1)
            return start, end, query
        else:
            return 0, total_count, query
  #