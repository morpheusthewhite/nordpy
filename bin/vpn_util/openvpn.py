from bin.conf_util import get_path_to_conf
from bin.credentials import *
from bin.root import *
from bin.logging_util import get_logger
from bin.vpn_util.exceptions import LoginError, OpenresolvError
from bin.vpn_util.killswitch import killswitch_up, killswitch_down

import signal

MAXIMUM_TRIES = 2
IKEV2_PROTOCOL_NUMBER = 2
TIMEOUT_TIME = 10
logger = get_logger(__name__)


def timeout_handler(signum, frame):
    raise TimeoutError


# registers the handler for the signal
signal.signal(signal.SIGALRM, timeout_handler)


def start_openvpn(server, protocol, killswitch=True):
    """
    starts openvpn connection with a certain protocol to a specific server. Raise a ConnectionError
    if the connection failed, a LoginError if the credentials are wrong or a OpenresolvError if openresolv is missing
    :param server: the server to which the connection will be established
    :param protocol: the protocol to be used (an integer)
    """
    pathToConf = get_path_to_conf(server, protocol)
    args = ["sudo", "openvpn", "--config", pathToConf, "--auth-user-pass", CURRENT_PATH + CREDENTIALS_FILENAME,
            # to prevent dns leaks
            "--script-security", "2", "--up", os.path.join(CURRENT_PATH, "scripts", "nordpy_up.sh"), "--down",
            os.path.join(CURRENT_PATH, "scripts", "nordpy_down.sh")]

    tries = 0
    while tries < MAXIMUM_TRIES:

        if killswitch:
            # activate killswitch
            killswitch_up(server, protocol)

        openvpn = subprocess.Popen(args, stdin=subprocess.PIPE, universal_newlines=True, stdout=subprocess.PIPE)

        signal.alarm(TIMEOUT_TIME)

        try:
            while True:
                line = openvpn.stdout.readline()

                if not line.strip() == '':
                    logger.debug("[OPENVPN]: "+line)

                if "Initialization Sequence Completed" in line:
                    # success !
                    signal.alarm(0)
                    return openvpn
                elif "connection failed" in line or "Exiting" in line:
                    tries += 1
                    openvpn_stop(killswitch)
                    break

                elif "AUTH_FAILED" in line:
                    # something's wrong
                    signal.alarm(0)

                    if killswitch:
                        killswitch_down()

                    raise LoginError

                # missing script
                elif "script fails with" in line:
                    signal.alarm(0)

                    if killswitch:
                        killswitch_down()
                    raise OpenresolvError

        except TimeoutError:
            logger.warning("expired timeout for openvpn connection")
            tries += 1
            openvpn_stop(killswitch)

    signal.alarm(0)

    # sometimes openvpn.kill() doesn't close the launched processes
    openvpn_stop(killswitch)

    raise ConnectionError


def openvpn_stop(killswitch=True):
    """
    Closes all runnning openvpn processes
    """
    subprocess.Popen(["sudo", "killall", "openvpn"]).communicate()

    if killswitch:
        killswitch_down()


def checkOpenVPN():
    """
    Checks if a openvpn process is already running
    :return: True if is running, False otherwise
    """
    c = subprocess.Popen(["ps ax | grep openvpn | grep -v grep"], stdout=subprocess.PIPE, shell=True, universal_newlines=True)
    (out, _) = c.communicate()
    if out != '':
        return True
    return False
