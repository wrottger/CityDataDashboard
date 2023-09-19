import json
from time import sleep
import serial
from serial import SerialException


def get_line():
    for attempt in range(3):
        try:
            with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as ser:
                return ser.readline().decode('utf-8')
        except SerialException:
            sleep(0.2)
    return None


def get_json_data():
    for attempt in range(3):
        line = get_line()
        try:
            line = json.loads(line)
            return line
        except json.decoder.JSONDecodeError:
            continue
        except TypeError:
            print("Couldn't receive data from Serial")
            raise
    return None
