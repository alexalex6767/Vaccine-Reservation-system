from model.Vaccine import Vaccine
from model.Caregiver import Caregiver
from model.Patient import Patient
from util.Util import Util
from db.ConnectionManager import ConnectionManager
import pymssql
import datetime

'''
objects to keep track of the currently logged-in user
Note: it is always true that at most one of currentCaregiver and currentPatient is not null
        since only one user can be logged-in at a time
'''
current_patient = None

current_caregiver = None

def create_patient(tokens):
    # create_patient <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Failed to create user.")
        return

    username = tokens[1]
    password = tokens[2]
    # check 2: check if the username has been taken already
    if username_exists_patient(username):
        print("Username taken, try again!")
        return

    # check 3: check if the password is strong enough
    if isStrongPassword(password) is False:
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the caregiver
    patient = Patient(username, salt=salt, hash=hash)

    # save to caregiver information to our database
    try:
        patient.save_to_db()
    except pymssql.Error as e:
        print("Failed to create user.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Failed to create user.")
        print(e)
        return
    print("Created user ", username)


def create_caregiver(tokens):
    # create_caregiver <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Failed to create user.")
        return

    username = tokens[1]
    password = tokens[2]
    # check 2: check if the username has been taken already
    if username_exists_caregiver(username):
        print("Username taken, try again!")
        return

    # check 3: check if the password is strong enough
    if isStrongPassword(password) is False:
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the caregiver
    caregiver = Caregiver(username, salt=salt, hash=hash)

    # save to caregiver information to our database
    try:
        caregiver.save_to_db()
    except pymssql.Error as e:
        print("Failed to create user.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Failed to create user.")
        print(e)
        return
    print("Created user ", username)


def isStrongPassword(password):
    # a. at least 8 characters
    if len(password) < 8:
        print("password should have at least 8 characters, try again!")
        return False

    # b. a mixture of both uppercase and lowercase letters
    has_uppercase = False
    has_lowercase = False
    for char in password:
        if char.isupper():
            has_uppercase = True
        elif char.islower():
            has_lowercase = True

    if not has_uppercase or not has_lowercase:
        print("password should be a mixture of both uppercase and lowercase letters, try again!")
        return False

    # c. a mixture of letters and numbers
    has_letter = False
    has_number = False
    for char in password:
        if char.isalpha():
            has_letter = True
        elif char.isdigit():
            has_number = True

    if not has_letter or not has_number:
        print("password should be a mixture of letters and numbers, try again!")
        return False

    # d. Inclusion of at least one special character, from "!","@", "#", "?"
    special_characters = ['!', '@', '#', '?']
    has_special_char = False
    for char in password:
        if char in special_characters:
            has_special_char = True
            break

    if not has_special_char:
        print("password should include at least one special character, from !, @, #, ?, try again!")
        return False

    # password meets all requirements
    return True


def username_exists_caregiver(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Caregivers WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when checking username")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def username_exists_patient(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Patients WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when checking username")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def login_patient(tokens):
    # login_patient <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_patient
    if current_caregiver is not None or current_patient is not None:
        print("User already logged in.")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Login failed.")
        return

    username = tokens[1]
    password = tokens[2]

    patient = None
    try:
        patient = Patient(username, password=password).get()
    except pymssql.Error as e:
        print("Login failed.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Login failed.")
        print("Error:", e)
        return

    # check if the login was successful
    if patient is None:
        print("Login failed.")
    else:
        print("Logged in as: " + username)
        current_patient = patient


def login_caregiver(tokens):
    # login_caregiver <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_caregiver
    if current_caregiver is not None or current_patient is not None:
        print("User already logged in.")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Login failed.")
        return

    username = tokens[1]
    password = tokens[2]

    caregiver = None
    try:
        caregiver = Caregiver(username, password=password).get()
    except pymssql.Error as e:
        print("Login failed.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Login failed.")
        print("Error:", e)
        return

    # check if the login was successful
    if caregiver is None:
        print("Login failed.")
    else:
        print("Logged in as: " + username)
        current_caregiver = caregiver


