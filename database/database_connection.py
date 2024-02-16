import psycopg2
import csv


# choose your database

db_params = {
    "host" : "localhost",
    "port" : 5432,
    "user" : "username",
    "password" : "password",
    "database" : "db",
}

# storing database info like this in the script is not a safe option
# but since this is info for a locally hosted docker container and this is a DEMO, we do it like this
# but in the real world use environment variables:
# https://dev.to/biplov/handling-passwords-and-secret-keys-using-environment-variables-2ei0
# this should also work when run in a docker container

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def create_connection():
    try:
        return psycopg2.connect(**db_params)
    except Exception as e:
        print(f"An error occurred in create_connection: {e}")

def insert_user(email, pwd):
    try:
        conn = create_connection()
        conn.autocommit = True
        cur = conn.cursor()

        sql_command = "SELECT insert_user(%s, %s);"
        cur.execute(sql_command, (email, pwd))
        result = cur.fetchone()
        print(result[0])
        if result[0] == "Error: Email already exists.":
            cur.close()
            conn.close()
            return False

        cur.close()
        conn.close()
        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False
def check_pwd(email, provided_pwd):
    conn, cur = None, None
    try:
        conn = create_connection()

        with conn.cursor() as cur:
            cur.callproc('check_password', (email, provided_pwd))
            result = cur.fetchone()

            if result is not None:
                print("Password is correct!")
                return result[0]
            else:
                print("Password is incorrect.")
                return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
def retrieve_user_medications(user_email):
    conn, cur = None, None
    try:
        conn = create_connection()
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("SELECT * FROM get_user_medications_info(%s);", (user_email,))
        medications = cur.fetchall()
        medications_without_data = []  # cos there is the time when it was added
        for medication in medications:
            medications_without_data.append(medication[:3])
        return medications_without_data

    except psycopg2.Error as e:
        print("Error retrieving user medications:", e)

    finally:
        # Close the cursor and connection
        if cur:
            cur.close()
        if conn:
            conn.close()
def add_user_medication(user_name, medication_name, expiration_date):
    success = False
    conn, cur = None, None

    try:
        conn = create_connection()
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("SELECT add_user_medication_info(%s, %s, %s);",
                    (user_name, medication_name, str(expiration_date)))
        success = True

    except psycopg2.Error as e:
        print(f"Error adding medication for {user_name}:", e)
        success = False

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        return success
def _remove_user_medication(user_name, medication_name, exp_date):
    conn, cur = None, None
    try:
        conn = create_connection()
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("SELECT remove_user_medication_info(%s, %s, %s);",
                    (user_name, medication_name, str(exp_date)))
        result = cur.fetchone()
        return result

    except psycopg2.Error as e:
        print(f"Error removing medication for {user_name}:", e)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
def get_all_med_info():
    conn, cur = None, None
    try:
        conn = create_connection()
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("SELECT * FROM get_all_medications_info();")

        # Fetch all rows
        rows = cur.fetchall()

        for row in rows:
            print(row)

    except psycopg2.Error as e:
        print(f"Error: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
def get_all_users():
    conn, cur = None, None
    users = []
    try:
        # Connect to the database
        conn = create_connection()
        conn.autocommit = True
        cur = conn.cursor()

        cur.callproc('get_all_users')

        # Fetch all results
        result = cur.fetchall()

        # Print or process the results as needed
        # for row in result:
        #     users.append(row[0])

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        return users

if __name__ == "__main__":
    pass
    # from datetime import datetime, timedelta
    # # Example usage:
    # user_email = 'test@test.whatever'
    #
    # # Retrieve all medications for a given user
    # medications = retrieve_user_medications(user_email)
    # print("User Medications:", medications)
    #
    # # Add a new medication for the user
    # new_medication_name = 'NewMedicine23'
    # new_medication_dosage = '10mg'
    # expiration_date = datetime.now() + timedelta(days=30)
    # add_user_medication(user_email, new_medication_name, expiration_date)
    # print(f"Added {new_medication_name} for {user_email} with expiration date {expiration_date}")
    #
    # # Retrieve user medications again
    # medications = retrieve_user_medications(user_email)
    # print("User Medications:", medications)
    #
    # # Remove a medication for the user
    # medication_to_remove = 'NewMedicine23'
    # result = _remove_user_medication(user_email, medication_to_remove, expiration_date)
    # print(f"Removed {medication_to_remove} for {user_email}")
    #
    # # Retrieve user medications after removal
    # medications = retrieve_user_medications(user_email)
    # print("User Medications:", medications)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
