import random
import time
import math
import mysql.connector
import os
import tempfile
import subprocess
from subprocess import run
import Functions


def logIn():
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
                database="FinanceRecords"
            )
        except:
            print("Incorrect username or password\n")
        else:
            logIn = True
            username = Uname
            password = Pword
            global mycursor
            mycursor = mydb.cursor()
    return None


def logOff():
    mydb.close()
    return None


def createUser():
    confirmed = False
    while not confirmed:
        User = input("Enter username: ")
        Pass = input("Enter password:")
        checkPass = input("Confirm password: ")
        if Pass == checkPass:
            print()
            confirmed = True
        else:
            print("Passwords do not match")
    statement = "CREATE USER '" + User + "'@'localhost' IDENTIFIED BY '" + Pass + "'"
    mycursor.execute(statement)
    print("Welcome", User)
    mycursor.execute("CREATE DATABASE FinanceRecords")
    logOff()
    return logIn()


print("Hello and welcome to Omega Financial Services")
print("A company by RETIS Engineering")
print()
access = False
while not access:
    print("Log in or Sign up?")
    x = input("(L/S): ")
    if x.lower == 'l':
        logIn()
        access = True
    elif x.lower == 's':
        createUser()
        access = True
    else:
        print()

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