def search_caregiver_schedule(tokens):
    """
    TODO: Part 2
    """
    # not complete
    # search_caregiver_schedule <date>
    # check 1: check if the user's already logged in
    global current_caregiver
    global current_patient

    if current_caregiver is None and current_patient is None:
        print('Please login first!')
        return

    # check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again!")
        return
    # check 3: the format of date should be mm-dd-yyyy
    if len(tokens[1]) != 10:
        print("Please try again, your date format should be mm-dd-yyyy")
        return

    if tokens[1][2] != "-" or tokens[1][5] != "-":
        print("Please try again, your date format should be mm-dd-yyyy")
        return
    # assume input is hyphenated in the format mm-dd-yyyy
    date = tokens[1]
    # date_tokens = date.split("-")
    # month = int(date_tokens[0])
    # day = int(date_tokens[1])
    # year = int(date_tokens[2])
    # d = datetime.datetime(year, month, day)

    # first cursor
    cm = ConnectionManager()
    conn = cm.create_connection()

    available_caregiver = "SELECT Username FROM Availabilities WHERE Time = CONVERT(DATETIME,%s) ORDER BY Username"
    vaccine_detail = "SELECT * FROM Vaccines"
    try:
        cursor1 = conn.cursor()
        cursor1.execute(available_caregiver, date)
        for row in cursor1:
            print(row['Username'])
    except pymssql.Error as e:
        print("Error occurred")
        print("Db-Error:", e)
        quit()
    except:
        print("Please try again!")

    # second cursor
    cm = ConnectionManager()
    conn = cm.create_connection()
    try:
        cursor2 = conn.cursor(as_dict=True)
        cursor2.execute(vaccine_detail)
        for row in cursor2:
            print(row['Name'] + "" + row['Doses'])
            return
    except pymssql.Error as e:
        print("Error occurred")
        print("Db-Error:", e)
        quit()
    except:
        print("Please try again!")

    finally:
        cm.close_connection()
    return


def reserve(tokens):
    """
    TODO: Part 2
    """
    # make reservation, we need to add AppointmentID to Appointments table, and make the amount of vaccines -1
    # one caregiver can only make one dose a day, upload_availability already avoid this, so is fine
    # we need to delete availability, then generate AppointmentID and insert a row in Appointments
    # reserve <date> <vaccine>
    # check 1: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    # check 2: check if the user's already logged in
    if current_caregiver is None and current_patient is None:
        print("Please login first!")
        return

    # check 3: check if the user is patient
    if current_caregiver is not None and current_patient is None:
        print("Please login as a patient!")
        return

    # check 4: the format of date should be mm-dd-yyyy
    if len(tokens[1]) != 10:
        print("Please try again, your date format should be mm-dd-yyyy")
        return

    if tokens[1][2] != "-" or tokens[1][5] != "-":
        print("Please try again, your date format should be mm-dd-yyyy")
        return

    date = tokens[1]
    vaccine_name = tokens[2]
    assigned_caregiver = None
# First one
    cm = ConnectionManager()
    conn = cm.create_connection()
    selected_caregiver = "SELECT TOP 1 Username FROM Availabilities WHERE Time = CONVERT(DATETIME,%s) ORDER BY Username"
    try:
        cursor1 = conn.cursor()
        cursor1.execute(selected_caregiver, date)
        for row in cursor1:
            assigned_caregiver = row[0]

        # check if there's available caregiver
        if assigned_caregiver is None:
            print("No caregiver is available!")
            return

    except pymssql.Error as e:
        print("Error occurred")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Please try again!")
        print("Error:", e)
    finally:
        cm.close_connection()

# Second one
    cm = ConnectionManager()
    conn = cm.create_connection()
    get_doses = "SELECT Doses FROM Vaccines WHERE Name = %s"
    try:
        cursor2 = conn.cursor()
        cursor2.execute(get_doses, (vaccine_name))
        for row in cursor2:
            required_doses = row[0]

        # check if there's available doses
        # print(required_doses)
        if required_doses == 0 or required_doses is None:
            print("Not enough available doses!")
            return
    except pymssql.Error as e:
        print("Error occurred")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Please try again!")
        print("Error:", e)
    finally:
        cm.close_connection()

