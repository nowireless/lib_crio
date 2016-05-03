import scapy.all as s
import crio
import binascii
import crio.packets as p
from crio.packets import DriverStation2RobotPacket
from crio.packets import Robot2DriverStationPacket


if __name__ == "__main__":
    print "Reading packets"
    packets = s.rdpcap("/home/nowireless/Desktop/disabled_teleop.pcap")
    print "Loaded packets"
    udp_packets = packets[s.UDP][s.IP]
    print "Udp packets found:", len(udp_packets)

    to_robot = []
    to_ds = []

    for pack in udp_packets:
        ip_layer = pack.getlayer(s.IP)
        udp_layer = pack.getlayer(s.UDP)
        # print ip_layer.dst, ip_layer.src
        if ip_layer.dst == "10.30.81.2" and ip_layer.src == "10.30.81.5" and udp_layer.dport == crio.TO_ROBOT_PORT and len(pack) == 1066:
            to_robot.append(pack)
        elif ip_layer.dst == "10.30.81.5" and ip_layer.src == "10.30.81.2" and udp_layer.dport == crio.TO_DS_PORT and len(pack) == 1066:
            to_ds.append(pack)
        else:
            print "Ignoring packet", pack.summary()

    print "To Robot packets", len(to_robot)
    print "To DS packets", len(to_ds)

    #for i in to_robot:
    #    print type(i)
    #    print len(i), len(i.getlayer(s.Raw).load)
    #    print i.show()
    #print len(to_robot[502].getlayer(s.Raw).load)
    #print "------"
    #print type(to_robot[2])
    #print len(to_robot[2].getlayer(s.Raw).load)
    #print to_robot[2].show()
    #print DriverStation2cRIOPacket.from_data(to_robot[2].getlayer(s.Raw).load)

    for packet in to_ds:
        c = Robot2DriverStationPacket.from_data(packet.getlayer(s.Raw).load)
        #if not c.control_byte.enabled:
        #    continue
        print c.control_byte.enabled, binascii.unhexlify(hex(c.version)[2:]), c.reported_state_str()
        #print c
        #print c.packet_index, c.control_byte

    #for packet in to_robot:
    #    c = DriverStation2RobotPacket.from_data(packet.getlayer(s.Raw).load)
    #    print binascii.unhexlify(hex(c.version)[2:])
    #    print c.packet_index, c.control_byte
