import sys
import json
from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from .commands import ReadCommand
from .commands import UpdateCommand
from .responses import ResponsePacket
from .responses import Data_102_0

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
        else:   # call from read_all()
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
                
        compare_length = (len(ResponsePacket.correct_101_0.value))
        if bytes_string[:int(compare_length)] != ResponsePacket.correct_101_0.value:
            raise Exception("Wrong 101_0 response")
            
        return self.command(ReadCommand.status_102_0)

    def _read_command(self, command, socket):
        bytes_string = self._send_recv_packet(command, socket)
        
        compare_length = (len(ResponsePacket.correct_102_0.value))
        if bytes_string[:int(compare_length)] != ResponsePacket.correct_102_0.value:
            raise Exception("Wrong 102_0 response")
            
        binary_string = "{:08b}".format(int(bytes_string.hex(),16))
        result = self._bits_value(binary_string[(compare_length * 8):])
        
        return result

    def _send_recv_packet(self, command, socket):
        with socket(AF_INET, SOCK_STREAM) as s:
            s.connect((self._host, 8888))
            s.send(command.value)
            result = s.recv(100)
            s.close()
            
        return result
    
    def _bits_value(self, string):
        result = {}

        for field in Data_102_0:
            result[field.name] = string[(field.offset - 1):(field.offset + field.length - 1)]
        
        return json.dumps(result)

