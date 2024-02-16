# Lékárnička
(a.k.a. **Spoiler Alert**)

_The maintainer of your first-aid-kit._

## Project information
_This DEMO application was collaboratively developed by a team at
CVUT FJFI during Winter semester 2023, as a Data Science assignment._

### What is this project?
_This project is a web application designed to allow users to 
manage their medications effectively, featuring a notification 
system that alerts users when their medications are nearing expiration._

Users can register using their **email** and a
**password**. This app can be then used to **scan the barcode** 
and **expiration date** on their medication. 
The [EAN](https://en.wikipedia.org/wiki/International_Article_Number#:~:text=The%20International%20Article%20Number%20)
code extracted from the barcode is used to 
find the name of the medication, and the expiration date is detected
using a convolutional neural network. The
user medication information is then saved to the database.

Furthermore, a system of **notifications** is connected to
the database, and the users are alerted via email when their medications
are nearing expiration.

### THE PRIMARY OBJECTIVES
1. [*REDUCE MEDICATION WASTE*](https://noharm-europe.org/sites/default/files/documents-files/4646/2013-12%20Unused%20pharmaceuticals.pdf)
2. [*ENCOURAGE RETURNING UNUSED MEDICATION TO PHARMACY*](https://www.cithara.cz/proc-vracet-stare-leky-do-lekarny/)
3. *HAVE YOUR MEDICATION INFORMATION AT HAND*

### MADE BY
 - Fucsiková Tereza   (neural network implementation)
 - Gaj Aleksej        (code extraction and technical advice)
 - Molnárová Soňa     (neural network research)
 - Morovicsová Katka  (planning, integration, testing)
 - Potúčková Tereza   (data preparation)
 - Studenovský Štěpán (database)
 - Štampach Adam      (frontend design)

As part of out final presentation a 
[PowerPoint presentation](https://docs.google.com/presentation/d/15IROdhD2hQe8S9msTfJbCceqlZpkbSScS4zMufoDw0M/edit#slide=id.p)
was made, including a DEMO video.

### Project Version Information

_This version of the project has been modified outside
the original scope submitted for the assignment. 
The edits and enhancements made in this version are 
not part of the official assignment submission 
but have been implemented by Katka Morovicsová for further development 
and improvement._

_To see the original repository, contact [aleksejalex](https://github.com/aleksejalex)._

## HOW TO RUN THE APP

### REQUIREMENTS
- Python: 3.10 (used during development)
- [GTK3-Runtime](https://gtk-win.sourceforge.io/home/)
- Additional python packages in `requirements.txt`
```bash
    pip install -r requirements.txt
```
  
### SET UP A DATABASE
You can either run a [Docker](https://www.docker.com/). 
container locally:

Navigate to the `database` folder
```bash
    docker compose up
```
_(This will download the [Postgres](https://www.postgresql.org/) 
and [Adminer](https://www.adminer.org/) images 
and start up a container with your database. You can then 
visualize the database using Adminer)_

**Or** you can connect to your own database by 
adjusting the information in 
`database_connection.py`:
```python
    db_params = {
        "host" : "localhost",
        "port" : 5432,
        "user" : "username",
        "password" : "password",
        "database" : "db",
        }
```
_Please note saving your database information in the script is not
a safe way to access it. Please connect your own database 
safely._
### RUN
```bash
    python frontend/run_website.py
```
### NAVIGATE TO THE WEBPAGE
Open your web browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) 
to view the app.

## FIRST LOOK AT THE APP
![Here your medications will be displayed](/Screenshots/img.png?raw=true "Screenshot")
![Login page](/Screenshots/img_1.png?raw=true "Screenshot")
![Add new drug](/Screenshots/img_2.png?raw=true "Screenshot")
![Medications displayed](/Screenshots/img_3.png?raw=true "Screenshot")
Mobile phone view:
![Mobile Phone view](/Screenshots/image101.jpg?raw=true "Screenshot")

## HOW IT WORKS

### BARCODE READER
The reader utilizes `OpenCV` library and `PyZBar` library 
to decode EAN code from images. It can also display the detected barcode 
on the image if specified.
2D code reader is to be added in the future.

### EAN to NAME
Upon detecting a code using the barcode reader, the application
initiates a query to the _pilulka.cz_ website, attempting to 
match the code with the corresponding medication. For this query,
`Selenium` is used.

**Why this solution?** Our focus was to
include as many prescription medication as possible, 
and at the time of developing this application, pilulka was 
identified as the only online pharmacy that retained at least partly the
visibility of EAN codes for prescription medications. 
It's important to note that this solution currently doesn't 
cover the majority of medications - future improvements will focus 
on expanding the database to include the most commonly used medications.

### DATE DETECTION
Expiry date is detected from an image using a Resnet
neural network implemented using the `doctr` library for optical 
character recognition. It includes functionality to 
extract potential dates from the recognized text.

For choosing an optimal model, we created our own dataset
(about 100 images) and tested several of the available models. 
Finally, the best model 
`crnn_vgg16_bn db_resnet50` tested with **71.43%** accuracy on our 
dataset.

### DATABASE
The database consists of three main tables:
- `users` table holds user details, such as a unique identifier (user_id), email (unique), password, and 
creation timestamp. 
- `user_medications_info` table contains information about medications, 
including a unique identifier (medication_id), name, dosage, and creation timestamp. This table stores user-specific medication information,
linking to the users table through the user_email field.
- `medications_info` is implemented for future use and possible 
synchronisation with the **SUKL** database.

### FRONTEND
See [Frontend RADME.md](frontend/README.md).

### NOTIFICATIONS
Our final application should automatically send notifications
to the users' email. This is done by having "the server" run the 
`notification.py` script every day. This script goes through all the 
users and their medications and then alerts the users
if their medication expiration is closer than 30 days.

For setting up automated emails, you need an email account to which
the script will be able to connect. We used a gmail account where
we enabled connection using 
[App password](https://knowledge.workspace.google.com/kb/how-to-create-app-passwords-000009237).

## Problems, issues and limitations: Future
- **Barcode reader** - our reader is able only to detect information from a
regular 1D code, and it's accuracy is limited. Original plan included
training our own neural network for improving detection, but this was not
completed due to time reasons.
- **2D code reader**: we managed to implement a 2D code reader, but it had 
a very low accuracy, and because of the specifics of the Czech medication
codes, which are designed to prevent forgery, we were unable to extract
the information about medication from them.
- The original **database** had a different structure relying 
heavily on SUKL codes. Because of the difficulties encountered
during the development, the database was greatly simplified,
and SUKL codes were not included.
- The neural network used for detecting the expiration date has
troubles detecting text which has been rotated. Future iterations
might include an improved version which tackles this issue.
- It's not possible to remove medications which were once added
using the frontend interface.