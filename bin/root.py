import subprocess


def getRootPermissions(sudoPassword):
    obtainsRoot = subprocess.Popen(["sudo", "-S", "ls"], stdin=subprocess.PIPE, universal_newlines=True,
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    obtainsRoot.communicate(input=sudoPassword + "\n")