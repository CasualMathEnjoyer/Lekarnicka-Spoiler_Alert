from website.main_flask import create_app
import os

print("importing backend...")
import backend.frontend_interface.app_logic as al
print("backend imported")

if __name__ == "__main__":
    print("starting website...")
    app = create_app()

    app.al = al

    UPLOAD_FOLDER = 'photos'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SECRET_KEY'] = os.urandom(16)

    # app.run(debug=True)
    # spoustet v nedebug modu, aby bylo nacitani rychlejsi:
    app.run(debug=False, host= '0.0.0.0')