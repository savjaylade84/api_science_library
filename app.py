from flask import Flask
from .blueprints.api import routes
from .blueprints.website import view
import os
from dotenv import load_dotenv
from .extension import mongo, jwt


load_dotenv()

def create_app():
    app = Flask(__name__)
    app = Flask(__name__)

    # configuration for the secret key
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    jwt.init_app(app)

    # configuration for the database of mongodb
    app.config["MONGO_URI"] = "mongodb://localhost:27017/science_library"
    mongo.init_app(app)

    # create a unique key for a collections of database science library
    mongo.db.books.create_index("id",unique=True)
    mongo.db.books.create_index("isbn",unique=True)
    mongo.db.users.create_index("user_id",unique=True)
    mongo.db.users.create_index("username",unique=True)
    mongo.db.users.create_index("super_key",unique=True)

    # register the blueprint of api and website
    app.register_blueprint(routes.library_bp)
    app.register_blueprint(view.library_wb_bp)
    
    return app


    

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)