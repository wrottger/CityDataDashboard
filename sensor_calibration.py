from statistics import mean
from serial_utils import get_json_data


def get_mean_value(sensor_outputs):
    mean_values = list()
    for sensor in sensor_outputs:
        mean_values.append(str(mean(sensor)))
    return mean_values


def main():
    datapoints = 8 * [list()]

    for i in range(80):
        line = get_json_data()
        for idx in range(8):
            datapoints[idx].append(line['data'][idx])
    mean_values = get_mean_value(datapoints)
    with open('data/calibrated_traffic', 'w') as f:
        f.write(", ".join(mean_values))


if __name__ == '__main__':
    main()