# Third one, get the latest number
    cm = ConnectionManager()
    conn = cm.create_connection()
    latest_number = "SELECT TOP 1 AppointmentID FROM Appointments Order by AppointmentID DESC"
    try:
        cursor3 = conn.cursor()
        cursor3.execute(latest_number)
        apptID_list = []
        for row in cursor3:
            apptID = int(row[0])
            apptID_list.append(apptID)
        if len(apptID_list) == 0:
            apptID = 0
        conn.commit()
    except pymssql.Error as e:
        print("Error occurred")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Please try again!")
        print("Error:", e)
    finally:
        cm.close_connection()

# Fourth one Delete Availabilities
    vaccine_obj = Vaccine(tokens[2], required_doses)
    cm = ConnectionManager()
    conn = cm.create_connection()
    delete_caregiver = "DELETE FROM Availabilities " \
                        "WHERE Username IN (SELECT TOP 1 Username FROM Availabilities WHERE Time = CONVERT(DATETIME,%s) ORDER BY Username) " \
                        "AND Time = CONVERT(DATETIME,%s)"
    try:
        cursor4 = conn.cursor()
        cursor4.execute(delete_caregiver, (date, date))
        conn.commit()
        apptID += 1
        vaccine_obj.decrease_available_doses(1)
        print('decrease vaccine')
    except pymssql.Error as e:
        print("Error occurred")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Please try again!")
        print("Error:", e)
    finally:
         cm.close_connection()

    print("Appointment ID:{}\nCaregiver username:{}".format(apptID, assigned_caregiver))

# Fifth one
    cm = ConnectionManager()
    conn = cm.create_connection()
    appt_query = "INSERT INTO Appointments VALUES (%s, %s, %s, %s, CONVERT(DATETIME,%s))"
    try:
        cursor5 = conn.cursor()
        cursor5.execute(appt_query, (apptID, current_patient.username, assigned_caregiver, vaccine_name, date))
        conn.commit()
    except pymssql.Error as e:
        print("Error occurred")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Please try again!")
        print("Error:", e)
    finally:
        cm.close_connection()
        print("appointment added!")


def upload_availability(tokens):
    #  upload_availability <date>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    # check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again!")
        return

    date = tokens[1]
    # assume input is hyphenated in the format mm-dd-yyyy
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])

    try:
        # make sure caregiver only available once in a day
        # cm = ConnectionManager()
        # conn = cm.create_connection()
        # cursor = conn.cursor()
        # check_availability = "SELECT * FROM Availabilities WHERE Username = %s AND Time = CONVERT(DATETIME,%s)"
        #
        # cursor = conn.cursor(as_dict=True)
        # cursor.execute(check_availability, (current_caregiver, date))
        # if cursor is not None:
        #     print("Caregiver can only be available a day")
        # else:
        d = datetime.datetime(year, month, day)
        current_caregiver.upload_availability(d)

    except pymssql.Error as e:
        print("Upload Availability Failed")
        print("Db-Error:", e)
        quit()
    except ValueError:
        print("Please enter a valid date!")
        return
    except Exception as e:
        print("Error occurred when uploading availability")
        print("Error:", e)
        return
    print("Availability uploaded!")


def cancel(tokens):
    """
    TODO: Extra Credit
    """
    # cancel < appointment_id >
    # check whether this apptID exists
    # safe the caregiver name and vaccine name before delete them
    # when patient cancel appointments, delete the Appointments on the AppointmentID,
    # the caregiver has the availabilities,
    # the vaccine which patient choose add one,
    #  check 1: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again!")
        return
    apptID = tokens[1]
    global current_caregiver
    global current_patient
# situation:caregiver login
    if current_caregiver is not None and current_patient is None:
        caregiver_name = current_caregiver.username
