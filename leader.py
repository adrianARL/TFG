import socket
import random
import json
import errno
from agent import Agent


class Leader(Agent):

    MAX_NUM_AGENTS = 10

    def __init__(self, leader, ip_leader, port_leader):
        Agent.__init__(self, leader, ip_leader, port_leader)
        self.agents = {}
        self.socket_broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bind_connection()

    def __del__(self):
        print("Leader down")
        self.socket_broadcast.close()
        self.socket_leader.close()

    def generate_id(self):
        seed = random.getrandbits(32)
        if seed not in self.agents:
            return seed
        else:
            return self.generate_id()

    def bind_connection(self):
        self.socket_leader.bind((self.ip_leader, self.port_leader))
        self.socket_leader.listen(self.MAX_NUM_AGENTS)
        self.socket_broadcast.bind((self.ip_leader, self.port_leader+1))

    def accept_connection(self):
        while True:
            agent_connection, addr = self.socket_leader.accept()
            agent_id = str(self.generate_id())
            self.agents[agent_id] = agent_connection
            agent_connection.send(agent_id.encode())
            print("Nuevo agent con id " + agent_id)

    def answer_request(self, message, agent_id):
        self.agents[agent_id].send(message.encode())

    def send_broadcast_message(self, message):
        for agent_id in list(self.agents):
            try:
                self.agents[agent_id].send(message.encode())
            except:
                pass

    def request_received(self):
        for agent_id in list(self.agents):
            try:
                msg = self.agents[agent_id].recv(4096).decode()
                if(msg != None and msg != ""):
                    print("Solicitud recibida del agent " + agent_id)
                    return agent_id, msg
            except IOError as e:
                if(e.errno == errno.EWOULDBLOCK):
                    pass
        return None, None
