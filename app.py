from flask import Flask
from blueprints.api.routes import library_bp
from blueprints.website.view import library_wb_bp
import os
from dotenv import load_dotenv
from extension import mongo
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app = Flask(__name__)

    # configuration for the database of mongodb
    app.config["MONGO_URI"] = "mongodb://localhost:27017/science_library"
    app.config['SECRET_KEY'] = os.getenv('SUPER_SECRET_KEY','default_secret_key')
    mongo.init_app(app)

    # create a unique key for a collections of database science library
    mongo.db.books.create_index("id",unique=True)
    mongo.db.books.create_index("isbn",unique=True)
    mongo.db.user.create_index("user_id",unique=True)
    mongo.db.user.create_index("username",unique=True)

    # register the blueprint of api and website
    app.register_blueprint(library_bp)
    app.register_blueprint(library_wb_bp)
    
    return app


    

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)