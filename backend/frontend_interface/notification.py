import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Database.database_connection import get_all_users, retrieve_user_medications

path_to_file = ""  # set your own path to the file containing connection information

def send_email(to_address, subject, message):
    # Set up the email parameters
    # a file with access key to the email, should not be public
    with open(path_to_file) as file:
        file = file.read()

    from_address = file.split(',')[0]          # Replace with your email address
    password = file.split(',')[1]              # Replace with your email password

    # Create the MIME object
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    # Attach the message to the email
    msg.attach(MIMEText(message, 'plain'))

    # Connect to the SMTP server (in this case, Gmail's SMTP server)
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        # Start the TLS encryption
        server.starttls()

        server.login(from_address, password)
        server.sendmail(from_address, to_address, msg.as_string())

    print(f"Email sent successfully to {to_address}")

# Example usage
# to_email = 'email@gmail.com'  # Replace with the recipient's email address
# email_subject = 'Hello Email'
# email_message = 'Hello! This is a test email.'
#
# send_email(to_email, email_subject, email_message)

def days_until_given_date(date_string):
    try:
        # Convert the input date string to a datetime object using dateutil.parser
        given_date = parser.parse(date_string)

        # Get the current date
        current_date = datetime.date.today()
        current_date = parser.parse(str(current_date))

        # Calculate the difference in days
        days_difference = (given_date - current_date).days

        return days_difference
    except ValueError as e:
        return f"Error: {e}"

def retrieve_users_send_mails():
    # returns list of all users from the database
    # for every user, returns all medication with their expiration dates
    # if expiration date is close, sends notifications
    users = get_all_users()
    print(users)
    for email in users:
        # print("user:", email)
        meds = retrieve_user_medications(email)
        print("meds:", meds)
        bad_meds = []
        for med in meds:
            try:
                try:
                    print(parser.parse(med[2]))
                except:
                    print("no")
                days = days_until_given_date(med[2])
                if days < 30:
                    print("warnin man:", med)
                    bad_meds.append(med)
                else:
                    # print("med ok man:", med)
                    pass
            except TypeError as e:
                # print(f"Error: {e}")
                pass
        if len(bad_meds) > 0:
            subject = "Brzy Vám prochází lék!!!!!!!!!!"
            message = 'Brzy Vám projdou nasledující léky:\n'
            for med in bad_meds:
                line = med[1] + " prochází " + med[2] + "\n"
                message += line
            print(email)
            print(subject)
            print(message)
            send_email(email, subject, message)

if __name__ == "__main__":
    retrieve_users_send_mails()
