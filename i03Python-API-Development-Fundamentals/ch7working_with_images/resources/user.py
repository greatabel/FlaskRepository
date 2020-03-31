import os
from flask import request, url_for, render_template
from flask_restful import Resource
from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required
from http import HTTPStatus

from webargs import fields
from webargs.flaskparser import use_kwargs

from extensions import image_set
from mailgun import MailgunApi
from models.recipe import Recipe
from models.user import User



from schemas.user import UserSchema
from schemas.recipe import RecipeSchema
from marshmallow import ValidationError

from utils import generate_token, verify_token, save_image


user_schema = UserSchema()
user_public_schema = UserSchema(exclude=('email', ))
user_avatar_schema = UserSchema(only=('avatar_url', ))
recipe_list_schema = RecipeSchema(many=True)

domain = os.environ.get('YOUR_DOMAIN_NAME', '')
api_key = os.environ.get('YOUR_API_KEY', '')
mailgun = MailgunApi(domain=domain, api_key=api_key)

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

            token = generate_token(user.email, salt='activate')
            subject = '请确认你的注册'
            link = url_for('useractivateresource',
                            token=token,
                            _external=True)
            # text = '感谢使用 SmileCook! 请点击确认链接: {}'.format(link)
            #  text Body of the message. (text version)/ html:Body of the message. (HTML version)
            text = None

            mailgun.send_email(to=user.email,
                               subject=subject,
                               text=text,
                               html=render_template('email/confirmation.html', link=link))

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


class UserActivateResource(Resource):
    def get(self, token):
        email = verify_token(token, salt='activate')
        if email is False:
            return {'message': 'Invalid token or token expired'}, HTTPStatus.BAD_REQUEST

        user = User.get_by_email(email=email)
        if not user:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        if user.is_active is True:
            return {'message': 'The user account is already activated'}, HTTPStatus.BAD_REQUEST

        user.is_active = True
        user.save()

        return {}, HTTPStatus.NO_CONTENT


class UserAvatarUploadResource(Resource):
    @jwt_required
    def put(self):

        file = request.files.get('avatar')

        if not file:
            return {'message': 'Not a valid image'}, HTTPStatus.BAD_REQUEST

        if not image_set.file_allowed(file, file.filename):
            return {'message': 'File type not allowed'}, HTTPStatus.BAD_REQUEST

        user = User.get_by_id(id=get_jwt_identity())

        if user.avatar_image:
            avatar_path = image_set.path(folder='avatars', filename=user.avatar_image)
            if os.path.exists(avatar_path):
                os.remove(avatar_path)

        filename = save_image(image=file, folder='avatars')

        user.avatar_image = filename
        user.save()

        return user_avatar_schema.dump(user), HTTPStatus.OK






