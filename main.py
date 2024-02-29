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
from tkinter import *
from tkinter import ttk

def startUp():
    try:  # If the program can access the root user with defaults, then it will initiate 'first time' procedures.
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
        )
        mycursor = mydb.cursor()
        mycursor.execute("CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin';")  # Creating admin user
        mycursor.execute("GRANT ALL PRIVILEGES on *.* to 'admin'@'localhost'WITH GRANT OPTION;")  # Setting admin permissions
    except:
        mydb.close()
        return None
    else:
        length = 12
        chars = string.ascii_letters + string.digits + '!@#$%^*&~:¬`'
        random.seed = (os.urandom(1024))
        secure = ''.join(random.choice(chars) for i in range(length))

        print("Press enter to view recover key. This is used for resetting this application.")
        print("WARNING LOSS OF RECOVERY KEY WILL RESULT IN COMPLETE LOSS OF ACCESS")
        input("[Enter]")
        root = Tk()
        frm = ttk.Frame(root, padding=25)
        frm.grid()
        ttk.Label(frm, text="Recovery key: ").grid(column=0, row=0)
        ttk.Label(frm, text=secure).grid(column=0, row=1)
        ttk.Button(frm, text="I have written down the key", command=root.destroy).grid(column=0, row=2)
        root.mainloop()
        mycursor.execute("ALTER USER 'root'@'localhost' IDENTIFIED BY '" + secure + "';")
        mycursor.execute("ALTER USER 'admin'@'localhost' IDENTIFIED BY '" + secure + "';")
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        mydb.close()

        mydb = mysql.connector.connect(
            host="localhost",
            user="admin",
            password=secure,
        )
        mycursor = mydb.cursor()

        mycursor.execute("CREATE ROLE CUSTOMER;")
        mycursor.execute("GRANT ALTER,CREATE,DELETE,DROP,INSERT,REFERENCES,RELOAD,SELECT,CREATE TABLESPACE,UPDATE on"
                         "*.* to 'CUSTOMER';")
        confirmed = False
        while not confirmed:
            print("Create an account\n")
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
        mycursor.execute("CREATE DATABASE FinanceRecords")  # Creating database
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

main = Tk()
frm = ttk.Frame(main, padding=25)
frm.grid()
introA = ttk.Label(frm, text="Hello and welcome to Omega Financial Services").grid(column=0, row=0)
intorB = ttk.Label(frm, text="A company by RETIS Software Inc").grid(column=0, row=1)
space = ttk.Label(frm, text="\n").grid(column=0, row=2)
loading = ttk.Label(frm, text="Loading...").grid(column=0, row=3)
time.sleep(5)
loading.delete()
text = ttk.Label(frm, text="Please log in:").grid(column=0, row=3)
main.mainloop()


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
