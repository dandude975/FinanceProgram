import random
import string
import time
import math
import mysql.connector
import os
import tempfile
import subprocess
from subprocess import run
import Functions

def startUp():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
    )
    mycursor = mydb.cursor()
    try:
        mycursor.execute("CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin';")  # Creating admin user
        mycursor.execute("GRANT ALL PRIVILEGES on *.* to 'admin'@'localhost'WITH GRANT OPTION;")  # Setting admin permissions
    except:
        mydb.close()
        firstTimeAccess = False
    else:
        firstTimeAccess = True
        length = 12
        chars = string.ascii_letters + string.digits + '!@#$%^*&~:¬`'
        random.seed = (os.urandom(1024))
        global secure
        secure = ''.join(random.choice(chars) for i in range(length))

        print("Press enter to view recover key. This is used for resetting this application.")
        print("WARNING LOSS OF RECOVERY KEY WILL RESULT IN COMPLETE LOSS OF ACCESS")
        input("[Enter]")
        print("Recovery key: " + secure)
        mycursor.execute("ALTER USER 'root'@'localhost' IDENTIFIED BY '" + secure + "';")
        mycursor.execute("ALTER USER 'admin'@'localhost' IDENTIFIED BY '" + secure + "';")
        input("[Press enter to confirm you have made not of you recovery code]")
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        mydb.close()

    mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password=secure,
    )
    mycursor = mydb.cursor()

    if firstTimeAccess == True:
        mycursor.execute("CREATE ROLE CUSTOMER;")
        mycursor.execute("GRANT ALTER,CREATE,DELETE,DROP,INSERT,REFERENCES,RELOAD,SELECT,CREATE TABLESPACE,UPDATE on"
                         "*.* to 'CUSTOMER';")
        confirmed = False
        while not confirmed:
            User = input("Enter username: ")
            Pass = input("Enter password:")
            checkPass = input("Confirm password: ")
            if Pass == checkPass:  # Check that passwords match
                print()
                confirmed = True
            else:
                print("Passwords do not match")
        mycursor.execute("CREATE USER '" + User + "'@'localhost' IDENTIFIED BY '" + Pass + "';")  # Creating user
        mycursor.execute("GRANT 'CUSTOMER' to '" + User + "'@'localhost';")
        mycursor.execute("SET DEFAULT ROLE 'CUSTOMER' to '" + User + "'@'localhost';")
        logOff()
        mydb.close()
        return None
    else:
        mydb.close()
        return None



def logInFunction():  # Function to log into the program
    global mycursor
    global mydb
    logIn = False
    while not logIn:
        print("Please log in:")
        Uname = input("Username: ")
        Pword = input("Password: ")
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user=Uname,
                password=Pword,
                database="financerecords"
            )
        except:
            print("Incorrect username or password\n")
        else:
            logIn = True
            username = Uname
            password = Pword
            global mycursor
            mycursor = mydb.cursor()
            print("Welcome", Uname)
    return None


def logOff():  # Function to log out of the system
    mydb.close()
    return None


def createUser():  # Creating the user

    try:  # Connecting to SQL database with admin privilidges to create user and set user permissions
        global mydb
        mydb = mysql.connector.connect(
            host="localhost",
            user="admin",
            password=secure,
        )
    except:
        print("Error code 1001")
        exit()
    else:
        logIn = True
        global mycursor
        mycursor = mydb.cursor()

        mydb = mysql.connector.connect(
            host="localhost",
            user=User,
            password=Pass,
        )
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE FinanceRecords")  # Creating database
        logOff()
    logInFunction()
    return None


print("Hello and welcome to Omega Financial Services")
print("A company by RETIS Software Inc")
print()
startUp()
access = False
while not access:
    print("Please log in:")
    logInFunction()
    access = True

print("\nRecorded years:")
mycursor.execute("SHOW TABLES")

for x in mycursor:
    print('-'+x[0])
print()
print("Please choose a year to view/modify or type 'back' to quit the program")
table = input()
mycursor.execute("SHOW TABLES")
for x in mycursor:
    if (x[0]) == table:
        print()
        options(table)
    elif table.upper() == "BACK":
        Functions.logOff()
        exit()
print("Create table?")
create = input("y/n ")
if create == "y":
    mycursor.fetchall()
    createTable(table)
