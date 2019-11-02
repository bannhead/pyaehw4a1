import sys
import json
import threading
import ipaddress
from queue import Queue
from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from .commands import ReadCommand
from .commands import UpdateCommand
from .responses import ResponsePacket
from .responses import DataPacket
import ifaddr

class AehW4a1:
    def __init__(self, host=None):
        if host is None:
            self._host = None
        else:
            self._host = host

    def command(self, command):
        if not self._host:
            raise Exception("Host required")
        
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

            return True

        raise Exception("Unknown packet type {0}: {1}".format(packet_type,
                        pure_bytes.hex()))

    def _read_command(self, command, socket):
        pure_bytes = self._send_recv_packet(command, socket)
        packet_type = self._packet_type(pure_bytes)
        data_start_pos = self._check_response(packet_type, pure_bytes)

        if data_start_pos:
            result = self._bits_value(packet_type, pure_bytes, data_start_pos)

            return json.loads(result)

        raise Exception("Unknown packet type {0}: {1}".format(packet_type,
                        pure_bytes.hex()))

    def _send_recv_packet(self, command, socket):
        with socket(AF_INET, SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((self._host, 8888))
            s.settimeout(None)
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
                    result[field.name] = binary_data[(field.offset - 1):
                                        (field.offset + field.length - 1)]

                return json.dumps(result)

        raise Exception("Unknown data type {0}: {1}".format(packet_type,
                        binary_data))

    def _packet_type(self, string):
        type = int(string[13:14].hex(),16)
        sub_type = int(string[14:15].hex(),16)

        result = "{0}_{1}".format(type, sub_type)

        return result

    def _check_response(self, packet_type, pure_bytes):
        for response_packet in ResponsePacket:
            if packet_type in response_packet.name:
                if response_packet.value not in pure_bytes:

                    raise Exception("Wrong response for type {0}: {1}".
                                    format(packet_type, pure_bytes.hex()))

                return len(response_packet.value)

        return False

    def discovery(self, full=None):
        if full is None:
            self._full = None
        elif full == True:
            self._full = True
        else:
            
            raise Exception("Optional argument for discovery is: True")

        nets = []
        adapters = ifaddr.get_adapters()
        for adapter in adapters:
            for ip in adapter.ips:
                if ip.is_IPv4 and ip.ip != "127.0.0.1":
                    if self._full:
                        nets.append(
                            ipaddress.IPv4Network(f"{ip.ip}/{ip.network_prefix}",
                            strict=False)
                        )
                    else:
                        nets.append(
                            ipaddress.IPv4Network(f"{ip.ip}/24", strict=False)
                        )

        if not nets:
            return None

        acs = []
        que = Queue()
        
        for net in nets:
            q = Queue()

            for x in range(100):
                t = threading.Thread(target = self._threader, args=(q,que))
                t.daemon = True
                t.start()
                
            for ip in net:
                q.put(ip)

            q.join()
            
            if not que.empty() and not self._full:
                break

        while not que.empty():
            acs.append(que.get())

        return acs

    def _threader(self, q, que):
        while True:
            ip = q.get()
            test = self._check_addr(str(ip))
            if test:
                que.put(str(ip))
            q.task_done()

    def _check_addr(self, ip):
        with socket(AF_INET, SOCK_STREAM) as s:
            try:
                s.settimeout(0.5)
                s.connect((ip, 8888))
                s.settimeout(None)

            except OSError as e:
            
                return None

            s.send(bytes("AT+XMV", 'utf-8'))
            result = s.recv(13)
            s.close()
        
        if bytes("+XMV:", 'utf-8') not in result:
        
            return None
            
        return result