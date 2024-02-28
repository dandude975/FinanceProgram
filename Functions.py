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
            )
        except:
            print("Incorrect username or password\n")
        else:
            logIn = True
            username = Uname
            password = Pword
            mycursor = mydb.cursor()
            mycursor.execute("CREATE DATABASE"+"FinanceRecords")
            return getDatabaseCursor(host, user, password)
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
    logOff()
    return logIn()


def getDatabaseCursor(host, username, password):
    global mydb
    mydb = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database="FinanceRecords"
    )
    global mycursor
    mycursor = mydb.cursor()
    while True:
        return mycursor
