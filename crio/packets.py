from suitcase.crc import crc32
from suitcase.fields import BitBool
from suitcase.fields import BitField
from suitcase.fields import CRCField
from suitcase.fields import Payload
from suitcase.fields import UBInt8
from suitcase.fields import UBInt16
from suitcase.fields import UBInt32
from suitcase.fields import UBInt40
from suitcase.fields import UBInt48
from suitcase.fields import UBInt64
from suitcase.structure import Structure


class DriverStation2RobotPacket(Structure):
    packet_index = UBInt16()
    control_byte = BitField(8,
                            reset = BitBool(),
                            not_estop = BitBool(),
                            enabled = BitBool(),
                            autonmous = BitBool(),
                            fms_attached = BitBool(),
                            resync = BitBool(),
                            test = BitBool(),
                            fpga_checksum = BitBool()
                        )
    digital_input = BitField(8,
                             input_8 = BitBool(),
                             input_7 = BitBool(),
                             input_6 = BitBool(),
                             input_5 = BitBool(),
                             input_4 = BitBool(),
                             input_3 = BitBool(),
                             input_2 = BitBool(),
                             input_1 = BitBool(),
                        )
    team_number = UBInt16()
    alliance = UBInt8() #ASCII of B or R
    position = UBInt8() #ASCII of 1,2,3

    joystick_1_axis_1 = UBInt8()
    joystick_1_axis_2 = UBInt8()
    joystick_1_axis_3 = UBInt8()
    joystick_1_axis_4 = UBInt8()
    joystick_1_axis_5 = UBInt8()
    joystick_1_axis_6 = UBInt8()
    joystick_1_buttons = BitField(16,
                                  button_1 = BitBool(),
                                  button_2 = BitBool(),
                                  button_3 = BitBool(),
                                  button_4 = BitBool(),
                                  button_5 = BitBool(),
                                  button_6 = BitBool(),
                                  button_7 = BitBool(),
                                  button_8 = BitBool(),
                                  button_9 = BitBool(),
                                  button_10 = BitBool(),
                                  button_11 = BitBool(),
                                  button_12 = BitBool(),
                                  button_13 = BitBool(),
                                  button_14 = BitBool(),
                                  button_15 = BitBool(),
                                  button_16 = BitBool()
                                )
    joystick_2_axis_1 = UBInt8()
    joystick_2_axis_2 = UBInt8()
    joystick_2_axis_3 = UBInt8()
    joystick_2_axis_4 = UBInt8()
    joystick_2_axis_5 = UBInt8()
    joystick_2_axis_6 = UBInt8()
    joystick_2_buttons = BitField(16,
                                  button_1 = BitBool(),
                                  button_2 = BitBool(),
                                  button_3 = BitBool(),
                                  button_4 = BitBool(),
                                  button_5 = BitBool(),
                                  button_6 = BitBool(),
                                  button_7 = BitBool(),
                                  button_8 = BitBool(),
                                  button_9 = BitBool(),
                                  button_10 = BitBool(),
                                  button_11 = BitBool(),
                                  button_12 = BitBool(),
                                  button_13 = BitBool(),
                                  button_14 = BitBool(),
                                  button_15 = BitBool(),
                                  button_16 = BitBool()
                              )
    joystick_3_axis_1 = UBInt8()
    joystick_3_axis_2 = UBInt8()
    joystick_3_axis_3 = UBInt8()
    joystick_3_axis_4 = UBInt8()
    joystick_3_axis_5 = UBInt8()
    joystick_3_axis_6 = UBInt8()
    joystick_3_buttons = BitField(16,
                                  button_1 = BitBool(),
                                  button_2 = BitBool(),
                                  button_3 = BitBool(),
                                  button_4 = BitBool(),
                                  button_5 = BitBool(),
                                  button_6 = BitBool(),
                                  button_7 = BitBool(),
                                  button_8 = BitBool(),
                                  button_9 = BitBool(),
                                  button_10 = BitBool(),
                                  button_11 = BitBool(),
                                  button_12 = BitBool(),
                                  button_13 = BitBool(),
                                  button_14 = BitBool(),
                                  button_15 = BitBool(),
                                  button_16 = BitBool()
                              )
    joystick_4_axis_1 = UBInt8()
    joystick_4_axis_2 = UBInt8()
    joystick_4_axis_3 = UBInt8()
    joystick_4_axis_4 = UBInt8()
    joystick_4_axis_5 = UBInt8()
    joystick_4_axis_6 = UBInt8()
    joystick_4_buttons = BitField(16,
                                  button_1 = BitBool(),
                                  button_2 = BitBool(),
                                  button_3 = BitBool(),
                                  button_4 = BitBool(),
                                  button_5 = BitBool(),
                                  button_6 = BitBool(),
                                  button_7 = BitBool(),
                                  button_8 = BitBool(),
                                  button_9 = BitBool(),
                                  button_10 = BitBool(),
                                  button_11 = BitBool(),
                                  button_12 = BitBool(),
                                  button_13 = BitBool(),
                                  button_14 = BitBool(),
                                  button_15 = BitBool(),
                                  button_16 = BitBool()
                                  )
    analog_value_1 = UBInt16()
    analog_value_2 = UBInt16()
    analog_value_3 = UBInt16()
    analog_value_4 = UBInt16()
    crio_checksum = UBInt64()
    fpga_checksum_1 = UBInt32()
    fpga_checksum_2 = UBInt32()
    fpga_checksum_3 = UBInt32()
    fpga_checksum_4 = UBInt32()
    driver_station_version = UBInt64() #ASCII string such as '02121300'

    unknown = Payload(939)

    #crc_checksum = UBInt32()
    crc_checksum = CRCField(UBInt32(), crc32, 0, 1024)

    @staticmethod
    def make_packet(index, team_number):
        ret = DriverStation2RobotPacket()
        ret.packet_index = index
        ret.control_byte.reset = False
        ret.control_byte.not_estop = True
        ret.control_byte.enabled = False
        ret.control_byte.autonmous = False
        ret.control_byte.fms_attached = False
        ret.control_byte.resync = False
        ret.control_byte.fpga_checksum = False
        ret.digital_input.input_8 = False
        ret.digital_input.input_7 = False
        ret.digital_input.input_6 = False
        ret.digital_input.input_5 = False
        ret.digital_input.input_4 = False
        ret.digital_input.input_3 = False
        ret.digital_input.input_2 = False
        ret.digital_input.input_1 = False
        ret.team_number = team_number
        ret.alliance = ord('R')
        ret.position = ord('1')
        ret.joystick_1_axis_1 = 0
        ret.joystick_1_axis_2 = 0
        ret.joystick_1_axis_3 = 0
        ret.joystick_1_axis_4 = 0
        ret.joystick_1_axis_5 = 0
        ret.joystick_1_axis_6 = 0
        ret.joystick_1_buttons.button_1 = False
        ret.joystick_1_buttons.button_2 = False
        ret.joystick_1_buttons.button_3 = False
        ret.joystick_1_buttons.button_4 = False
        ret.joystick_1_buttons.button_5 = False
        ret.joystick_1_buttons.button_6 = False
        ret.joystick_1_buttons.button_7 = False
        ret.joystick_1_buttons.button_8 = False
        ret.joystick_1_buttons.button_9 = False
        ret.joystick_1_buttons.button_10 = False
        ret.joystick_1_buttons.button_11 = False
        ret.joystick_1_buttons.button_12 = False
        ret.joystick_1_buttons.button_13 = False
        ret.joystick_1_buttons.button_14 = False
        ret.joystick_1_buttons.button_15 = False
        ret.joystick_1_buttons.button_16 = False

        ret.joystick_2_axis_1 = 0
        ret.joystick_2_axis_2 = 0
        ret.joystick_2_axis_3 = 0
        ret.joystick_2_axis_4 = 0
        ret.joystick_2_axis_5 = 0
        ret.joystick_2_axis_6 = 0
        ret.joystick_2_buttons.button_1 = False
        ret.joystick_2_buttons.button_2 = False
        ret.joystick_2_buttons.button_3 = False
        ret.joystick_2_buttons.button_4 = False
        ret.joystick_2_buttons.button_5 = False
        ret.joystick_2_buttons.button_6 = False
        ret.joystick_2_buttons.button_7 = False
        ret.joystick_2_buttons.button_8 = False
        ret.joystick_2_buttons.button_9 = False
        ret.joystick_2_buttons.button_10 = False
        ret.joystick_2_buttons.button_11 = False
        ret.joystick_2_buttons.button_12 = False
        ret.joystick_2_buttons.button_13 = False
        ret.joystick_2_buttons.button_14 = False
        ret.joystick_2_buttons.button_15 = False
        ret.joystick_2_buttons.button_16 = False

        ret.joystick_3_axis_1 = 0
        ret.joystick_3_axis_2 = 0
        ret.joystick_3_axis_3 = 0
        ret.joystick_3_axis_4 = 0
        ret.joystick_3_axis_5 = 0
        ret.joystick_3_axis_6 = 0
        ret.joystick_3_buttons.button_1 = False
        ret.joystick_3_buttons.button_2 = False
        ret.joystick_3_buttons.button_3 = False
        ret.joystick_3_buttons.button_4 = False
        ret.joystick_3_buttons.button_5 = False
        ret.joystick_3_buttons.button_6 = False
        ret.joystick_3_buttons.button_7 = False
        ret.joystick_3_buttons.button_8 = False
        ret.joystick_3_buttons.button_9 = False
        ret.joystick_3_buttons.button_10 = False
        ret.joystick_3_buttons.button_11 = False
        ret.joystick_3_buttons.button_12 = False
        ret.joystick_3_buttons.button_13 = False
        ret.joystick_3_buttons.button_14 = False
        ret.joystick_3_buttons.button_15 = False
        ret.joystick_3_buttons.button_16 = False

        ret.joystick_4_axis_1 = 0
        ret.joystick_4_axis_2 = 0
        ret.joystick_4_axis_3 = 0
        ret.joystick_4_axis_4 = 0
        ret.joystick_4_axis_5 = 0
        ret.joystick_4_axis_6 = 0
        ret.joystick_4_buttons.button_1 = False
        ret.joystick_4_buttons.button_2 = False
        ret.joystick_4_buttons.button_3 = False
        ret.joystick_4_buttons.button_4 = False
        ret.joystick_4_buttons.button_5 = False
        ret.joystick_4_buttons.button_6 = False
        ret.joystick_4_buttons.button_7 = False
        ret.joystick_4_buttons.button_8 = False
        ret.joystick_4_buttons.button_9 = False
        ret.joystick_4_buttons.button_10 = False
        ret.joystick_4_buttons.button_11 = False
        ret.joystick_4_buttons.button_12 = False
        ret.joystick_4_buttons.button_13 = False
        ret.joystick_4_buttons.button_14 = False
        ret.joystick_4_buttons.button_15 = False
        ret.joystick_4_buttons.button_16 = False

        ret.analog_value_1 = 0
        ret.analog_value_2 = 0
        ret.analog_value_3 = 0
        ret.analog_value_4 = 0
        ret.crio_checksum = 0
        ret.fpga_checksum_1 = 0
        ret.fpga_checksum_2 = 0
        ret.fpga_checksum_3 = 0
        ret.fpga_checksum_4 = 0
        ret.driver_station_version = 3546356223709687856# This was reported by the FRC 2016 DS

        payload = ""
        for i in xrange(0,940):
            payload += "\x00"
        ret.unknown = payload
        return ret


