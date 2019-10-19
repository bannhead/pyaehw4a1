import sys
import json
from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from .commands import ReadCommand
from .commands import UpdateCommand
from .responses import ResponsePacket
from .responses import DataPacket

class AehW4a1:
    def __init__(self, host):
        self._host = host

    def command(self, command):
        for name, member in ReadCommand.__members__.items():
            if command == name:

                return self._read_command(member, socket)

        for name, member in UpdateCommand.__members__.items():
            if command == name:
                if command == "temp_to_F":
                    self._update_command(member, socket)

                    return self.command("temp_to_F_reset_temp")

                elif command == "temp_to_C":
                    self._update_command(member, socket)

                    return self.command("temp_to_C_reset_temp")

                else:

                    return self._update_command(member, socket)

        raise Exception("Not yet implemented: {0}".format(command))

    def _update_command(self, command, socket):
        pure_bytes = self._send_recv_packet(command, socket)
        packet_type = self._packet_type(pure_bytes)

        if self._check_response(packet_type, pure_bytes):

            return self.command("status_102_0")

        raise Exception("Unknown packet type {0}: {1}".format(packet_type, pure_bytes.hex()))

    def _read_command(self, command, socket):
        pure_bytes = self._send_recv_packet(command, socket)
        packet_type = self._packet_type(pure_bytes)
        data_start_pos = self._check_response(packet_type, pure_bytes)

        if data_start_pos:
            result = self._bits_value(packet_type, pure_bytes, data_start_pos)

            return result

        raise Exception("Unknown packet type {0}: {1}".format(packet_type, pure_bytes.hex()))

    def _send_recv_packet(self, command, socket):
        with socket(AF_INET, SOCK_STREAM) as s:
            s.connect((self._host, 8888))
            s.send(command.value)
            result = s.recv(100)
            s.close()

        return result

    def _bits_value(self, packet_type, pure_bytes, data_pos):
        result = {}

        binary_string = "{:08b}".format(int(pure_bytes.hex(),16))
        binary_data = binary_string[data_pos*8:-24]

        for data_packet in DataPacket:
            if packet_type in data_packet.name:
                for field in data_packet.value:
                    result[field.name] = binary_data[(field.offset - 1):(field.offset + field.length - 1)]

                return json.dumps(result)

        raise Exception("Unknown data type {0}: {1}".format(packet_type, binary_data))

    def _packet_type(self, string):
        type = int(string[13:14].hex(),16)
        sub_type = int(string[14:15].hex(),16)

        result = "{0}_{1}".format(type, sub_type)

        return result

    def _check_response(self, packet_type, pure_bytes):
        for response_packet in ResponsePacket:
            if packet_type in response_packet.name:
                if response_packet.value not in pure_bytes:

                    raise Exception("Wrong response for type {0}: {1}".format(packet_type, pure_bytes.hex()))

                return len(response_packet.value)

        return False