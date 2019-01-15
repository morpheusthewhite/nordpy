import os
import subprocess
from tkinter import simpledialog
from bin.pathUtil import CURRENT_PATH
from bin.root import get_root_permissions

CREDENTIALS_FILENAME = "credentials"


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


def read_saved_credentials(sudo_password):
    """
    reads saved credentials
    :param sudo_password: the root password
    :return:
    """
    get_root_permissions(sudo_password)

    args = ['sudo', 'cat', credentials_file_path]
    reading_process = subprocess.Popen(args, universal_newlines=True, stdout=subprocess.PIPE)
    (out, _) = reading_process.communicate()

    cred = out.split(os.linesep)

    return cred[0], cred[1]


credentials_file_path = CURRENT_PATH + "credentials"