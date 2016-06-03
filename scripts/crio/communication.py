import crio
import logging
import network as net
import time
import socket
from packets import DriverStation2RobotPacket
from packets import Robot2DriverStationPacket
from threading import Thread
from threading import RLock


class RobotState:

    def __init__(self, team):
        self.team = team
        self.reset = False
        self.enabled = False
        self.estoped = False
        self.auto = False
        self.test = False

        self.joystick_axis = [
            [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
        self.buttons = [
            [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]]

    def reset_robot(self):
        self.reset = True

    def no_reset(self):
        self.reset = False

    def enable(self):
        if not self.estoped:
            self.enabled = True

    def disable(self):
        self.enabled = False

    def estop(self):
        self.estoped = True
        self.disable()

    def teleop(self):
        self.auto = False
        self.test = False

    def auto(self):
        self.auto = True
        self.test = False

    def test(self):
        self.auto = False
        self.test = True

    def make_packet(self, index):
        pkt = DriverStation2RobotPacket.make_packet(index, self.team)
        pkt.control_byte.reset = self.reset
        pkt.control_byte.enabled = self.enabled
        pkt.control_byte.not_estop = not self.estoped
        pkt.control_byte.autonmous = self.auto
        pkt.control_byte.test = self.test
        return pkt


class DSException(RuntimeError):
    pass


class DS(Thread):
    def __init__(self, team):
        super(DS, self).__init__()
        self.running = True
        self.team = team
        self.log = crio.make_logger("DS", logging.INFO)
        if net.check_interfaces(team):
            self.log.info("Interfaces look ok")
        else:
            self.log.fatal("Network does not seem to configured correctly")
            raise DSException
        self.state_lock = RLock()
        self.state = RobotState(team)

    def run(self):
        send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receive.settimeout(crio.SOCKET_TIME_OUT)

        self.log.info("Binding to socket")
        receive.bind((crio.team_to_ds(self.team), crio.TO_DS_PORT))

        crio_ip = crio.team_to_ip(self.team)
        packet_number = 0

        # Start out with not being connected to the crio
        alive = False

        while self.running:
            print self.state.enabled
            if not alive:
                self.log.info("Pinging robot")
                if net.is_host_alive(crio_ip):
                    self.log.info("Robot is alive, restarting communication")
                    alive = True
                    packet_number = 0 # Reset packet index
                    self.state_lock.acquire()
                    self.state.disable()
                    self.state_lock.release()
                time.sleep(1)

            # Send DS->Robot Packet
            self.state_lock.acquire()
            to_robot_packet = self.state.make_packet(packet_number)
            if self.state.reset:
                # Do this so only one packet is sent with the reset flag
                self.state.reset = False
            self.state_lock.release()
            send.sendto(to_robot_packet.pack(), (crio_ip, crio.TO_ROBOT_PORT))

            # Wait for Robot Packet
            data = None
            try:
                data, addr = receive.recvfrom(1024)
            except socket.timeout:
                self.log.warn("Received timeout, robot is not alive")
                alive = False
                continue

            from_crio_packet = Robot2DriverStationPacket.from_data(data)
            self.log.info("Sent %i | Got %i | %s | Enabled %s", packet_number, from_crio_packet.packet_index, str(from_crio_packet.packet_index == packet_number), from_crio_packet.control_byte.enabled)

            # Increment packet index
            packet_number = (packet_number + 1) % 65535
            time.sleep(crio.LOOP_TIME)
        receive.close()
        send.close()

    def stop(self):
        self.running = False

if __name__ == "__main__":
    ds = DS(3081)
    ds.start()
