from statistics import mean

from serial_utils import get_json_data

with open("data/calibrated_traffic", "r") as file:
    string_values = file.readline().split(sep=", ")
normal_mean = list(map(float, string_values))


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
        f.write(mean(json['data'][-2:]))


if __name__ == '__main__':
    while True:
        loop()
