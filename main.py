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

# FUTURE DAN!!!! Your next task is to migrate this entire program from text which is useless to PyQt5


class income():
    def __init__(self):
        answers = False
        while not answers:
            date = []
            name = input("Income name: ")
            print("Per instance, what is the amount of the income (gross)")
            amount = input("GBP: ")
            print("What frequency does this income come in?")
            frequency = input("Annually (A), Quarterly (Q), Monthly (M), Weekly (W): ")
            print("What type of income is this?")
            type = input("Salaried Employment (Es), Hourly Employment (Eh), "
                         "Benifits (B), Self-Employment/Contractor (C), or "
                         "Dividends (D)")
            if frequency.lower() != 'w':
                print("What date does this income come in on?")
                day = input("1st - 28th (please only type the number): ")
                answers2 = False
                while not answers2:
                    if frequency.lower() == 'a':
                        print("What month does this income come in on?")
                        month = input("1 - 12 (please only type the number); ")
                        date.append(int(month))
                        answers2 = True
                    elif frequency.lower() == 'q':
                        print("What is the first month of the (tax) year that income comes in on?")
                        month = input("1 - 12 (please only type the number); ")
                        date.append(int(month))
                        answers2 = True
                    elif frequency.lower() == 'm':
                        if int(day) >= 6:
                            date.append(3)
                        if int(day) < 6:
                            date.append(4)
                        answers2 = True
                    elif frequency.lower() == 'w':
                        date.append(00)
                        answers2 = True
                    else:
                        print("Please enter answers in the correct format")
                date.append(int(day))
                self.recordAdder(name, str(type.lower()), amount, frequency, date)
                print("Record added")
                break
                return None
            elif frequency.lower() == 'w':
                print("What day does this income come in on?")
                day = input("1 - 7 (please only type the number): ")
                date.append(0)
                date.append(int(day))
                self.recordAdder(name, str(type.lower()), amount, frequency, date)
                print("\n")
                print("Record added")
                break
                return None
            else:
                print("Please enter answers in the correct format")

    def recordAdder(self, name, type, amount, frequency, date):
        print("Please confirm details of bill:")
        print()
        print("Income name:", name)
        print("Income amount per instance: ", str(amount) + " GBP")
        if frequency == 'a':
            print("Income frequency: Annually")
        elif frequency == 'q':
            print("Income frequency: Quarterly")
        elif frequency == 'm':
            print("Income frequency: Monthly")
        elif frequency == 'w':
            print("Income frequency: Weekly")
        print("Income dates for current year:")
        if frequency == 'a':
            print(" - ", self.dateDisplay(date))
            print("Total per year: ", amount, "GBP")
            add = ("INSERT INTO Income (Name, type,  Amount, Day, Month)"
                   "VALUES (%s, %s, %s, %s, %s)")
            data = (str(name), str(type), str(amount), str(date[1]), str(date[0]))
            mycursor.execute(add, data)
            mydb.commit()
        elif frequency == 'q':
            print(" - ", self.dateDisplay(date))
            for i in range(0,3):
                date[0] = date[0] + 3
                print(" - ", self.dateDisplay(date))
                add = ("INSERT INTO Income (Name, Type, Amount, Day, Month)"
                       "VALUES (%s, %s, %s, %s, %s)")
                data = (str(name), str(type), str(amount), str(date[1]), str(date[0]))
                mycursor.execute(add, data)
                mydb.commit()
            print("Total per year: ", float(amount)*4, "GBP")
        elif frequency == 'm':
            for i in range(0, 12):
                date[0] = date[0] + 1
                print(" - ", self.dateDisplay(date))
                add = ("INSERT INTO Income (Name, Type, Amount, Day, Month)"
                       "VALUES (%s, %s, %s, %s, %s)")
                data = (str(name), str(type), str(amount), str(date[1]), str(date[0]))
                mycursor.execute(add, data)
                mydb.commit()
            print("Total per year: ", float(amount)*12, "GBP")
        elif frequency == 'w':
            print("Average total per month:")
            date[0] = 3
            date[1] = 6
            for i in range(0, 12):
                date[0] = date[0] + 1
                print(" - ", self.dateDisplay(date))
                add = ("INSERT INTO Income (Name, Type, Amount, Day, Month)"
                       "VALUES (%s, %s, %s, %s, %s)")
                data = (str(name), str(type), str(float(amount*4.33)), str(date[1]), str(date[0]))
                mycursor.execute(add, data)
                mydb.commit()
            print("Total per year: ", float(amount)*52, "GBP")

    def dateDisplay(self, date):
        if date[0] > 12:
            date[0] = date[0] - 12
        if date[0] == 1:
            month = "January"
        elif date[0] == 2:
            month = "February"
        elif date[0] == 3:
            month = "March"
        elif date[0] == 4:
            month = "April"
        elif date[0] == 5:
            month = "May"
        elif date[0] == 6:
            month = "June"
        elif date[0] == 7:
            month = "July"
        elif date[0] == 8:
            month = "August"
        elif date[0] == 9:
            month = "September"
        elif date[0] == 10:
            month = "October"
        elif date[0] == 11:
            month = "November"
        elif date[0] == 12:
            month = "December"
        elif date[0] == 0:
            if date[1] == 1:
                day = "Mondays"
            elif date[1] == 2:
                day = "Tuesdays"
            elif date[1] == 3:
                day = "Wednesdays"
            elif date[1] == 4:
                day = "Thursdays"
            elif date[1] == 5:
                day = "Fridays"
            elif date[1] == 6:
                day = "Saturdays"
            elif date[1] == 7:
                day = "Sundays"
            return("Weelky on "+ str(day))
        return(str(date[1]) + ' ' + str(month))


