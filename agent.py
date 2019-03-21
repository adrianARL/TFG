import socket
import errno,sys
import json


class Agent:

    REQUEST_MESSAGE = "request_leader_info"
    REQUEST_TRAFFIC_LIGHT_STATUS = "requestTrafficLightStatus"
    TRAFFIC_LIGHT_REQUEST = "request_traffic_light_info"
    NESTED_LEADERS_REQUEST = "requestNestedLeaders"

    def __init__(self, leader, ip_leader, port_leader):
        self.ip_leader = ip_leader
        self.port_leader = port_leader
        self.socket_leader = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.json_data = None

        if(not leader):
            self.id = self.make_connection(self.ip_leader, self.port_leader)

    def __del__(self):
        print("Agent down")
        self.socket_leader.close()

    def make_connection(self, ip, port):
        print("Me intento conectar a " + "(" + ip + ":" + str(port) + ")")
        self.ip_leader = ip
        self.port_leader = port
        self.socket_leader.close()
        try:
            self.socket_leader =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_leader.connect((ip, port))
            id = self.socket_leader.recv(4096).decode()
            print("Me han asignado el ID " + id)
            return id
        except:
            print("El agente no se ha podido conectar al leader")
            self.__del__()

    def send_message(self, message):
        self.socket_leader.send(message.encode())

    def receive_message(self):
        message = self.socket_leader.recv(4096).decode()
        return message

    def request_leader_info(self, request_message):
        self.send_message(request_message)
        leader_info = self.socket_leader.recv(4096).decode()
        leader_info = json.loads(leader_info)
        return leader_info

    def close_leader(self):
        self.socket_leader.close()

