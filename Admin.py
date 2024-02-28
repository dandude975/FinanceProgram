import mysql.connector

print("Please log in:")
input("[Press enter to log in]")
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
    )
except:
    print("Access denied\n")
else:
    mycursor = mydb.cursor()
    print("Successfully logged in")

while True:
    print("")
    command = input("Enter a command: ")
    if command.lower() == "exit":
        exit()
    mycursor.execute(command)
    print("Command executed")
    print("\n\n\n")