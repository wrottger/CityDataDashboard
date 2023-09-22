from collections import deque
from statistics import mean
import time
from serial_utils import get_json_data

with open("data/traffic_counter", 'w') as f:
    f.write("0")


def add_traffic():
    with open("data/traffic_counter", 'r') as f:
        number = int(float(f.readline()))
    number += 1
    print(number)
    with open("data/traffic_counter", 'w') as f:
        f.write(str(number))


last_time = time.time()
last_traffic = deque([0] * 10, maxlen=10)


def car_passed(traffic_volume):
    global last_traffic, last_time

    last_traffic.append(traffic_volume)
    if last_traffic.count(1) == 5 and last_traffic.count(0) == 5 and last_traffic[0] == 1:
        return True
    else:
        return False


def loop():
    traffic = 0
    json = get_json_data()
    if json['data'][0] != 0:
        traffic = 1
    with open("data/traffic_volume", 'w') as f:
        f.write(str(traffic))
    with open("data/loudness", 'w') as f:
        f.write(str(mean(json['data'][-2:])))
    if car_passed(traffic):
        add_traffic()


if __name__ == '__main__':
    while True:
        loop()
