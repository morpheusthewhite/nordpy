import subprocess
from tkinter import messagebox, simpledialog
from bin.logging_util import get_logger
logger = get_logger(__name__)

def getRootPermissions(sudoPassword):
    obtainsRoot = subprocess.Popen(["sudo", "-S", "ls"], stdin=subprocess.PIPE, universal_newlines=True,
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    obtainsRoot.communicate(input=sudoPassword + "\n")

    logger.info("Obtained root access")


def test_root_password(sudoPassword):
    check_root = subprocess.Popen(["sudo -S ls"], stdin=subprocess.PIPE, universal_newlines=True,
                                   stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, shell=True)

    (_, err) = check_root.communicate(input=sudoPassword + "\n")

    if "Sorry, try again." in err:
        return False

    return True

def wrong_root_password():
    messagebox.showwarning(title="Wrong password", message="Wrong root password, insert it again")


def askRootPassword():
    rootPassword = simpledialog.askstring("Password", "Enter root password:", show='*')

    if rootPassword is None:
        return None

    while rootPassword is None or not test_root_password(rootPassword):
        wrong_root_password()
        rootPassword = simpledialog.askstring("Password", "Enter root password:", show='*')

        if rootPassword is None:
            return None

    return rootPassword
