from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from .commands import ReadCommand
from .commands import UpdateCommand

class DanfossClient:
    def __init__(self, host):
        self._host = host

    def command(self, command):
        if isinstance(command, ReadCommand):
            return self._read_command(command, socket)

        if isinstance(command, UpdateCommand):
            return self._update_command(command, socket)

        raise Exception("Not yet implemented")

    def read_all(self):
        result = {}

        for command in ReadCommand:
            result[command] = self.command(command)

        return result

    def _update_command(self, command, socket):
        if command in {UpdateCommand.boost_activate,
                       UpdateCommand.boost_deactivate,
                       UpdateCommand.bypass_activate,
                       UpdateCommand.bypass_deactivate,
                       UpdateCommand.automatic_bypass_activate,
                       UpdateCommand.automatic_bypass_deactivate}:
            self._update_switch(command, socket)
            
            if(command == UpdateCommand.boost_activate or 
               command == UpdateCommand.boost_deactivate):
                return self._read_bit(ReadCommand.boost, socket)
            
            elif(command in {UpdateCommand.bypass_activate, 
                             UpdateCommand.bypass_deactivate}):
                return self._read_bit(ReadCommand.bypass, socket)
            
            else:
                return self._read_command(ReadCommand.automatic_bypass, socket)

        raise Exception("Unknown comand: {0}".format(command))

    def _update_switch(self, command, socket):
        self._read_value(command, socket)

    def _read_command(self, command, socket):
        if(command == ReadCommand.exhaustTemperature or
           command == ReadCommand.outdoorTemperature or
           command == ReadCommand.extractTemperature or
           command == ReadCommand.supplyTemperature):
            return self._read_temperature(command, socket)

        if(command == ReadCommand.humidity or
           command == ReadCommand.filterPercent or
           command == ReadCommand.battery_percent
                ):
            return self._read_percent(command, socket)

        if(command == ReadCommand.bypass or
           command == ReadCommand.boost or
           command == ReadCommand.away_mode
                ):
            return self._read_bit(command, socket)

        if command == ReadCommand.automatic_bypass:
            return not self._read_bit(command, socket)

        if(command == ReadCommand.supply_fan_speed or
           command == ReadCommand.exhaust_fan_speed
                ):
            return self._read_short(command, socket)

        if(command == ReadCommand.fan_step):
            return self._read_byte(command, socket)

        raise Exception("Unknown command: {0}".format(command))

    def _read_temperature(self, command, socket):
        return self._read_short(command, socket)/100

    def _read_bit(self, command, socket):
        result = self._read_value(command, socket)
        return result[0] != 0x00

    def _read_percent(self, command, socket):
        result = self._read_value(command, socket)
        return int(result[0]) * 100/255

    def _read_value(self, command, socket):
        with socket(AF_INET, SOCK_STREAM) as s:
            s.connect((self._host, 30046))
            s.send(command.value)
            result = s.recv(63)
            s.close()
            
            return result

    def _read_byte(self, command, socket):
        result = self._read_value(command, socket)
        
        r = bytes([result[0]])
        
        return int.from_bytes(r, byteorder = 'big', signed=True)

    def _read_short(self, command, socket):
        result = self._read_value(command, socket)
        
        r = bytes([result[0], result[1]])
        
        return int.from_bytes(r, byteorder = 'big', signed=True)