# first, check this apptID's existence
        cm = ConnectionManager()
        conn = cm.create_connection()
        check_appt_sql = "SELECT AppointmentID FROM Appointments WHERE AppointmentID = %s and C_Username = %s "
        try:
            cursor1 = conn.cursor()
            cursor1.execute(check_appt_sql, (apptID, caregiver_name))
            appt_list = []
            for row in cursor1:
                appt_list.append(row)
            if len(appt_list) == 0:
                print("There's no such AppointmentID or this username does not have permission to cancel this!")
                return
            else:
                print("AppointmentID existed")
        except pymssql.Error as e:
            print("Error occurred")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Please try again!")
            print("Error:", e)
        finally:
            cm.close_connection()

# Second, save caregiver_name, vaccine_name, and time
        cm = ConnectionManager()
        conn = cm.create_connection()
        save_name_sql = "SELECT V_Name, C_Username, Time FROM Appointments WHERE AppointmentID = %s and C_Username = %s "
        try:
            cursor2 = conn.cursor()
            cursor2.execute(save_name_sql, (apptID, caregiver_name))
            for row in cursor2:
                v_name = row[0]
                c_name = row[1]
                time = row[2]
                print("name saved")
        except pymssql.Error as e:
            print("Error occurred")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Please try again!")
            print("Error:", e)
        finally:
            cm.close_connection()

# Third, delete the Appointment
        cm = ConnectionManager()
        conn = cm.create_connection()
        delete_apptID_sql = "DELETE FROM Appointments WHERE AppointmentID = %s and C_Username = %s "
        try:
            cursor3 = conn.cursor()
            cursor3.execute(delete_apptID_sql, (apptID, caregiver_name))
            conn.commit()
            print("Appointment deleted")
        except pymssql.Error as e:
            print("Error occurred")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Please try again!")
            print("Error:", e)
        finally:
            cm.close_connection()

# fourth, add caregiver back
        cm = ConnectionManager()
        conn = cm.create_connection()
        add_caregiver_availability_sql = "INSERT INTO Availabilities VALUES (%s, %s) "
        try:
            cursor4 = conn.cursor()
            cursor4.execute(add_caregiver_availability_sql, (time, c_name))
            conn.commit()
            print("Availability added")
        except pymssql.Error as e:
            print("Error occurred")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Please try again!")
            print("Error:", e)
        finally:
            cm.close_connection()

# fifth, add doses back, and need to get current doses
        cm = ConnectionManager()
        conn = cm.create_connection()
        get_current_doses_sql = "SELECT Doses FROM Vaccines WHERE Name = %s "
        try:
            cursor5 = conn.cursor()
            cursor5.execute(get_current_doses_sql, v_name)
            for row in cursor5:
                current_doses = row[0]
            print("current_doses_get")
            vaccine_obj = Vaccine(v_name, current_doses)
            vaccine_obj.increase_available_doses(1)
            print("vaccine_doses_increased")
        except pymssql.Error as e:
            print("Error occurred")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Please try again!")
            print("Error:", e)
        finally:
            cm.close_connection()
