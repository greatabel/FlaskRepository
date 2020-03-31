import datetime as dt
from marshmallow import Schema, fields, post_load
from marshmallow import pprint


# https://marshmallow.readthedocs.io/en/stable/quickstart.html
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = dt.datetime.now()

    def __repr__(self):
        return "<User(name={self.name!r})>".format(self=self)

# Create a schema by defining a class with variables mapping attribute names to Field objects.
class UserSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()

# create a schema from a dictionary of fields using the from_dict method.
UserSchemaA = Schema.from_dict(
    {"name": fields.Str(), "email": fields.Email(), "created_at": fields.DateTime()}
)


#Serializing Objects
user = User(name="Monty", email="monty@python.org")
schema = UserSchema()
result = schema.dump(user)
pprint(result)
print(type(result))

print('You can also serialize to a JSON-encoded string: 注意dump vs dumps')
json_result = schema.dumps(user)
pprint(json_result)
print(type(json_result))

user1 = User(name="Mick", email="mick@stones.com")
user2 = User(name="Keith", email="keith@stones.com")
users = [user1, user2]
schema = UserSchema(many=True)
result = schema.dump(users)  # OR UserSchema().dump(users, many=True)
pprint(result)


print('Deserializing Objects\n')
user_data = {
    # "created_at": "2014-08-11T05:26:03.869245",
    "email": "ken@yahoo.com",
    "name": "Ken",
}
schema = UserSchema()
result = schema.load(user_data)
pprint(result)
print(type(result))

class UserSchemaB(Schema):
    name = fields.Str()
    email = fields.Email()
    # created_at = fields.DateTime()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

schema_b = UserSchemaB()
result = schema_b.load(user_data)
pprint(result)
print(type(result))






