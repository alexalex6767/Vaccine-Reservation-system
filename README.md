# Vaccine-Reservation-system
This is a project-like assignment from UW CSE414. It is completed by Charlene Tang(https://github.com/CharleneTang1215) and I. 


HW 6 | Appointment Reservation System 
Objectives: To gain experience with database application development, and learn how to use SQL from within Python via pymssql.
Contents:
Introduction
Setup 
Requirements
Part 1 
Part 2 

Introduction
A common type of application that connects to a database is a reservation system, where users schedule time slots for some centralized resource. I will program part of an appointment scheduler for vaccinations, where the users are patients and caregivers keeping track of vaccine stock and appointments.
This application will run on the command line terminal, and connect to a database server created with Microsoft Azure account.

Setup
2.1 Clone the starter code
Navigate to the Github repository hosting the starter code: 
https://github.com/aaditya1004/vaccine-scheduler-python (As you continue to work on the assignment, DO NOT manipulate the internal project structure of the assignment. This will save you some headache when it comes time to submit your code)

Click on the green button “Code” and select “Download ZIP” from the drop-down menu.

Once your download completes, decompress the ZIP file and retrieve the starter code.

2.2 Read through the starter code
We created the important folders and files you will be using to build your application:
src.main.scheduler/
Scheduler.py: 
This is the main entry point to the command-line interface application. Once you compile and run Scheduler.py, you should be able to interact with the application.
db/:
This is a folder holding all of the important components related to your database.
ConnectionManager.py: This is a wrapper class for connecting to the database. Read more in 2.3.4. You should run this document to connect to the database so you can successfully interact with the application.
model/:
This is a folder holding all the class files for your data model.
You should implement all classes for your data model (e.g., patients, caregivers) in this folder. We have created implementations for Caregiver and Vaccines, and you need to complete the Patient class (which can heavily borrow from Caregiver. Feel free to define more classes or change our implementation if you want! 
src.main.resources/
create.sql: SQL create statements for your tables, we have included the create table code for our implementation. You should copy, paste, and run the code (along with all other create table statements) in your Azure Query Editor.

2.3 Configure your database connection
2.3.1 Installing dependencies and anaconda
Our application relies on a few dependencies and external packages. You’ll need to install those dependencies to complete this assignment.

We will be using Python SQL Driver pymssql to allow our Python application to connect to an Azure database. We recommend using Anaconda for completing this assignment. 

Mac users, follow the instructions in the link to install Anaconda on macOS: https://docs.anaconda.com/anaconda/install/mac-os/

Windows users, follow the instructions in the link to install Anaconda on Windows: https://docs.anaconda.com/anaconda/install/windows/. You can choose to install Pycharm for Anaconda, but we recommend installing Anaconda without PyCharm as we will be using the terminal.

After installing Anaconda:
We first need to create a development environment in conda.
macOS users: launch terminal and navigate to your source directory.
Windows users: launch “Anaconda Prompt” and navigate to your source directory.
Follow the steps here to create an environment. Make sure you remember the name of your environment.
Run: conda create -n [environment name]
Activate your environment following the steps here. 
Run: conda activate [environment name]
To deactivate, Run: conda deactivate
Run “conda install pymssql” to install the dependencies.
Disclaimer: You don’t need to put the file you downloaded in Step 2.1 into the environment folder. You can leave it wherever you downloaded. 

2.3.3 Setting up credentials
The first step is to retrieve the information to connect to your Microsoft Azure Database.
The Server and DB names can be found in the Azure portal. 
The server name would be “data514server.database.windows.net”. However, for step 2.3.3 Setting up environment variables, you’ll only need to put in the phrase before “.database.windows.net”. In the screenshot below, it would be just “data514server” for the server in step 2.3.3 Setting up environment variables. 
The database name would be “data514db” for the database shown in the screenshot below. 
YOU NEED TO CHANGE THIS ACCORDING TO YOUR DATABASE!
The User ID would be of the format <user id>@<server name> 
For example, it could be exampleUser@data514server where “exampleUser” is the login ID which you used to log in to query editor on Azure and “data514server” is the server name.
Password is what you used to log in to your query editor on the Azure portal.
If you’re having trouble finding that information, please make a discussion post, or contact us through email!

Once you’ve retrieved the credentials needed, you can set up your environment variables. 
2.3.3 Setting up environment variables 
Make sure to set this in the environment you created if you’re using virtual environments! Remember, to go into the environment you created, you’ll need to activate it. 
In your terminal or Anaconda Prompt, type the following:
conda env config vars set Server={}
conda env config vars set DBName={}
conda env config vars set UserID={}
conda env config vars set Password={}


Where “{}” is replaced by the respective information you retrieved from step.
You will need to reactivate your environment after that with just the command “conda activate [environment name]”. Don’t do conda deactivate before this
2.3.4 Working with the connection manager
In scheduler.db.ConnectionManager.py, we have defined a wrapper class to help you instantiate the connection to your SQL Server database. You’ll need to run this document to connect to your database: Run “python ConnectionManager.py”. 
We recommend reading about pymssql Connection and Cursor classes for retrieving and updating information in your database.
Here’s an example of using ConnectionManager.
# instantiating a connection manager class and cursor
cm = ConnectionManager()
conn = cm.create_connection()
cursor = conn.cursor()


# example 1: getting all names and available doses in the vaccine table
get_all_vaccines = "SELECT Name, Doses FROM vaccines"
try:
    cursor.execute(get_all_vaccines)
    for row in cursor:
        print(name:" + str(row[‘Name’]) + ", available_doses: " + str(row[‘Doses’]))
except pymssql.Error:     
    print(“Error occurred when getting details from Vaccines”)

# example 2: getting all records where the name matches “Pfizer”
get_pfizer = "SELECT * FROM vaccine WHERE name = %s"
try:
    cursor.execute(get_pfizer)
    for row in cursor:
        print(name:" + str(row[‘Name’]) + ", available_doses: " + str(row[‘Doses’]))
except pymssql.Error:     
    print(“Error occurred when getting pfizer from Vaccines”)


2.4 Verify your setup
Once you’re done with everything, try to run the program and you should see the following output. You should be running the program in terminal (macOS) or Anaconda Prompt (Windows) and in your conda environment. 
Note: Command to run the program: “python Scheduler.py” or “python3 Scheduler.py”.
Welcome to the COVID-19 Vaccine Reservation Scheduling Application!
*** Please enter one of the following commands ***
> create_patient <username> <password>
> create_caregiver <username> <password>
> login_patient <username> <password>
> login_caregiver <username> <password>
> search_caregiver_schedule <date>
> reserve <date> <vaccine>
> upload_availability <date>
> cancel <appointment_id>
> add_doses <vaccine> <number>
> show_appointments
> logout
> quit


If you can see the list of options above, congratulations! You have verified your local setup.

Next, to verify that you have set up your database connection correctly, try to create a caregiver with the command “create_caregiver <username> <password>”. Make sure you have created the tables on Azure before testing this command.



Requirements
Build a vaccine scheduling application (with a database hosted on Microsoft Azure) that can be deployed by hospitals or clinics and supports interaction with users through the terminal/command-line interface. In the real world it is unlikely that users would be using the command line terminal instead of a GUI, but all of the application logic would remain the same. For simplicity of programming, we use the command line terminal as our user interface for this assignment.
We need the following entity sets in our database schema design (hint: you should probably be defining your class files based on this!):
Patients: these are customers that want to receive the vaccine.
Caregivers: these are employees of the health organization administering the vaccines.
Vaccines: these are vaccine doses in the health organization’s inventory of medical supplies that are on hand and ready to be given to the patients.
In this assignment, you will need to:
Complete the design of the database schema, with an E/R diagram and table statements (Part 1);
Implement the missing functionality from the application (Part 1 & Part 2)



A few things to note:
You should handle invalid inputs gracefully. For example, if the user types a command that doesn’t exist, it is bad to immediately terminate the program. A better design would be to give the user some feedback and allow them to re-type the command. Points will be taken off if the program terminates immediately after receiving invalid input. While you don’t have to consider all possible inputs, error handling for common errors (e.g., missing information, wrong spelling) should be considered.
After executing a command, you should re-route the program to display the list of commands again. For example:
If a patient ‘reserves’ their vaccine for a date, you should update your database to reflect this information and route the patient back to the menu again.

1.3 How to handle passwords
You should never directly store any password in the database. Instead, we'll be using a technique called salting and hashing. In cryptography, salting hashes refer to adding random data to the input of a hash function to guarantee a unique output. We will store the salted password hash and the salt itself to avoid storing passwords in plain text. Use the following code snippet as a template for computing the hash given a password string:

import hashlib
import os
# Generate a random cryptographic salt
salt = os.urandom(16)
# Generate the hash
hash = hashlib.pbkdf2_hmac(
   'sha256',
   password.encode('utf-8'),
   salt,
   100000,
   dklen=16
)


Part 1
Design
You will first need to work on the design of your database application. Before you begin, please carefully read the assignment specification (including Part 2) and the starter code, and think about what tables would be required to support the required operations. Once you have an idea of how you want to design your database schema:
Draw the ER diagram of your design and place it under src.main.resources (design.pdf).
Write the create table statements for your design, create the tables on Azure, and save the code under src.main.resources (create.sql).
You will also need to implement the corresponding Python classes of your design. We have implemented Caregiver.py for you, but feel free to change any of the details. You will need the following classes, and you may implement more data models if you feel the necessity:
Caregiver.py: data model for caregivers (implemented for you.)
Vaccine.py: data model for vaccines (implemented for you.)
Patient.py: data model for patients.
You will implement this class, it can be mostly based on Caregiver.py
Implementation
Congratulations! You’re now ready to implement your design! For Part 1, you will need to implement the following functionalities. It is up to you to decide how you want the user to interact with your system. TAs will be interacting with your command-line interface, and we will give credits to all reasonable designs, so don’t worry too much about the details.
We have implemented account creation for caregivers as an example for you, please read through our implementation before you begin.

You’re allowed to choose your own messages to display, but please make sure to supply enough information to the user regarding specific situations (e.g., when create failed). Refer to our implementation as an example.

You will need to implement the following operations:
create_patient <username> <password>
Print "Created user {username}" if create was successful.
If the username is already taken, print “Username taken, try again!”.
For all other errors, print “Failed to create user.”.
login_patient <username> <password>
If a user is already logged in in the current session, you need to log out first before logging in again. In this case, print “User already logged in.”.
For all other errors, print "Login failed.". Otherwise, print 
"Logged in as: [username]".


Part 2
For most of the operations mentioned below, Your program will need to do some checks to ensure that the appointment can be reserved (e.g., whether the vaccine still has available doses). Again, you do not have to cover all of the unexpected situations, but we do require you to have a reasonable amount of checks (especially the easy ones).

For Part 2, you will need to implement the following operations:
search_caregiver_schedule <date>
Both patients and caregivers can perform this operation.
Output the username for the caregivers that are available for the date, along with the number of available doses left for each vaccine. Order by the username of the caregiver. Separate each attribute with a space.
If no user is logged in, print “Please login first!”.
For all other errors, print "Please try again!".
reserve <date> <vaccine>
Patients perform this operation to reserve an appointment.
Caregivers can only see a maximum of one patient per day, meaning that if the reservation went through, the caregiver is no longer available for that date.
If there are available caregivers, choose the caregiver by alphabetical order and print “Appointment ID: {appointment_id}, Caregiver username: {username}” for the reservation.
If there’s no available caregiver, print “No Caregiver is available!”. If not enough vaccine doses are available, print "Not enough available doses!".
If no user is logged in, print “Please login first!”. If the current user logged in is not a patient, print “Please login as a patient!”.
For all other errors, print "Please try again!".
show_appointments
Output the scheduled appointments for the current user (both patients and caregivers). 
For caregivers, you should print the appointment ID, vaccine name, date, and patient name. Order by the appointment ID. Separate each attribute with a space.
For patients, you should print the appointment ID, vaccine name, date, and caregiver name. Order by the appointment ID. Separate each attribute with a space.
If no user is logged in, print “Please login first!”.
For all other errors, print "Please try again!".
Logout
If not logged in, you should print “Please login first.”. Otherwise, print “Successfully logged out!”.
For all other errors, print "Please try again!".




Optional
You can do either one of the following extra tasks by the final due date for 10 extra credit points.

Add guidelines for strong passwords. In general, it is advisable that all passwords used to access any system should be strong. Add the following check to only allow strong passwords:
At least 8 characters.
A mixture of both uppercase and lowercase letters.
A mixture of letters and numbers.
Inclusion of at least one special character, from “!”, “@”, “#”, “?”.
Both caregivers and patients should be able to cancel an existing appointment. Implement the cancel operation for both caregivers and patients. Hint: both the patient’s schedule and the caregiver’s schedule should reflect the change when an appointment is canceled.
> cancel <appointment_id>



