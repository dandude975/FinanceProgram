import random
import time
import math
import mysql.connector
import os
import tempfile
import subprocess
from subprocess import run
import Functions


def logInFunction():
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


def logOff():
    mydb.close()
    return None


def createUser():  # Creating the user
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
    try:  # Connecting to SQL database with admin privilidges to create user
        global mydb
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
        )
    except:
        print("Error code 1001")
        exit()
    else:
        logIn = True
        global mycursor
        mycursor = mydb.cursor()
        mycursor.execute("CREATE USER '" + User + "'@'localhost' IDENTIFIED BY '" + Pass + "';")  # Creating user
        mycursor.execute("CREATE ROLE CUSTOMER;")
        mycursor.execute("GRANT ALTER,CREATE,DELETE,DROP,INSERT,REFERENCES,RELOAD,SELECT,CREATE TABLESPACE,UPDATE on"
                         "*.* to 'CUSTOMER';")
        mycursor.execute("GRANT 'CUSTOMER' to '"+User+"'@'localhost';")
        mycursor.execute("SET DEFAULT ROLE 'CUSTOMER' to '"+User+"'@'localhost';")
        logOff()
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
access = False
while not access:
    print("Log in or Sign up?")
    x = input("(L/S): ")
    if x.lower() == "l":
        logInFunction()
        access = True
    elif x.lower() == "s":
        createUser()
        access = True
    else:
        print("nope")

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
