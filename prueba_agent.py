import time
from multiprocessing import Process, Queue
from multiprocessing.managers import BaseManager
from agent import Agent


"""
Procesos:
    - LineFollower
    - Lector de RFID
    - Agent
"""

LEADER_IP = "10.10.176.123"
LEADER_PORT = 5000

LEADER_IP_B = "10.9.41.216"
LEADER_PORT_B = 5000

def reconect(agent):
    while True:
        agent.make_connection(LEADER_IP_B, LEADER_PORT_B)
        print ("traffic: "+str(agent.request_leader_info(agent.TRAFFIC_LIGHT_REQUEST)))
        print("nested: "+str(agent.request_leader_info(agent.NESTED_LEADERS_REQUEST)))
        agent.close_leader()
        time.sleep(3)
        print("\n\n\n\n")
        agent.make_connection(LEADER_IP, LEADER_PORT)
        print ("traffic: "+str(agent.request_leader_info(agent.TRAFFIC_LIGHT_REQUEST)))
        print("nested: "+str(agent.request_leader_info(agent.NESTED_LEADERS_REQUEST)))
        agent.close_leader()
        print("\n\n\n\n")
        time.sleep(3)



def main():
    agent = Agent(False, LEADER_IP_B, LEADER_PORT_B)
    reconect(agent)

if __name__ == '__main__':
    main()
