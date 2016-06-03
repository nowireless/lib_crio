import logging

TO_DS_PORT = 1150
TO_ROBOT_PORT = 1110

LOOP_TIME = 0.1

SOCKET_TIME_OUT = 1

NO_CODE = "No Code?"
DISABLED = "Disabled?"
TELEOP = "Teleop?"
AUTO = "AUTO?"
TEST = "TEST?"


def team_to_ip(team_number):
    return "10."+str(team_number/100)+"."+str(team_number%100)+".2"


def team_to_ds(team_number):
    return "10."+str(team_number/100)+"."+str(team_number%100)+".5"


def make_logger(name, level):
    log = logging.getLogger(name)
    log.setLevel(level)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    ch.setLevel(logging.INFO)
    log.addHandler(ch)
    return log