class expense():
    def __init__(self):
        answers = False
        while not answers:
            date = []
            name = input("Bill name: ")
            print("Per instance, what is the amount of the bill")
            amount = input("GBP: ")
            print("What frequency does this bill go out?")
            frequency = input("Annually (A), Quarterly (Q), Monthly (M), Weekly (W): ")
            if frequency.lower() != 'w':
                print("What date does this bill go out on?")
                day = input("1st - 28th (please only type the number): ")
                answers2 = False
                while not answers2:
                    if frequency.lower() == 'a':
                        print("What month does this bill go out?")
                        month = input("1 - 12 (please only type the number); ")
                        date.append(int(month))
                        answers2 = True
                    elif frequency.lower() == 'q':
                        print("What month does the first bill of the year go out on?")
                        month = input("1 - 12 (please only type the number); ")
                        date.append(int(month))
                        answers2 = True
                    elif frequency.lower() == 'm':
                        if int(day) >= 6:
                            date.append(3)
                        if int(day) < 6:
                            date.append(4)
                        answers2 = True
                    elif frequency.lower() == 'w':
                        date.append(00)
                        answers2 = True
                    else:
                        print("Please enter answers in the correct format")
                date.append(int(day))
                self.recordAdder(name, amount, frequency, date)
                print("Record added")
                break
                return None
            elif frequency.lower() == 'w':
                print("What day does this bill go out on?")
                day = input("1 - 7 (please only type the number): ")
                date.append(0)
                date.append(int(day))
                self.recordAdder(name, amount, frequency, date)
                print("\n")
                print("Record added")
                break
                return None
            else:
                print("Please enter answers in the correct format")

    def recordAdder(self, name, amount, frequency, date):
        print("Please confirm details of bill:")
        print()
        print("Bill name:", name)
        print("Bill amount per instance: ", str(amount) + " GBP")
        if frequency == 'a':
            print("Bill frequency: Annually")
        elif frequency == 'q':
            print("Bill frequency: Quarterly")
        elif frequency == 'm':
            print("Bill frequency: Monthly")
        elif frequency == 'w':
            print("Bill frequency: Weekly")
        print("Bill dates for current year:")
        if frequency == 'a':
            print(" - ", self.dateDisplay(date))
            print("Total per year: ", amount, "GBP")
            add = ("INSERT INTO Expenses (Name, Amount, Day, Month)"
                   "VALUES (%s, %s, %s, %s)")
            data = (str(name), str(amount), str(date[1]), str(date[0]))
            mycursor.execute(add, data)
            mydb.commit()
        elif frequency == 'q':
            print(" - ", self.dateDisplay(date))
            for i in range(0,3):
                date[0] = date[0] + 3
                print(" - ", self.dateDisplay(date))
                print("Total per year: ", amount, "GBP")
                add = ("INSERT INTO Expenses (Name, Amount, Day, Month)"
                       "VALUES (%s, %s, %s, %s)")
                data = (str(name), str(amount), str(date[1]), str(date[0]))
                mycursor.execute(add, data)
                mydb.commit()
            print("Total per year: ", float(amount)*4, "GBP")
        elif frequency == 'm':
            for i in range(0,12):
                date[0] = date[0] + 1
                print(" - ", self.dateDisplay(date))
                add = ("INSERT INTO Expenses (Name, Amount, Day, Month)"
                       "VALUES (%s, %s, %s, %s)")
                data = (str(name), str(amount), str(date[1]), str(date[0]))
                mycursor.execute(add, data)
                mydb.commit()
            print("Total per year: ", float(amount)*12, "GBP")
        elif frequency == 'w':
            print("Average total per month:")
            date[0] = 3
            date[1] = 6
            for i in range(0, 12):
                date[0] = date[0] + 1
                print(" - ", self.dateDisplay(date), str(float(amount) * 4.33), "GBP")
                add = ("INSERT INTO Expenses (Name, Amount, Day, Month)"
                       "VALUES (%s, %s, %s, %s)")
                data = (str(name), str(float(amount) * 4.33), str(date[1]), str(date[0]))
                mycursor.execute(add, data)
                mydb.commit()
            print("Total per year: ", float(amount)*52, "GBP")

    def dateDisplay(self, date):
        if date[0] > 12:
            date[0] = date[0] - 12
        if date[0] == 1:
            month = "January"
        elif date[0] == 2:
            month = "February"
        elif date[0] == 3:
            month = "March"
        elif date[0] == 4:
            month = "April"
        elif date[0] == 5:
            month = "May"
        elif date[0] == 6:
            month = "June"
        elif date[0] == 7:
            month = "July"
        elif date[0] == 8:
            month = "August"
        elif date[0] == 9:
            month = "September"
        elif date[0] == 10:
            month = "October"
        elif date[0] == 11:
            month = "November"
        elif date[0] == 12:
            month = "December"
        elif date[0] == 0:
            if date[1] == 1:
                day = "Mondays"
            elif date[1] == 2:
                day = "Tuesdays"
            elif date[1] == 3:
                day = "Wednesdays"
            elif date[1] == 4:
                day = "Thursdays"
            elif date[1] == 5:
                day = "Fridays"
            elif date[1] == 6:
                day = "Saturdays"
            elif date[1] == 7:
                day = "Sundays"
            return("Weelky on "+ str(day))
        return(str(date[1]) + ' ' + str(month))


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
        logInFunction()
        return None
    else:
        length = 12
        chars = string.ascii_letters + string.digits + '!@#$%^*&~:¬`'
        random.seed = (os.urandom(1024))
        secure = ''.join(random.choice(chars) for i in range(length))

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

        print("Your recovery key is: "+secure)
        print("Please make a note of this.")
        print("LOSS OF RECOVERY KEY WILL RESULT IN COMPLETE LOSS OF DATA")
        input("Press [enter] to continue")
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
        mycursor.execute("CREATE DATABASE FinanceRecords2023_24;")  # Creating database
        mydb.close()
        mydb = mysql.connector.connect(
            host="localhost",
            user="admin",
            password=secure,
            database="FinanceRecords2023_24"
        )
        mycursor = mydb.cursor()
        mycursor.execute("CREATE TABLE expenses ("
                         "Name varchar(255),"
                         "Amount float,"
                         "Day int,"
                         "Month varchar(255));")  # Creating expense table
        mycursor.execute("CREATE TABLE income ("
                         "Name varchar(255),"
                         "Type varchar(255),"
                         "Amount float,"
                         "Day int,"
                         "Month varchar(255));")  # Creating income table
        mydb.close()
        logInFunction()
        return None


