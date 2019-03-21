from multiprocessing import Queue
from agent import Agent
import json, time
import logging

logger = logging.getLogger('loggerito')
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler("log")
handler.setLevel(logging.INFO)
logger.addHandler(handler)

class DecisionMaker:
    
    GREEN = 'green'
    YELLOW = 'yellow'
    RED = 'red'
    
    STOP_DISTANCES = {
        0: 20, 
        1: 10, 
        2: 12, 
        3: 13, 
        4: 14, 
        5: 15, 
        6: 16, 
        7: 17, 
        8: 18, 
        9: 19, 
        10: 20
    }

    route_0 = {
        "01 84 254 41": "go_straight",
        "255 014 167 137": "go_straight",
        "143 99 01 41": "go_straight",
        "193 125 198 89": "go_straight",
        "127 240 92 41": "turn_left"
    }

    route_1 = {
        "01 84 254 41": "turn_left", 
        "137 40 167 137": "turn_right", 
        "143 05 104 41": "turn_left"
    }

    def __init__(self, car, leader_ip, leader_port, queue):
        self.queue = queue
        self.car = car
        self.leader_ip = leader_ip
        self.leader_port = leader_port
        self.last_rfid = ''
        self.agent = Agent(False, self.leader_ip, self.leader_port)
        self.trafficlight_positions = {}
        self.trafficlight_positions = self.agent.request_leader_info(self.agent.TRAFFIC_LIGHT_REQUEST)
        self.nested_leaders = self.agent.request_leader_info(self.agent.NESTED_LEADERS_REQUEST)
        self.current_route = self.route_0
        self.emergency = False

        
    def process_data(self):
        last_trafficlight_state = ''
        distance = 100000
        while True:
            queue_data = self.queue.get()
            data = queue_data.split('-')
            if data[0] == 'rfid':
                self.last_rfid = data[1]
                print "Last rfid " + self.last_rfid
            elif data[0] == 'ultrasonic_distance':
                distance = int(data[1])
            self.check_stop(distance)
            self.check_route()
            self.check_change_leader()

    def change_leader(self):
        self.agent.make_connection(self.leader_ip, self.leader_port)
        self.trafficlight_positions = self.agent.request_leader_info(self.agent.TRAFFIC_LIGHT_REQUEST)
        self.nested_leaders = self.agent.request_leader_info(self.agent.NESTED_LEADERS_REQUEST)

    def check_stop(self, distance):
        if distance <= self.STOP_DISTANCES[self.car.get_speed_level()]:
            self.car.stop()
        elif self.last_rfid in self.trafficlight_positions.keys():
            trafficlight = self.trafficlight_positions[self.last_rfid]
            if not self.emergency:
                self.agent.send_message(self.agent.REQUEST_TRAFFIC_LIGHT_STATUS + '_' + trafficlight)
                traffic_light_status = self.agent.receive_message()
                print "trafficlight status: " + traffic_light_status
                if traffic_light_status == self.RED or traffic_light_status == self.YELLOW:
                    self.car.stop()
                elif self.car.is_car_stopped():
                    self.car.run()
            else:
                self.agent.send_message(self.agent.SET_TRAFFIC_LIGHT_SERVICE + "-" + trafficlight)
                print "Envio al leader que ponga el semaforo " + trafficlight + " en estado de emergencia"
        elif self.car.is_car_stopped():
        	self.car.run()

    def check_route(self):
        if not self.car.is_car_stopped() and self.last_rfid in self.current_route.keys():
            action = self.current_route[self.last_rfid]
            print("Action: " + action)
            logger.info("Action: " + action)
            if action == "turn_left":
                print 'Voy a girar a la izquierda'
                self.car.left_corner()
            elif action == "turn_right":
                print 'Voy a girar a la derecha'
                self.car.right_corner()
            elif action == "go_straight":
                print "Continuo recto"
                self.car.go_straight()
            self.last_rfid = ''

    def check_change_leader(self):
        # if self.last_rfid in self.nested_leaders.keys():
            # connection = self.nested_leaders[self.last_rfid]
            # self.leader_ip = connection[0]
            # self.leader_port = connection[1]
            # self.change_leader()
        pass

    def is_emergency(self):
        return self.emergency

    def set_emergency(self, state):
        self.emergency = state
