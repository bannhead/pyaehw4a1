import sys
from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from .commands import ReadCommand
from .commands import UpdateCommand
from .commands import ResponsePacket

class AehW4a1:
    def __init__(self, host):
        self._host = host

    def command(self, command):
        if  isinstance(command, str):
            for pointer_to_enum in ReadCommand:
                if command == pointer_to_enum.name:
                    return self._read_command(pointer_to_enum, socket)
            for pointer_to_enum in UpdateCommand:
                if command == pointer_to_enum.name:
                    return self._update_command(pointer_to_enum, socket)
        else:
            if command.name in ReadCommand.__dict__:
                return self._read_command(command, socket)

            if command.name in UpdateCommand.__dict__:
                return self._update_command(command, socket)

        raise Exception("Not yet implemented")

    def read_all(self):
        result = {}

        for command in ReadCommand:
            binary_string = self.command(command)    
            result[command] = binary_string

        return result

    def _update_command(self, command, socket):
        bytes_string = self._send_recv_packet(command, socket)
                
        # Check starting bytes
        if bytes_string != ResponsePacket.correct_101_0.value:
            raise Exception("Wrong 101_0 response")
            
        return True

    def _read_command(self, command, socket):
        bytes_string = self._send_recv_packet(command, socket)
        
        # Check starting bytes
        compare_length = (sys.getsizeof(ResponsePacket.correct_102_0_start) / 2)
        if bytes_string[:int(compare_length)] != ResponsePacket.correct_102_0_start.value:
            raise Exception("Wrong 102_0 response")
            
        binary_string = "{:08b}".format(int(bytes_string.hex(),16))
            
        return binary_string

    def _send_recv_packet(self, command, socket):
        with socket(AF_INET, SOCK_STREAM) as s:
            s.connect((self._host, 8888))
            s.send(command.value)
            result = s.recv(100)
            s.close()
            
        return result

