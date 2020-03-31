from  app import *
from models.user import User
from models.recipe import Recipe


app = create_app()
# app.run(port=5000, debug=True)
with app.app_context():
    user = User(username='abel', email='abel@gmail.com', password='test')
    db.session.add(user)
    db.session.commit()

    print(user.username, user.email)

    pizza = Recipe(name='Cheese Pizza', description='This is a lovely cheese pizza recipe', 
        num_of_servings=2, cook_time=30, directions='This is how you make it', user_id=user.id)
    db.session.add(pizza)
    db.session.commit()

    pasta = Recipe(name='Tomato Pasta', description='This is a lovely tomato pasta recipe', 
        num_of_servings=3, cook_time=20, directions='This is how you make it', user_id=user.id)
    db.session.add(pasta)
    db.session.commit()

    user = User.query.filter_by(username='abel').first()

    for recipe in user.recipes:
        print('{} recipe made by {} can serve {} people.'.format(recipe.name, 
                recipe.user.username, recipe.num_of_servings))
