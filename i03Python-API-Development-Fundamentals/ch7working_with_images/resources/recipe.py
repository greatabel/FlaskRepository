import os
from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from http import HTTPStatus


from models.recipe import Recipe
from schemas.recipe import RecipeSchema
from marshmallow import ValidationError

           
from extensions import image_set

from utils import save_image


recipe_schema = RecipeSchema()
recipe_cover_schema = RecipeSchema(only=('cover_url', ))
recipe_list_schema = RecipeSchema(many=True)


class RecipeListResource(Resource):
    
    def get(self):
        data = []
        recipes = Recipe.get_all_publish()
        data = recipe_list_schema.dump(recipes)
        return data, HTTPStatus.OK

    @jwt_required
    def post(self):
        json_data = request.get_json()

        current_user = get_jwt_identity()
        try:
            data = recipe_schema.load(data=json_data)

            recipe = Recipe(**data)
            recipe.user_id = current_user
            recipe.save()
            return recipe_schema.dump(recipe), HTTPStatus.CREATED

        except ValidationError as err:
            return {'message': err.messages}, HTTPStatus.BAD_REQUEST


        


class RecipeResource(Resource):

    @jwt_optional
    def get(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if recipe.is_publish == False and recipe.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return recipe.data(), HTTPStatus.OK

    @jwt_required
    def patch(self, recipe_id):

        json_data = request.get_json()

        try:
            data = recipe_schema.load(data=json_data)

            recipe = Recipe.get_by_id(recipe_id=recipe_id)

            if recipe is None:
                return {'message': 'Recipe not found'}, HTTPStatus.NOT_FOUND

            current_user = get_jwt_identity()

            if current_user != recipe.user_id:
                return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
                
            recipe.name = data.get('name') or recipe.name
            recipe.description = data.get('description') or recipe.description
            recipe.num_of_servings = data.get('num_of_servings') or recipe.num_of_servings
            recipe.cook_time = data.get('cook_time') or recipe.cook_time
            recipe.directions = data.get('directions') or recipe.directions

            recipe.save()

            return recipe_schema.dump(recipe), HTTPStatus.OK

        except ValidationError as err:
            return {'message': err.messages}, HTTPStatus.BAD_REQUEST



    @jwt_required
    def delete(self, recipe_id):

        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if recipe is None:
            return {'message': 'Recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        recipe.delete()

        return {}, HTTPStatus.NO_CONTENT



class RecipePublishResource(Resource):
    @jwt_required
    def put(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if recipe is None:
            return {'message': 'Recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        recipe.is_publish = True
        recipe.save()

        return {}, HTTPStatus.NO_CONTENT

    @jwt_required
    def delete(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if recipe is None:
            return {'message': 'Recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        recipe.is_publish = False


class RecipeCoverUploadResource(Resource):
    @jwt_required
    def put(self, recipe_id):

        file = request.files.get('cover')

        if not file:
            return {'message': 'Not a valid image'}, HTTPStatus.BAD_REQUEST

        if not image_set.file_allowed(file, file.filename):
            return {'message': 'File type not allowed'}, HTTPStatus.BAD_REQUEST

        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if recipe is None:
            return {'message': 'Recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        if recipe.cover_image:
            cover_path = image_set.path(folder='recipes', filename=recipe.cover_image)
            if os.path.exists(cover_path):
                os.remove(cover_path)

        filename = save_image(image=file, folder='recipes')
        recipe.cover_image = filename
        recipe.save()

        return recipe_cover_schema.dump(recipe), HTTPStatus.OK




