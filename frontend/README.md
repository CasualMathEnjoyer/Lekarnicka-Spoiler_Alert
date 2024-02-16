# Frontend

This readme provides an overview of the Frontend, including its structure, main functionalities, and usage.

## Overview

The Flask app is designed to manage a user's medication information. Users can add drugs to their aid kit by providing details such as the drug's name and expiration date. The app also includes functionality to recognize drug names and expiration dates from uploaded images.

## App Structure

The Flask app consists of the following components:

- **`main_flask.py`**: The main script to run the Flask app. It initializes the app, sets up configurations, and starts the server.

- **`views` Blueprint (inside `main_flask.py`)**: Handles the routes related to user interactions, such as displaying the home page and adding drugs to the aid kit.

- **`author` Blueprint (inside `main_flask.py`)**: Manages user authentication, including login and signup functionality.

- **`templates` Folder**: Contains HTML templates for rendering web pages, including the home page and drug addition forms.

- Additionally **`frontend_interface/app_logic.py`** contains backend logic for processing drug-related functionalities, such as barcode recognition and database interactions.

## Main Functionalities

### Home Page

- Accessible via the root URL or "/home."
- Displays the user's aid kit with a list of added drugs.

### Add Drug Page

- Accessed through the "/add_drug" route.
- Allows users to add a new drug to their aid kit.
- Supports barcode scanning and image upload for drug information.

### User Authentication

- Login: Accessed through "/login."
- Signup: Accessed through "/signup."

User passwords are protected using hash function.

## Error Handling

The app includes error handling for various scenarios, such as missing data, incorrect file formats, or unsuccessful database operations. Error messages are displayed to guide users in resolving issues.

## Additional Notes

- The app is set to run in non-debug mode by default for faster loading. Modify the `app.run` line in `run_website.py` if you need to enable debug mode.

- Ensure that the required dependencies are installed before running the app.

- For any additional customization or modifications, refer to the Flask documentation: [Flask Documentation](https://flask.palletsprojects.com/).
