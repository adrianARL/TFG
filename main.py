import time
from multiprocessing import Process, Queue
from multiprocessing.managers import BaseManager
from sensors import Sensors
from car_movement import CarMovement
from line_follower import LineFollower
from agent import Agent
from decision_maker import DecisionMaker
from frontend_connection import FrontendConnection
from requests.exceptions import ConnectionError


# LEADER_IP = "10.9.41.216"
LEADER_IP = "10.10.176.123"
LEADER_PORT = 5000

# Datos servidor donde se aloja el front-end
HOST_FRONTEND = '10.0.2.16'
PORT_FRONTEND = 3001


card_id = {
    "41 205 254 41": 'NW',
    "252 94 249 41": 'NE',
    "227 134 166 137" : 'SE',
    "47 34 231 89" : 'SW',
    "57 156 167 137" : 'UB',
    "140 88 228 137" : 'N1',
    "158 220 186 89" : 'N2',
    "220 24 232 137" : 'N3',
    "119 44 171 169" : 'N4',
    "193 125 198 89" : 'N5',
    "014 137 254 41" : 'N6',
    "81 127 227 137" : 'N7',
    "186 134 166 137" : 'S1',
    "78 95 166 137" : 'S2',
    "255 014 167 137" : 'S3',
    "217 117 197 89" : 'S4',
    "137 40 167 137" : 'S5',
    "01 180 166 137" : 'S6',
    "50 74 227 41" : 'S7',
    "27 06 231 89" : 'W1',
    "01 84 254 41" : 'W2',
    "86 013 231 89" : 'W3',
    "187 205 166 137" : 'W4',
    "243 223 166 137" : 'B1',
    "43 180 230 89" : 'B2',
    "206 93 226 41" : 'B3',
    "218 125 230 89" : 'B4',
    "95 173 230 89" : 'B5',
    "128 03 231 89" : 'B6',
    "250 68 255 41" : 'B7',
    "127 240 92 41" : 'E1',
    "143 121 02 41" : 'E2',
    "143 99 01 41" : 'E3',
    "143 133 87 41" : 'E4',
    "143 05 104 41" : 'C1',
    "158 224 83 32" : 'C2',
    "158 246 166 32" : 'C3',
    "143 101 015 41" : 'C4',
    "143 76 98 41" : 'EXTRA1',
    "143 78 107 41" : 'EXTRA2'

}


# Propiedades y caracteristicas del agente (Ambulancia) que representa este script 
FIRETRUCK = {
    "id" : "FT1",
    "type" : "firefighters",
    "positioning" : "rfid",
    "description" : "Servicio de ambulancia",
    "position" : "",
    "info" : {
        "color" : "#ffffff"    
    }
}

def connect_frontend():
    try:
        frontend = FrontendConnection(HOST_FRONTEND, PORT_FRONTEND) # Conexion con Frontend
        frontend.recognizeAgent(FIRETRUCK)
        print("Se ha conectado con el frontend")
        return frontend
    except:
        print("El servidor frontend no esta conectado")
        return None


def read_rfid(q, sensor, frontend):
    while True:
        tag = sensor.read_RFID()
        q.put("rfid-" + tag)
        print "Tag leido: " + tag
        if frontend and (tag in card_id.keys()):
            frontend.repositionAgent(FIRETRUCK["id"], card_id[tag])
        
def read_distance(q, sensor):
    while True:
        distance = sensor.read_distance()
        q.put("ultrasonic_distance-" + str(distance))
        # print("Distance: " + str(distance))


def take_decision(q, car):
    decision_maker = DecisionMaker(car, LEADER_IP, LEADER_PORT, q)
    decision_maker.process_data()

def line_follower_process(car):
    line = LineFollower(car)
    line.follow_line()

def main():
    frontend = connect_frontend()
    q = Queue()

    BaseManager.register('CarMovement', CarMovement)
    manager = BaseManager()
    manager.start()
    car = manager.CarMovement()

    sensor = Sensors()

    rfid_process = Process(target=read_rfid, args=(q, sensor, frontend, ))
    distance_process = Process(target=read_distance, args=(q, sensor,))
    decision_process = Process(target=take_decision, args=(q, car,))
    line_process = Process(target=line_follower_process, args=(car,))

    rfid_process.start()
    distance_process.start()
    decision_process.start()
    
    time.sleep(5)
    line_process.start()

    try:
        decision_process.join()
        line_process.join()
        rfid_process.join()
        distance_process.join()
    except:
        print "Except del main"
        decision_process.join()
        line_process.join()
        rfid_process.join()
        distance_process.join()
        exit()

if __name__ == '__main__':
    main()
