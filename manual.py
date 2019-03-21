from car_movement import CarMovement
import click


def main():
    movement = CarMovement()
    speed_level = 1
    angle_level = 1

    key = ''
    while key != 'q':
        key = click.getchar()
        
        if key == 'a':
            movement.turn_left(angle_level)
        elif key == 'd':
            movement.turn_right(angle_level)
        elif key == 's':
            movement.decelerate(speed_level)
        elif key == 'w':
            movement.accelerate(speed_level)
        elif key == ' ':
            movement.brake()
        elif key == 'q':
            movement.stop()

if __name__ == "__main__":
    main()

    