def logInFunction():  # Function to log into the program
    logIn = False
    while not logIn:
        print("Please log in:")
        Uname = input("Username: ")
        Pword = input("Password: ")
        global mydb
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user=Uname,
                password=Pword,
                database="financerecords2023_24"
            )
        except:
            print("Incorrect username or password\n")
        else:
            logIn = True
            username = Uname
            password = Pword
            print("Welcome", Uname)
    return None


def fetch(table):
    query = ("SELECT * FROM " + table)
    try:
        mycursor.execute(query)
    except:
        print("Please enter a valid table name")
        return None
    else:
        result = mycursor.fetchall()
        total = 0
        if table == "income":
            for i in result:
                print("Income name:",i[0], "| Income type:",incomeTypeTranslator(i[1]), "| Instance amount:",i[2], "GBP",
                      "| Instance date: "+str(i[3])+"/"+str(i[4]))
                total = total + i[2]
            print("Total income amount: " + str(total))
        elif table == "expenses":
                for i in result:
                    print("Expense name:", i[0], "| Instance amount:", i[1], "GBP",
                          "| Instance date: " + str(i[2]) + "/" + str(i[3]))
                    total = total + i[1]
                print("Total income amount: " + str(total))
        return None


def incomeTypeTranslator(type):
    if type == "es":
        return("Salaried Employment")
    elif type == "eh":
        return("Hourly Employment")
    elif type == 'b':
        return("Benifits")
    elif type == 'c':
        return("Self-Employment/Contractor")
    elif type == 'd':
        return("Dividend Payout")


# Program starts here

startUp()
while True:
    mycursor = mydb.cursor()
    print()
    print("\n\n-----HOMESCREEN-----\n")
    print("Default year is 2023-24")
    print("Please type either  'expenses', or 'income' for this year to view.")
    print("Please choose a year to view/modify or type 'back' to quit the program")
    mycursor.execute("SHOW TABLES")
    for x in mycursor:
        print('-'+x[0])
    print()
    selection = input()
    if selection.lower() == "back":
        print("\nByeee!")
        mydb.close()
        exit()
        break
    elif selection.lower() == "add":
        print("Add income (I) or bill (B)?")
        selection = input()
        if selection.lower() == 'i':
            income()
        elif selection.lower() == 'b':
            expense()
    else:
        fetch(selection.lower())

# print("Create table?")
# create = input("y/n ")
"""if create == "y":
    mycursor.fetchall()
    createTable(table)"""
