from itertools import zip_longest
from configparser import ConfigParser
import csv

degree_sign = u'\N{DEGREE SIGN}'
minute_sign = '\''
config_obj = ConfigParser()
config_obj.read('config.ini')

CONFIG = config_obj['CONFIG']

input_file_path = CONFIG['path_to_input_file']
output_file_path = CONFIG['path_to_output_file']

array_x = list()
array_y = list()
transformed_x_values = list()
transformed_y_values = list()
y_coordinates = list()
x_coordinates = list()

with open(input_file_path, newline='') as csvfile:
    coordinate = csv.DictReader(csvfile, delimiter=';')
    for cor in coordinate:
        array_x.append(cor['x'])
        array_y.append(cor['y'])


def decdeg2dms(dd):
    is_positive = dd >= 0
    dd = abs(dd)
    minutes, seconds = divmod(dd * 3600, 60)
    degrees, minutes = divmod(minutes, 60)
    degrees = degrees if is_positive else -degrees
    return str(int(degrees))+degree_sign + str(int(minutes)) + minute_sign + str(round(seconds, 3))+'\"'


def check_and_replace_delimiter(new_data):
    new_data = str(new_data).replace(',', '.')
    return float(new_data)


def replace_empty_coordinate(data):
    for x in range(0, len(data)):
        if data[x] == '':
            data[x] = 0.000
    return data


array_x = replace_empty_coordinate(array_x)
array_y = replace_empty_coordinate(array_y)

for cor in array_x:
    cor = check_and_replace_delimiter(cor)
    x_coordinates.append(cor)

for cor in array_y:
    cor = check_and_replace_delimiter(cor)

    y_coordinates.append(cor)

for x in x_coordinates:
    transformed_x_values.append(decdeg2dms(float(x)))

for y in y_coordinates:
    y = decdeg2dms(float(y))
    transformed_y_values.append(y)


fieldnames = ['x', 'y']
rez = zip_longest(transformed_x_values, transformed_y_values, fillvalue='None')

with open(output_file_path, 'w', newline='') as csv_out:
    writer = csv.writer(csv_out, delimiter=';', quotechar='|', quoting=csv.QUOTE_NONE)
    writer.writerow(fieldnames)
    for r in rez:
        print(r)
        writer.writerow(r)
