import os
import json
import subprocess
from tkinter import simpledialog
from bin.pathUtil import CURRENT_PATH

CREDENTIALS_FILENAME = "credentials"
credentials_file_path = CURRENT_PATH + "credentials"
credentials_ikev2_file_path = CURRENT_PATH + "credentials.ikev2"


class NoCredentialsProvidedException(Exception):
    pass


def check_credentials():
    """
    checks if exists a file with the credentials for nordvpn.com
    :return: True if exists, False otherwise
    """
    return os.path.exists(credentials_file_path)


def save_credentials():
    """
    Stores credentials in a root-password-protected file. Raises a NoCredentialsProvidedException if some
    credentials info were not inserted
    """
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


def check_credentials_ikev2():
    """
    checks if exists a file with the credentials for ikev2 protocol
    :return: True if exists, False otherwise
    """
    return os.path.exists(credentials_ikev2_file_path)


def save_credentials_ikev2():
    """
    Stores credentials in a root-password-protected file. Raises a NoCredentialsProvidedException if some
    credentials info were not inserted
    """
    print("Storing credentials in " + "'" + credentials_ikev2_file_path + "'")

    username = askIkev2Username()
    if username is None:
        raise NoCredentialsProvidedException

    password = askIkev2Password()
    if password is None:
        raise NoCredentialsProvidedException

    try:
        with open(credentials_ikev2_file_path, 'w') as creds:
            json.dump({'username': username, 'password': password}, creds)

        # Change file permissions
        subprocess.check_call(["sudo", "chown", "root", credentials_file_path],
                                             universal_newlines=True, stdout=subprocess.DEVNULL,
                                             stderr=subprocess.DEVNULL)
        subprocess.check_call(["sudo", "chmod", "600", credentials_file_path],
                                             universal_newlines=True, stdout=subprocess.DEVNULL,
                                             stderr=subprocess.DEVNULL)

        print("Awesome, the credentials have been saved in " +
              "'" + credentials_ikev2_file_path + "'" + "\n")
    except (IOError, OSError):
        print(f"IOError while creating {credentials_ikev2_file_path} file.")



def askVPNUsername():
    """
    Asks VPN username by a dialog window
    :return: the username inserted
    """
    return simpledialog.askstring("Username NordVPN", "Enter username:")


def askVPNPassword():
    """
    Asks VPN password by a window dialog
    :return: the password inserted
    """
    return simpledialog.askstring("Password NordVPN", "Enter password:", show="*")


def askIkev2Username():
    """
    Asks Ikev2 username by a dialog window
    :return: the username inserted
    """
    return simpledialog.askstring("Ikev2 NordVPN username", "Enter username (see shorturl.at/lszBX):")


def askIkev2Password():
    """
    Asks Ikev2 password by a window dialog
    :return: the password inserted
    """
    return simpledialog.askstring("Ikev2 NordVPN password", "Enter password (see shorturl.at/lszBX):", show="*")


def read_saved_credentials():
    """
    reads saved credentials
    :return: a tuple containing (username, password)
    """
    args = ['sudo', 'cat', credentials_file_path]
    reading_process = subprocess.Popen(args, universal_newlines=True, stdout=subprocess.PIPE)
    (out, _) = reading_process.communicate()

    cred = out.split(os.linesep)

    return cred[0], cred[1]


def read_saved_credentials_ikev2():
    """
    reads saved credentials
    :return: a tuple containing (username, password)
    """
    args = ['sudo', 'cat', credentials_ikev2_file_path]
    reading_process = subprocess.Popen(args, universal_newlines=True, stdout=subprocess.PIPE)
    (out, _) = reading_process.communicate()

    cred = json.loads(out)

    return cred["username"], cred["password"]
