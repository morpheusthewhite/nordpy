import os
import subprocess
from tkinter import simpledialog
from bin.pathUtil import CURRENT_PATH

CREDENTIALS_FILENAME = "credentials"


class NoCredentialsProvidedException(Exception):
    pass


def check_credentials():
    return os.path.exists(credentials_file_path)


def save_credentials():
    print("Storing credentials in " + "'" + credentials_file_path + "'" + " with openvpn",
          "compatible 'auth-user-pass' file format\n")

    username = askVPNUsername()
    if username is None:
        raise NoCredentialsProvidedException

    password = askVPNPassword()
    if password is None:
        raise NoCredentialsProvidedException

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


def askVPNUsername():
    return simpledialog.askstring("Username NordVPN", "Enter username:")


def askVPNPassword():
    return simpledialog.askstring("Password NordVPN", "Enter password:", show="*")


credentials_file_path = CURRENT_PATH + "credentials"