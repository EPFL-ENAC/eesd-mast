from sqlmodel import SQLModel, select
from sqlalchemy import func, text, or_, and_, cast, String, case
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
        query_ = select(column, func.count().label("count")).order_by(text("count DESC")).group_by(
            text(field))
        return self._apply_filter(query_)

    def build_frequencies_exists_query(self, field: str):
        column = getattr(self.model, field)
        case_expr = case(
            (cast(column, String) != 'null', 1),
            (column.is_(None), 1),
            else_=0)
        query_ = select(case_expr.label(field), func.count().label(
            'count')).order_by(text("count DESC")).group_by(case_expr)
        return self._apply_filter(query_)

    def build_parallel_count_query(self, fields: list[str]):
        columns = [getattr(self.model, field)
                   for field in fields]
        selected_columns = columns + [func.count().label("count")]
        query_ = select(*selected_columns).group_by(*
                                                    columns).order_by(*columns)
        return self._apply_filter(query_)

    def build_query(self, total_count):
        query_ = self._apply_filter(select(self.model))
        query_ = self._apply_sort(query_)
        return self._apply_range(query_, total_count)

    def build_filter_query(self, query_from):
        query_ = self._apply_filter(query_from)
        return query_

    def _apply_filter(self, query_):
        if len(self.filter):
            for field, value in self.filter.items():
                column = getattr(self.model, field)
                if isinstance(value, list):
                    if len(value) == 1 and value[0] is None:
                        query_ = self._apply_filter_value(
                            query_, field, column, value[0])
                    elif None in value:
                        noNoneValues = [v for v in value if v is not None]
                        query_ = query_.where(
                            or_(column.is_(None), column.in_(noNoneValues)))
                    elif field == "test_scale":
                        # test_scale is a float field, but when the first criteria is 1,
                        # the query parameters are passed as integers, then force
                        # the values to be floats
                        query_ = query_.where(column.in_(
                            [float(val) for val in value]))
                    else:
                        query_ = query_.where(column.in_(value))
                else:
                    query_ = self._apply_filter_value(
                        query_, field, column, value)
        return query_

    def _apply_filter_value(self, query_, field, column, value):
        if field == "id" or field == "reference_id" or field == "experiment_id" or field == "building_id" or isinstance(value, int):
            query_ = query_.where(column == value)
        elif value is None:
            query_ = query_.where(column.is_(None))
        elif isinstance(value, dict):
            query_ = self._apply_filter_object(query_, field, column, value)
        else:
            query_ = query_.where(column.ilike(f"%{value}%"))
        return query_

    def _apply_filter_object(self, query_, field, column, value):
        if '$exists' in value:
            if value['$exists']:
                query_ = query_.where(
                    and_(column.isnot(None), cast(column, String) != 'null'))
            elif not value['$exists']:
                query_ = query_.where(
                    or_(column.is_(None), cast(column, String) == 'null'))
        return query_

    def _apply_sort(self, query_):
        if len(self.sort) == 2:
            sort_field, sort_order = self.sort
            attr = getattr(self.model, sort_field)
            if sort_order == "ASC":
                query_ = query_.order_by(attr)
            else:
                query_ = query_.order_by(attr.desc())
        return query_

    def _apply_range(self, query_, total_count):
        if len(self.range) == 2:
            start, end = self.range
            query_ = query_.offset(start).limit(end - start + 1)
            return start, end, query_
        else:
            return 0, total_count, query_
