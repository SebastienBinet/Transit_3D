import requests
# import xml.etree.ElementTree as ET
# import re
import json
from pathlib import Path
import time

RAW_TYPES = {'routeTag':'str', 'lat':0.0, 'lon':0.0, 'secsSinceReport':0, 'heading':0, 'speedKmHr':0}
RAW_KEYS = ['routeTag', 'lat', 'lon', 'secsSinceReport', 'heading', 'speedKmHr']

def xml_multiline_to_list_of_dict(xml_multi_line_string):
    decoded_string = xml_multi_line_string.decode("utf-8")
    result = []
    for line in decoded_string.split('\n'):
        dict_for_line = {}
        splitted_line = line.split(' ')
        for key, example_of_dest_type in RAW_TYPES.items():
            for split_part in splitted_line:
                if split_part.startswith(f'{key}='):
                    value = split_part.split('"')[1]
                    dict_for_line[key] = type(example_of_dest_type)(value)
        if dict_for_line:
            result.append(dict_for_line)
    return result

def xml_multiline_to_csv_multiline_string(xml_multi_line_string, epoch_of_rest_response):
    decoded_string = xml_multi_line_string.decode("utf-8")
    lines_string = decoded_string.split('\n')
    # First line is header, and it includes the 'epochOfRestResponse' value
    keys = RAW_KEYS
    result_multiline_string = ','.join(RAW_KEYS)
    result_multiline_string = result_multiline_string + ',' + f'epochOfRestResponse={epoch_of_rest_response}' + '\n'
    iiii = 0
    for line_string in lines_string[1:]:
        # If the line does not contain the proper information, we simply skip it
        print('a')
        print(line_string)
        print('b')
        string_for_line = ''
        print('c')
        remaining = line_string
        print(f'd {remaining}')
        try:
            for i, key in enumerate(keys):
                print(f'e {remaining}, searching for {key}')
                value, remaining = remaining.split(f' {key}="')[-1].split('"',1)
                print(f'f {key}:{value}, {remaining}')
                string_for_line = string_for_line + (',' if i != 0 else '') + value
                print('f2')
                print(string_for_line)
                print('g')
            print('i')
            result_multiline_string = result_multiline_string + string_for_line + '\n'
        except:
            print('j')
            pass
        print('h')
        print('k')

        if iiii == 3:
            pass
        else:
            iiii = iiii + 1

    print('l')
    return result_multiline_string

def write_bus_positions_in_json_file(busses_info_list_of_dict, busses_info_json_file_path):
    json_string_for_busses_info = json.dumps(busses_info_list_of_dict, indent=2, sort_keys=True)
    with open(busses_info_json_file_path, 'w') as fid:
        fid.write(json_string_for_busses_info)

def write_bus_positions_in_csv_file(busses_info_in_csv_multiline_string, busses_info_csv_file_path):
    with open(busses_info_csv_file_path, 'w') as fid:
        fid.write(busses_info_in_csv_multiline_string)

def get_folder_path_for_raw_opendata():
    return Path('C:/GitHub/Transit_3D/Transit_3D_Raw_OpenData/Current_Busses_Positions')

def get_busses_info_raw_csv_file_path():
    return get_folder_path_for_raw_opendata() / 'Busses_current_position.csv'

def get_current_busses_info_and_write_raw_data_in_csv():
    busses_info_raw_csv_file_path = get_busses_info_raw_csv_file_path()
    request = requests.get("https://retro.umoiq.com/service/publicXMLFeed?command=vehicleLocations&a=stl&t=0")
    busses_info_list_of_dict = xml_multiline_to_list_of_dict(request.content)
    epoch_of_rest_response = int(time.time())
    #print(busses_info_list_of_dict)
    print('+++++++++++++++++++++++++++++++++ 1')
    busses_info_in_csv_multiline_string = xml_multiline_to_csv_multiline_string(request.content, epoch_of_rest_response)
    print('+++++++++++++++++++++++++++++++++ 2')
    print(busses_info_in_csv_multiline_string)
    print('+++++++++++++++++++++++++++++++++ 3')


    write_bus_positions_in_csv_file(busses_info_in_csv_multiline_string, busses_info_raw_csv_file_path)



def debuggg():
    print(xml_to_dict(     b'<?xml version="1.0" encoding="utf-8" ?> <body> <ttt>yyy</ttt> </body>'))
    print(xml_to_dict(     b'<?xml version="1.0" encoding="utf-8" ?> <body rrrr="ssss"/>'))
    print(xml_to_dict(     b'<?xml version="1.0" encoding="utf-8" ?> <body> <ttt>yyy</ttt> <uuuuu>vvvvv</uuuuu> </body>'))
    # print(xml_to_dict(     b'<?xml version="1.0" encoding="utf-8" ?> <body copyright="All data copyright Societe de transport de Laval 2023."/> <vehicle id="1216"
    # print(xml_to_dict(     b'<?xml version="1.0" encoding="utf-8" ?> \n<body copyright="All data copyright Societe de transport de Laval 2023.">\n<vehicle id="1216"
