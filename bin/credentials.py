import os
import subprocess
from tkinter import simpledialog
from bin.pathUtil import CURRENT_PATH

CREDENTIALS_FILENAME = "credentials"

def check_credentials():
    return os.path.exists(credentials_file_path)


def save_credentials():
    print("Storing credentials in " + "'" + credentials_file_path + "'" + " with openvpn",
          "compatible 'auth-user-pass' file format\n")

    username = input("Enter your username for NordVPN, i.e youremail@yourmail.com: ")
    password = input("Enter the password for NordVPN: ")
    try:
        with open(credentials_file_path, 'w') as creds:
            creds.write(username + "\n")
            creds.write(password + "\n")

        # Change file permissions
        subprocess.check_call(["sudo", "chown", "root", credentials_file_path],
                                             universal_newlines=True, stdout=subprocess.DEVNULL,
                                             stderr=subprocess.DEVNULL)
        subprocess.check_call(["sudo", "chmod", "600", credentials_file_path],
                                             universal_newlines=True, stdout=subprocess.DEVNULL,
                                             stderr=subprocess.DEVNULL)

        print("Awesome, the credentials have been saved in " +
              "'" + credentials_file_path + "'" + "\n")
    except (IOError, OSError):
        print("IOError while creating 'credentials' file.")
    return

def askRootPassword():
    rootPassword = simpledialog.askstring("Password", "Enter password:", show='*')
    return rootPassword

credentials_file_path = CURRENT_PATH + "credentials"