from collections import deque
from statistics import mean
import time
from serial_utils import get_json_data

with open("data/calibrated_traffic", "r") as file:
    string_values = file.readline().split(sep=", ")
normal_mean = list(map(float, string_values))


def add_traffic():
    with open("data/traffic_counter", 'r') as f:
        number = int(float(f.readline()))
    number += 1
    with open("data/traffic_counter", 'w') as f:
        f.write(str(number))


last_time = time.time()
last_traffic = 0


def car_passed(traffic_volume):
    global last_traffic, last_time

    if (last_traffic == 0 and
            traffic_volume != 0 and
            time.time() - last_time > 7):
        return True
    else:
        return False


def loop():
    global normal_mean
    traffic_volume = 0

    json = get_json_data()
    for i in range(8):
        if (json['data'][i] - normal_mean[i]) > 2:
            traffic_volume += 1
    with open("data/traffic_volume", 'w') as f:
        f.write(str(traffic_volume))
    with open("data/loudness", 'w') as f:
        f.write(str(mean(json['data'][-2:])))
    if car_passed(traffic_volume):
        add_traffic()


if __name__ == '__main__':
    while True:
        loop()
