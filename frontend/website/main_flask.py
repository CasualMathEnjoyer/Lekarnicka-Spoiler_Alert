from flask import Flask
import os

# from frontend.website.camera import Camera

def create_app():
    app = Flask(__name__)

    from .views import views
    from .author import author

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(author, url_prefix="/")

    # app.config["UPLOAD_FOLDER"] = "photos"
    #
    # # Create the "photos" directory if it doesn't exist
    # if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    #     os.makedirs(app.config["UPLOAD_FOLDER"])

    return app