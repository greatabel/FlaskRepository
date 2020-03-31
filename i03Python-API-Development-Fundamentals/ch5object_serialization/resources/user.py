from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required
from http import HTTPStatus

from webargs import fields
from webargs.flaskparser import use_kwargs

from models.recipe import Recipe
from models.user import User

from schemas.user import UserSchema
from schemas.recipe import RecipeSchema
from marshmallow import ValidationError


user_schema = UserSchema()
user_public_schema = UserSchema(exclude=('email', ))
recipe_list_schema = RecipeSchema(many=True)


class UserListResource(Resource):
    def post(self):
        json_data = request.get_json()

        # data, errors = user_schema.load(data=json_data)
        try:
            data = user_schema.load(data=json_data)

            username = data.get('username')
            email = data.get('email')

            if User.get_by_username(username):
                return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST

            if User.get_by_email(email):
                return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST

            user = User(**data)
            user.save()

            data = user_schema.dump(user)
            return data, HTTPStatus.CREATED

        except ValidationError as err:
            return {'message': err.messages}, HTTPStatus.BAD_REQUEST
        # if errors:
        #     return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST




class UserResource(Resource):

    @jwt_optional
    def get(self, username):

        user = User.get_by_username(username=username)

        if user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        # print('current_user=', current_user, user.id)
        if current_user == user.id:
            data = user_schema.dump(user)
        else:
            data = user_public_schema.dump(user)

        return data, HTTPStatus.OK


class MeResource(Resource):

    @jwt_required
    def get(self):
        user = User.get_by_id(id=get_jwt_identity())

        data = user_schema.dump(user)

        return data, HTTPStatus.OK
        
example_args = {
    'visibility': fields.String(missing='public')    
}

class UserRecipeListResource(Resource):
    #visibility 和 username 顺序很重要，错了不行
    @jwt_optional
    @use_kwargs(example_args, location="query")
    def get(self, visibility, username):
        print('visibility=', visibility)
        user = User.get_by_username(username=username)

        if user is None:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        print(current_user, user.id, visibility)
        if current_user == user.id and visibility in ['all', 'private']:
            pass
        else:
            visibility = 'public'

        recipes = Recipe.get_all_by_user(user_id=user.id, visibility=visibility)
        # print('recipes=', recipes)
        data = recipe_list_schema.dump(recipes)
        return data, HTTPStatus.OK



