import math
import time
from car_movement import CarMovement
from sensors import Sensors

class LineFollower:

    stop_distance = {
        0: 10,
        1: 1,
        2: 2,
        3: 3,
        4: 4,
        5: 5,
        6: 6,
        7: 7,
        8: 8,
        9: 9,
        10: 10
    }
    
    def __init__(self, car):
        self.sensors = Sensors()
        self.references = [-1,-1,-1,-1,-1]
        self.car = car
        self.calibration()

    def calculate_reference(self, white_reference, black_reference):
        for i in range(0, 5):
            self.references[i] = (white_reference[i] - black_reference[i])/2 + black_reference[i]
        print self.references

    def calibration(self):
        print "Calibration..."
        print "  Black test:"
        black_reference = self.sensors.test_color_line()
        print 
        print "  White test:"
        white_reference = self.sensors.test_color_line()
        self.calculate_reference(white_reference, black_reference)

    def follow_line(self):
        while True:
            digital_list = self.sensors.read_digital_line(self.references)
            if digital_list[0] == 1:
                self.car.set_speed_level(5)
                self.car.set_angle(60)
            if digital_list[1] == 1:
                self.car.set_speed_level(7)
                self.car.set_angle(75)
            if digital_list[2] == 1:
                self.car.set_speed_level(9)
                self.fw.turn_straight()
            if digital_list[3] == 1:
                self.car.set_speed_level(7)
                self.car.set_angle(105)
            if digital_list[4] == 1:
                self.car.set_speed_level(5)
                self.car.set_angle(120)


def main():
    car = CarMovement()
    line_follower = LineFollower(car)
    #try:
    time.sleep(3)
    line_follower.follow_line()
    #except:
    #    print "Stopped!!!"
    #    car.stop()

if __name__ == '__main__':
    main()
