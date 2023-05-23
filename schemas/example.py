from marshmallow import Schema,fields, validate

class ExampleSchema(Schema):
    name = fields.String(required=True,)
    
    
class Meta:
    strict = True