# situation:patient login
    elif current_caregiver is None and current_patient is not None:
        patient_name = current_patient.username
        # first, check this apptID's existence
        cm = ConnectionManager()
        conn = cm.create_connection()
        check_appt_sql = "SELECT AppointmentID FROM Appointments WHERE AppointmentID = %s and P_Username = %s "
        try:
            cursor1 = conn.cursor()
            cursor1.execute(check_appt_sql, (apptID, patient_name))
            appt_list = []
            for row in cursor1:
                appt_list.append(row)
            if len(appt_list) == 0:
                print("There's no such AppointmentID or this username does not have permission to cancel this!")
                return
            else:
                print("AppointmentID existed")
        except pymssql.Error as e:
            print("Error occurred")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Please try again!")
            print("Error:", e)
        finally:
            cm.close_connection()

        # Second, safe caregiver_name, vaccine_name, and time
        cm = ConnectionManager()
        conn = cm.create_connection()
        save_name_sql = "SELECT V_Name, C_Username, Time FROM Appointments WHERE AppointmentID = %s and P_Username = %s "
        try:
            cursor2 = conn.cursor()
            cursor2.execute(save_name_sql, (apptID, patient_name))
            for row in cursor2:
                v_name = row[0]
                c_name = row[1]
                time = row[2]
                print("name saved")
        except pymssql.Error as e:
            print("Error occurred")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Please try again!")
            print("Error:", e)
        finally:
            cm.close_connection()

        # Third, delete the Appointment
        cm = ConnectionManager()
        conn = cm.create_connection()
        delete_apptID_sql = "DELETE FROM Appointments WHERE AppointmentID = %s and P_Username = %s "
        try:
            cursor3 = conn.cursor()
            cursor3.execute(delete_apptID_sql, (apptID, patient_name))
            conn.commit()
            print("Appointment deleted")
        except pymssql.Error as e:
            print("Error occurred")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Please try again!")
            print("Error:", e)
        finally:
            cm.close_connection()

        # fourth, add caregiver back
        cm = ConnectionManager()
        conn = cm.create_connection()
        add_caregiver_availability_sql = "INSERT INTO Availabilities VALUES (%s, %s) "
        try:
            cursor4 = conn.cursor()
            cursor4.execute(add_caregiver_availability_sql, (time, c_name))
            conn.commit()
            print("Availability added")
        except pymssql.Error as e:
            print("Error occurred")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Please try again!")
            print("Error:", e)
        finally:
            cm.close_connection()

        # fifth, add doses back, and need to get current doses
        cm = ConnectionManager()
        conn = cm.create_connection()
        get_current_doses_sql = "SELECT Doses FROM Vaccines WHERE Name = %s "
        try:
            cursor5 = conn.cursor()
            cursor5.execute(get_current_doses_sql, v_name)
            for row in cursor5:
                current_doses = row[0]
            print("current_doses_get")
            vaccine_obj = Vaccine(v_name, current_doses)
            vaccine_obj.increase_available_doses(1)
            print("vaccine_doses_increased")
        except pymssql.Error as e:
            print("Error occurred")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Please try again!")
            print("Error:", e)
        finally:
            cm.close_connection()
    else:
        print("Please login first!")
        return

def add_doses(tokens):
    #  add_doses <vaccine> <number>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    #  check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    vaccine_name = tokens[1]
    doses = int(tokens[2])
    vaccine = None
    try:
        vaccine = Vaccine(vaccine_name, doses).get()
    except pymssql.Error as e:
        print("Error occurred when adding doses")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when adding doses")
        print("Error:", e)
        return

    # if the vaccine is not found in the database, add a new (vaccine, doses) entry.
    # else, update the existing entry by adding the new doses
    if vaccine is None:
        vaccine = Vaccine(vaccine_name, doses)
        try:
            vaccine.save_to_db()
        except pymssql.Error as e:
            print("Error occurred when adding doses")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Error occurred when adding doses")
            print("Error:", e)
            return
    else:
        # if the vaccine is not null, meaning that the vaccine already exists in our table
        try:
            vaccine.increase_available_doses(doses)
        except pymssql.Error as e:
            print("Error occurred when adding doses")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Error occurred when adding doses")
            print("Error:", e)
            return
    print("Doses updated!")


