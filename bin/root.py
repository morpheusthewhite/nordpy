import subprocess
from tkinter import messagebox, simpledialog
from bin.logging_util import get_logger
logger = get_logger(__name__)


def get_root_permissions(sudo_password=None, parent=None):
    """
    Obtains root permission by launching a simple sudo command, asking for password is sudo_password is None.
    :param sudo_password: the root password
    :return false if no correct password has been provided, true otherwise
    """
    if has_root_privileges():
        return True

    if sudo_password is None:
        sudo_password = ask_root_password(parent)

        # no password has been inserted
        if sudo_password is None:
            return False

    obtainsRoot = subprocess.Popen(["sudo", "-S", "ls"], stdin=subprocess.PIPE, universal_newlines=True,
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    obtainsRoot.communicate(input=sudo_password + "\n")

    return True


def has_root_privileges():
    """
    checks if the process has temporarily obtained root privileges
    :return: True if it has, False otherwise
    """
    (_, err) = subprocess.Popen(["sudo", "-n", "ls"], stdin=subprocess.PIPE, universal_newlines=True,
                                  stderr=subprocess.PIPE, stdout=subprocess.DEVNULL).communicate()

    if "password is required" in err:
        return False

    return True


def test_root_password(sudo_password):
    """
    Checks if the given root password is correct
    :param sudo_password: the root password
    :return True if it is correct, False otherwise
    """
    check_root = subprocess.Popen(["sudo", "-S", "ls"], stdin=subprocess.PIPE, universal_newlines=True,
                                   stderr=subprocess.PIPE, stdout=subprocess.DEVNULL)

    (_, err) = check_root.communicate(input=sudo_password + "\n")

    if "Sorry, try again." in err:
        return False

    return True


def wrong_root_password():
    """
    Shows a window dialog notifying that the root password is not correct
    :return:
    """
    messagebox.showwarning(title="Wrong password", message="Wrong root password, insert it again")


def ask_root_password(parent=None):
    """
    Shows a window dialog that asks for the root password
    :return: the correct root password if inserted correctly, None otherwise
    """

    if parent is None:
        root_password = simpledialog.askstring("Password", "Enter root password:", show='*')
    else:
        root_password = simpledialog.askstring("Password", "Enter root password:", parent=parent, show='*')

    if root_password is None:
        return None

    while root_password is None or not test_root_password(root_password):
        wrong_root_password()
        root_password = simpledialog.askstring("Password", "Enter root password:", show='*')

        if root_password is None:
            return None

    return root_password