class Robot2DriverStationPacket(Structure):
    control_byte = BitField(8,
                            reset = BitBool(),
                            not_estop = BitBool(),
                            enabled = BitBool(),
                            autonmous = BitBool(),
                            fms_attacted = BitBool(),
                            resync = BitBool(),
                            test = BitBool(),
                            fpga_checksum = BitBool()
                        )
    battery_voltage = UBInt16()
    ds_digital_in = UBInt8()
    unknown_1 = UBInt32()
    team_number = UBInt16()
    crio_mac_address = UBInt48()
    version = UBInt64()
    unknown_2b = UBInt40()
    unknown_3 = UBInt8()
    packet_index = UBInt16()
    unknown_4 = Payload(988)
    crc_checksum = CRCField(UBInt32(), crc32, 0,1024)

if __name__ == "__main__":
    file = open("packets/packet_1.bin",'rb')
    #data_hex = binascii.hexlify(file.read())
    #data = binascii.unhexlify(data_hex)
    #print binascii.crc32(data)
    #print binascii.crc32(data[:-4])
    #print data_hex
    print DriverStation2RobotPacket.from_data(file.read())

    file = open("packets/packet_2_crio2ds.bin",'rb')
#    data_hex = binascii.hexlify(file.read())
#    data = binascii.unhexlify(data_hex)
#    print data_hex
    print Robot2DriverStationPacket.from_data(file.read())

    print DriverStation2RobotPacket.from_data(DriverStation2RobotPacket.make_packet(2, 3081).pack())