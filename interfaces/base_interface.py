from abc import ABC, abstractclassmethod
from schemas.pagination_schema import PaginationSchema
from marshmallow import Schema


class BaseRepositoryInterface(ABC):
    @abstractclassmethod
    def get_all(self):
        pass

    @abstractclassmethod
    def get_pagination(self, pagination_schema: PaginationSchema):
        pass

    @abstractclassmethod
    def store(self, schema: Schema):
        pass

    @abstractclassmethod
    def get_by_field(self, field, value):
        pass

    @abstractclassmethod
    def get_by_multi_field(self, datas):
        pass

    @abstractclassmethod
    def update(self, id, schema: Schema):
        pass

    @abstractclassmethod
    def delete(self, field, value):
        pass
