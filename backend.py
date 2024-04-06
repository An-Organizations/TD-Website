import os.path

filename = "accounts.txt"


def createAccount(username, passwrd, file):
    file.write(f"{username} ; {passwrd}\n")

def promptUser():
    usrname = input("Username: ")
    passwrd = input("Password: ")
    with open("accounts.txt", "a") as file:  # Open for appending
        createAccount(usrname, passwrd, file)


promptUser()
