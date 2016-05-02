import crio
import logging
import time
import socket
from packets import DriverStation2cRIOPacket
from packets import cRIO2DSPacket
from threading import Thread

class RobotState:
    def __init__(self):
        self.enabled = False


class SendToRobotThread(Thread):
    def __init__(self, team_number):
        super(SendToRobotThread, self).__init__()
        self.log = crio.make_logger("Send", logging.INFO)
        self.team_number = team_number
        self.running = False

    def run(self):
        self.running = True
        robot = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip = crio.team_to_ip(self.team_number)
        packet_number = 0
        while self.running:
            packet = DriverStation2cRIOPacket.make_packet(packet_number, self.team_number)
            packet.control_byte.reset = False
            packet.control_byte.enabled = False
            self.log.info("Sending packet")
            robot.sendto(packet.pack(), (ip, crio.TO_ROBOT_PORT))

            packet_number = (packet_number + 1) % 65535
            time.sleep(0.02)#Send packets at 50hz

    def stop(self):
        self.running = False


class ReceiveFromRobotThread(Thread):
    def __init__(self, team_number):
        super(ReceiveFromRobotThread, self).__init__()
        self.log = crio.make_logger("Receive", logging.INFO)
        self.team_number = team_number
        self.running = False

    def run(self):
        self.running = True
        robot = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.log.info("Binding socket")
        robot.bind(("10.30.81.5", crio.TO_DS_PORT))
        while self.running:
            data, addr = robot.recvfrom(1024)
            packet = cRIO2DSPacket.from_data(data)
            self.log.info("Received packet %i", packet.packet_index)

    def stop(self):
        self.running = False


class DS:
    def __init__(self, team):
        self.receive = ReceiveFromRobotThread(team)
        self.send = SendToRobotThread(team)

    def start(self):
        self.receive.start()
        self.send.start()

    def stop(self):
        self.receive.stop()
        self.send.stop()

#r = ReceiveFromRobotThread(3081)
#s = SendToRobotThread(3081)
#r.start()
#s.start()