def show_appointments(tokens):
    '''
    TODO: Part 2
    '''
    # show_appointments
    #  check 1: the length for tokens need to be exactly 1
    if len(tokens) != 1:
        print("Please try again!")
        return

    # check 2: check if the user's already logged in
    global current_caregiver
    global current_patient

    if current_caregiver is None and current_patient is None:
        print('Please login first!')
        return

    cm = ConnectionManager()
    conn = cm.create_connection()

    if current_caregiver is not None:

        appt_info_for_caregivers = "SELECT AppointmentID, V_name AS vaccine_name , Time AS date , P_Username AS patient_name " \
                                   "FROM Appointments " \
                                   "WHERE C_Username = %s " \
                                   "ORDER BY AppointmentID"
        try:
            cursor1 = conn.cursor()
            cursor1.execute(appt_info_for_caregivers, (current_caregiver.username))
            for row in cursor1:
                print(row[0], "", row[1], "", row[2], "", row[3])
            return
        except pymssql.Error as e:
            print("Error occurred")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Please try again!")
            print("Error:", e)
        finally:
            cm.close_connection()
    else:

        appt_info_for_patients = "SELECT AppointmentID, V_name AS vaccine_name, Time AS date, C_Username AS caregiver_name " \
                                 "FROM Appointments " \
                                 "WHERE P_Username = %s " \
                                 "ORDER BY AppointmentID"
        try:
            cursor2 = conn.cursor()
            cursor2.execute(appt_info_for_patients,(current_patient.username))
            for row in cursor2:
                print(row[0], "", row[1], "", row[2], "", row[3])
            return
        except pymssql.Error as e:
            print("Error occurred")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Please try again!")
            print("Error:", e)
        finally:
            cm.close_connection()


def logout(tokens):
    """
    TODO: Part 2
    """
    global current_caregiver
    global current_patient
    try:
        if current_caregiver is None and current_patient is None:
            print("You are not logged in, stupid! Plz login first!")
            return
        elif current_caregiver is not None:
            current_caregiver = None
            print("Bye Bye, beauty caregiver, ur logout")
            return
        else:
            current_patient = None
            print("Bye Bye, beauty patient, ur logout")
            return
    except:
        print("There's other error, plz try again!")
        return


def start():
    stop = False
    print()
    print(" *** Please enter one of the following commands *** ")
    print("> create_patient <username> <password>")  # //TODO: implement create_patient (Part 1)
    print("> create_caregiver <username> <password>")
    print("> login_patient <username> <password>")  # // TODO: implement login_patient (Part 1)
    print("> login_caregiver <username> <password>")
    print("> search_caregiver_schedule <date>(mm-dd-yyyy)")  # // TODO: implement search_caregiver_schedule (Part 2)
    print("> reserve <date> <vaccine>")  # // TODO: implement reserve (Part 2)
    print("> upload_availability <date>(mm-dd-yyyy)")
    print("> cancel <appointment_id>")  # // TODO: implement cancel (extra credit)
    print("> add_doses <vaccine> <number>")
    print("> show_appointments")  # // TODO: implement show_appointments (Part 2)
    print("> logout")  # // TODO: implement logout (Part 2)
    print("> Quit")
    print()
    while not stop:
        response = ""
        print("> ", end='')

        try:
            response = str(input())
        except ValueError:
            print("Please try again!")
            break

        response = response.lower()
        tokens = response.split(" ")
        if len(tokens) == 0:
            ValueError("Please try again!")
            continue
        operation = tokens[0]
        if operation == "create_patient":
            create_patient(tokens)
        elif operation == "create_caregiver":
            create_caregiver(tokens)
        elif operation == "login_patient":
            login_patient(tokens)
        elif operation == "login_caregiver":
            login_caregiver(tokens)
        elif operation == "search_caregiver_schedule":
            search_caregiver_schedule(tokens)
        elif operation == "reserve":
            reserve(tokens)
        elif operation == "upload_availability":
            upload_availability(tokens)
        elif operation == "cancel":
            cancel(tokens)
        elif operation == "add_doses":
            add_doses(tokens)
        elif operation == "show_appointments":
            show_appointments(tokens)
        elif operation == "logout":
            logout(tokens)
        elif operation == "quit":
            print("Bye!")
            stop = True
        else:
            print("Invalid operation name!")


if __name__ == "__main__":
    '''
    // pre-define the three types of authorized vaccines
    // note: it's a poor practice to hard-code these values, but we will do this ]
    // for the simplicity of this assignment
    // and then construct a map of vaccineName -> vaccineObject
    '''

    # start command line
    print()
    print("Welcome to the COVID-19 Vaccine Reservation Scheduling Application!")

    start()