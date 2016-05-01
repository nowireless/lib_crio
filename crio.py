import socket
from threading import Thread
import time
import logging
from packets import DriverStation2cRIOPacket
from packets import cRIO2DSPacket

TO_DS_PORT = 1150
TO_ROBOT_PORT = 1110

#log = logging.getLogger("crio")
#log.setLevel(logging.INFO)
#ch = logging.StreamHandler()
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#ch.setFormatter(formatter)
#ch.setLevel(logging.INFO)
#log.addHandler(ch)


def team_to_ip(team_number):
    return "10."+str(team_number/100)+"."+str(team_number%100)+".2"


def team_to_ds(team_number):
    return "10."+str(team_number/100)+"."+str(team_number%100)+".5"


def make_logger(name, level):
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    ch.setLevel(logging.INFO)
    log.addHandler(ch)
    return log


class SendToRobotThread(Thread):
    def __init__(self, team_number):
        super(SendToRobotThread, self).__init__()
        self.log = make_logger("Send", logging.INFO)
        self.team_number = team_number

    def run(self):
        robot = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip = team_to_ip(self.team_number)
        packet_number = 0
        while True:
            packet = DriverStation2cRIOPacket.make_packet(packet_number, self.team_number)
            packet.control_byte.reset = False
            packet.control_byte.enabled = False
            self.log.info("Sending packet")
            robot.sendto(packet.pack(), (ip,TO_ROBOT_PORT))

            packet_number = (packet_number + 1) % 65535
            time.sleep(0.02)#Send packets at 50hz


class ReceiveFromRobotThread(Thread):
    def __init__(self, team_number):
        super(ReceiveFromRobotThread, self).__init__()
        self.log = make_logger("Receive", logging.INFO)
        self.team_number = team_number

    def run(self):
        robot = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.log.info("Binding socket")
        robot.bind(("10.30.81.5",TO_DS_PORT))
        while True:
            data, addr = robot.recvfrom(1024)
            packet = cRIO2DSPacket.from_data(data)
            self.log.info("Received packet %i", packet.packet_index)


r = ReceiveFromRobotThread(3081)
s = SendToRobotThread(3081)
r.start()
s.start()