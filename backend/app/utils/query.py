from sqlmodel import SQLModel, select
from sqlalchemy import func, text
import json


class QueryBuilder:

    def __init__(self, model: SQLModel, filter: dict | str, sort: list | str, range: list | str):
        self.model = model
        self.filter = json.loads(filter) if filter and type(
            filter) == str else (filter if filter else {})
        self.sort = json.loads(sort) if sort and type(
            sort) == str else (sort if sort else [])
        self.range = json.loads(range) if range and type(
            range) == str else (range if range else [])

    def build_count_query(self):
        return self._apply_filter(select(func.count(self.model.id)))

    def build_frequencies_query(self, field: str):
        column = getattr(self.model, field)
        query = select(column, func.count().label("count")).order_by(text("count DESC")).group_by(
            text(field))
        return self._apply_filter(query)

    def build_parallel_count_query(self, fields: list[str]):
        columns = [getattr(self.model, field)
                   for field in fields]
        selected_columns = columns + [func.count().label("count")]
        query = select(*selected_columns).group_by(*columns).order_by(*columns)
        return self._apply_filter(query)

    def build_query(self, total_count):
        query = self._apply_filter(select(self.model))
        query = self._apply_sort(query)
        return self._apply_range(query, total_count)

    def _apply_filter(self, query):
        if len(self.filter):
            for field, value in self.filter.items():
                column = getattr(self.model, field)
                if isinstance(value, list):
                    if len(value) == 1:
                        query = self._apply_filter_value(
                            query, field, column, value[0])
                    else:
                        query = query.where(column.in_(value))
                else:
                    query = self._apply_filter_value(
                        query, field, column, value)
        return query

    def _apply_filter_value(self, query, field, column, value):
        if field == "id" or field == "reference_id" or field == "experiment_id" or isinstance(value, int):
            query = query.where(column == value)
        elif value is None:
            query = query.where(column.is_(None))
        else:
            query = query.where(column.ilike(f"%{value}%"))
        return query

    def _apply_sort(self, query):
        if len(self.sort) == 2:
            sort_field, sort_order = self.sort
            attr = getattr(self.model, sort_field)
            if sort_order == "ASC":
                query = query.order_by(attr)
            else:
                query = query.order_by(attr.desc())
        return query

    def _apply_range(self, query, total_count):
        if len(self.range) == 2:
            start, end = self.range
            query = query.offset(start).limit(end - start + 1)
            return start, end, query
        else:
            return 0, total_count, query
