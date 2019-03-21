from frontend_connection import FrontendConnection
from requests.exceptions import ConnectionError
from threading import Thread
from leader import Leader
import serial
import json

 
HOST_FRONTEND = "10.0.2.16"
PORT_FRONTEND = 3001

traffic_light_dict = {
    "01 84 254 41": "TW1",
    "255 014 167 137" : "TS1"
    # "143 76 98 41": "TW1" 
}

nested_leaders = {
    "218 125 230 89": ("10.9.41.216", 5000),
    "137 40 167 137": ("10.9.41.216", 5000)
}

traffic_light_status = {
    "TW1" : "",
    "TW2" : "",
    "TS1" : ""
}

traffic_light_color = {
    "1000" : "green",
    "0100" : "yellow",
    "0010" : "red",
    "0001" : "blue"
}

# Propiedades y caracteristicas de los agentes que representa este script
tw1 = {
    "id" : "TW1", 
    "type" : "trafficlight",
    "positioning" : "rfid",
    "x" : 139,
    "y" : 480,
    "direction" : "left",
    "orientation" : "v",
    "status" : "green",
    "description" : "Semaforo",
    "attributtes" : {
        "role" : "agent",
        "leader" : "TW2",
        "resources" : {
            "CPU" : "1,5GHz",
            "Chipset" : "DDR4",
            "DISK" : 5
        },
        "iots" : {}
    } 
}

tw2 = {
    "id" : "TW2", 
    "type" : "trafficlight",
    "positioning" : "rfid", 
    "x" : 261,
    "y" : 447,
    "long" : 60/2,
    "direction" : "left",
    "orientation" : "h",
    "status" : "red",
    "description" : "Semaforo",
    "attributtes" : {
        "role" : "leader",
        "leader" : "",
        "resources" : {
            "CPU" : "1,5GHz",
            "Chipset" : "DDR4",
            "DISK" : 5
        },
        "iots" : {}
    }
}

ts1 = {
    "id" : "TS1", 
    "type" : "trafficlight",
    "positioning" : "rfid",
    "x" : 591,
    "y" : 817,
    "direction" : "right",
    "orientation" : "h",
    "status" : "red",
    "description" : "Semaforo",
    "attributtes" : {
        "role" : "agent",
        "leader" : "TW2",
        "resources" : {
            "CPU" : "1,5GHz",
            "Chipset" : "DDR4",
            "DISK" : 500
        },
        "iots" : {}
    }
}

def connect_frontend():
    try:
        frontend = FrontendConnection(HOST_FRONTEND, PORT_FRONTEND) # Conexion con Frontend
        frontend.recognizeAgent(tw1)
        frontend.recognizeAgent(tw2)
        frontend.recognizeAgent(ts1)
        print("Se ha conectado con el frontend")
        return frontend
    except:
        print("El servidor frontend no esta conectado")
        return None

def accept_connection():
    global leader
    leader.accept_connection()

def receive_request():
    global leader, traffic_light_status, arduinos
    while True:
        agent_id, msg = leader.request_received()
        if agent_id != None and msg != None: 
            print("El mensaje es ", msg)
            if "set_traffic_light_service" in msg:
                data = msg.split('-')
                traffic_light = data[1][-1:]
                print("Pongo " + traffic_ligth + " a " + status)
                # a que arduino le envio el mensaje para poner el semaforo
                # arduino.write(traffic_light + '1002')
            elif msg == Leader.TRAFFIC_LIGHT_REQUEST:
                info = json.dumps(traffic_light_dict, ensure_ascii=False)
                print("leader info:"+str(info))
                leader.answer_request(info, agent_id)
                print("enviado")
            elif msg == Leader.NESTED_LEADERS_REQUEST:
                info = json.dumps(nested_leaders, ensure_ascii=False)
                print("leader info:"+str(info))
                leader.answer_request(info, agent_id)
            elif msg.split("_")[0] == Leader.REQUEST_TRAFFIC_LIGHT_STATUS:
                traffic_light = msg.split("_")[1]
                print("contesto: ", traffic_light_status[traffic_light])
                leader.answer_request(traffic_light_status[traffic_light], agent_id)
                #print("traffic_light_status de " + traffic_light +" = "+traffic_light_status[traffic_light])
                print("contestado")
            

def read_arduino_traffic_light_status(arduino, frontend):
    while True:
        try:
            lectura = arduino.readline().decode().rstrip()
            traffic_light, status= lectura.split('-')
            traffic_light_status[traffic_light] = traffic_light_color[status]
            if frontend:
                frontend.sendStatus(traffic_light, status)
            print("traffic_light_status de " + traffic_light +" = "+traffic_light_status[traffic_light])
        except:
            pass

def read_traffic_light_status():
    global arduinos, frontend
    
    #arduinos = [arduino1, arduino2]
    for arduino in arduinos:
        thread = Thread(target=read_arduino_traffic_light_status, args=(arduino, frontend))
        thread.start()


def main():
    th_connection = Thread(target=accept_connection)
    th_request = Thread(target=receive_request)
    th_light_status = Thread(target=read_traffic_light_status)
    th_connection.start()
    th_request.start()
    th_light_status.start()

if __name__ == '__main__':
    arduino1 = serial.Serial('/dev/ttyACM0', 9600)
    #arduino2 = serial.Serial('/dev/ttyACM1', 9600)
    arduinos = [arduino1]
    
    leader = Leader(True, "10.10.176.123", 5000)
    frontend = connect_frontend() # Conexion con FrontEnd
    main()
