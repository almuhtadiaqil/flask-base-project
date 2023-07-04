from app import db
from datetime import datetime
from schemas.pagination_schema import PaginationSchema
from sqlalchemy.sql import text
from schemas.error_schema import ErrorSchema
from datetime import datetime
from interfaces.base_interface import BaseRepositoryInterface
from marshmallow import Schema
from app import db
from sqlalchemy import and_

ts = datetime.utcnow()


class BaseRepository(BaseRepositoryInterface):
    def __init__(self, model) -> None:
        self.model = model

    def get_all(self):
        query = self.model.query.all()
        return query

    def get_pagination(self, request: PaginationSchema):
        try:
            query = self.model.query.filter(self.model.deleted_at == None)
            search = request["search"]
            order_by = request["order_by"]
            page_index = int(request["page_index"])
            page_size = int(request["page_size"])

            if search is not None:
                search = "%{}%".format(search.lower())
                search_filters = []
                for column in self.model.__table__.columns:
                    if column.name != "id":  # Exclude the 'id' column from search
                        search_filters.append(column.ilike(search))
                query.filter(*search_filters)

            if order_by is not None:
                order_by = order_by.split(",")
                query.order_by(text("{} {}".format(order_by[0], order_by[1])))
            count = len(query.all())
            result = query.paginate(page_index, page_size)
            return result, count
        except Exception as e:
            error = ErrorSchema().load({"message": str(e), "code": 500})
            raise Exception(error)

    def get_specific_field_distinct(self, columns):
        column_objects = [getattr(self.model, column) for column in columns]
        query = self.model.query.with_entities(*column_objects).distinct().all()
        return query

    def store(self, schema: Schema):
        data = self.model(**schema)
        db.session.add(data)
        db.session.commit()

    def get_by_field(self, field, value):
        try:
            result = self.model.query.filter(
                text("{} = '{}'".format(field, value))
            ).first()
            return result
        except Exception as e:
            error = ErrorSchema().load({"message": str(e), "code": 500})
            raise Exception(error)

    def get_by_multi_field(self, datas):
        try:
            result = self.model.query.filter(
                *[
                    and_(getattr(self.model, field["field"]) == field["value"])
                    for field in datas
                ]
            ).first()
            return result
        except Exception as e:
            error = ErrorSchema().load({"message": str(e), "code": 500})
            raise Exception(error)

    def update(self, field, value, schema: Schema):
        try:
            data = self.model.query.filter(
                text("{} = '{}'".format(field, value))
            ).first()
            if data is None:
                error = ErrorSchema().load(
                    {"message": str("record is not found"), "code": 400}
                )
                raise Exception(error)
            for key, value in schema.fields.items():
                value = value.default() if callable(value.default) else value.default
                setattr(data, key, value)
            db.session.commit()
            return data
        except Exception as e:
            error = ErrorSchema().load({"message": str(e), "code": 500})
            raise Exception(error)

    def delete(self, field, value):
        try:
            data = self.model.query.filter(
                text("{} = '{}'".format(field, value))
            ).first()
            if not data:
                error = ErrorSchema().load(
                    {"message": str("record is not found"), "code": 400}
                )
                raise Exception(error)
            db.session.delete(data)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            error = ErrorSchema().load({"message": str(e), "code": 500})
            raise Exception(error)
