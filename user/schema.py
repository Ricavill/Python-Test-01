from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from user.model import User


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ('pass_hash',)
