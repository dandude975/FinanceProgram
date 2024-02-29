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
import tkinter as tk
from tkinter import *
from tkinter import ttk
from PyQt5.QtWidgets import QApplication, QLabel


  # FUTURE DAN!!!! Your next task is to migrate this entire program from Tkinter which is useless to PyQt5


def handle_keypress(event):
    global frm
    frm.destroy()
    frm = ttk.Frame(window, padding=25)
    frm.grid()
    button1 = tk.Button(frm, text="Click here to view recover key. ", command=startUp()).grid(column=0, row=0)
    label1 = tk.Label(frm, text="This is used for resetting this application.").grid(column=0, row=1)
    label2 = tk.Label(frm, text="\n").grid(column=0, row=2)
    label3 = tk.Label(frm, text="WARNING LOSS OF RECOVERY KEY WILL RESULT IN COMPLETE LOSS OF ACCESS").grid(column=0,row=3)


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

        root = Tk()
        frm = ttk.Frame(root, padding=25)
        frm.grid()
        ttk.Label(frm, text="Recovery key: ").grid(column=0, row=0)
        ttk.Label(frm, text=secure).grid(column=0, row=1)
        ttk.Button(frm, text="I have written down the key", command=lambda:[root.destroy(),window.destroy()].grid(column=0, row=2))
        root.mainloop()
        window.mainloop()
        mycursor.execute("ALTER USER 'root'@'localhost' IDENTIFIED BY '" + secure + "';")
        mycursor.execute("ALTER USER 'admin'@'localhost' IDENTIFIED BY '" + secure + "';")
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

window = Tk()
window.title("Omega Financial Services")
frm = ttk.Frame(window, padding=25)
frm.grid()
label1 = tk.Label(frm, text="Hello and welcome to Omega Financial Services").grid(column=0, row=0)
label2 = tk.Label(frm, text="A company by RETIS Software Inc").grid(column=0, row=1)
label3 = tk.Label(frm, text="\n").grid(column=0, row=2)
label4 = tk.Button(frm, text="Press 'J' to continue").grid(column=0, row=3)\

window.bind("j", handle_keypress)

window.mainloop()
print()
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
