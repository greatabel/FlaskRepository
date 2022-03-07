import os

from flask import Flask





def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = os.path.join('covid', 'adapters', 'data')

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']



    

    # with app.app_context():
    #     # Register blueprints.
    #     from .home import home
    #     # app.register_blueprint(home.home_blueprint)
    return app


