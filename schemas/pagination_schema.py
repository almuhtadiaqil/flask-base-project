from marshmallow import Schema, fields, validate


class PaginationSchema(Schema):
    page_index = fields.Integer(load_default=1)
    page_size = fields.Integer(load_default=5)
    search = fields.String(load_default=None)
    order_by = fields.String(load_default=None)
