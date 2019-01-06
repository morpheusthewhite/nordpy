import subprocess
from tkinter import messagebox, simpledialog
from bin.logging_util import get_logger
logger = get_logger(__name__)


def get_root_permissions(sudo_password):
    """
    Obtains root permission by launching a simple sudo command
    :param sudo_password: the root password
    """
    obtainsRoot = subprocess.Popen(["sudo", "-S", "ls"], stdin=subprocess.PIPE, universal_newlines=True,
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    obtainsRoot.communicate(input=sudo_password + "\n")

    logger.info("Obtained root access")


def test_root_password(sudo_password):
    """
    Checks if the given root password is correct
    :param sudo_password: the root password
    :return True if it is correct, False otherwise
    """
    check_root = subprocess.Popen(["sudo -S ls"], stdin=subprocess.PIPE, universal_newlines=True,
                                   stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, shell=True)

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


def ask_root_password():
    """
    Shows a window dialog that asks for the root password
    :return: the correct root password if inserted correctly, None otherwise
    """
    root_password = simpledialog.askstring("Password", "Enter root password:", show='*')

    if root_password is None:
        return None

    while root_password is None or not test_root_password(root_password):
        wrong_root_password()
        root_password = simpledialog.askstring("Password", "Enter root password:", show='*')

        if root_password is None:
            return None

    return root_password
