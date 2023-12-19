import requests
# import xml.etree.ElementTree as ET
# import re
import json

def xml_multiline_to_list_of_dict(xml_multi_line_string):
    decoded_string = xml_multi_line_string.decode("utf-8")
    result = []
    for line in decoded_string.split('\n'):
        dict_for_line = {}
        splitted_line = line.split(' ')
        for key, example_of_dest_type in {'routeTag':'str', 'lat':0.0, 'long':0.0, 'secsSinceReport':0, 'heading':0, 'speedKmHr':0}.items():
            for split_part in splitted_line:
                if split_part.startswith(f'{key}='):
                    value = split_part.split('"')[1]
                    dict_for_line[key] = type(example_of_dest_type)(value)
        if dict_for_line:
            result.append(dict_for_line)
    return result

def xml_multiline_to_csv_multiline_string(xml_multi_line_string):
    decoded_string = xml_multi_line_string.decode("utf-8")
    keys = ['routeTag', 'lat', 'lon', 'secsSinceReport', 'heading', 'speedKmHr']
    result_multiline_string = '- - -'
    for key in keys:
        result_multiline_string = result_multiline_string + ','+ key
    result_multiline_string = result_multiline_string + '\n'
    for line_string in decoded_string.split('\n'):
        # If the line does not contain the proper information, we simply skip it
        print('a')
        try:
            print('b')
            string_for_line = ''
            print('c')
            remaining = line_string
            print(f'd {remaining}')
            for i, key in enumerate(keys):
                print(f'e {remaining}')
                value, remaining = remaining.split(f' {key}="')[1].split('"',1)
                print(f'f {key}:{value}, {remaining}')
                string_for_line = string_for_line + (',' if i != 0 else '') + value
                print('g')
            print('h')
            result_multiline_string = result_multiline_string + string_for_line + '\n'
            print('i')
        except:
            print('j')
            pass
        print('k')
    print('l')
    return result_multiline_string

def write_bus_positions_in_json_file(busses_info_list_of_dict, busses_info_json_file_path):
    json_string_for_busses_info = json.dumps(busses_info_list_of_dict, indent=2, sort_keys=True)
    with open(busses_info_json_file_path, 'w') as fid:
        fid.write(json_string_for_busses_info)

def write_bus_positions_in_csv_file(busses_info_in_csv_multiline_string, busses_info_csv_file_path):
    with open(busses_info_csv_file_path, 'w') as fid:
        fid.write(busses_info_in_csv_multiline_string)


def get_current_busses_info_and_write_in_json():
    busses_info_csv_file_path = 'C:/GitHub/Transit_3D_001/Content/CsvOfCurrentBussesPositions/DT_Busses_current_position.csv'
    request = requests.get("https://retro.umoiq.com/service/publicXMLFeed?command=vehicleLocations&a=stl&t=0")
    print("status code response: ", request.status_code)
    busses_info_list_of_dict = xml_multiline_to_list_of_dict(request.content)
    #print(busses_info_list_of_dict)
    print('+++++++++++++++++++++++++++++++++ 1')
    busses_info_in_csv_multiline_string = xml_multiline_to_csv_multiline_string(request.content)
    print('+++++++++++++++++++++++++++++++++ 2')
    print(busses_info_in_csv_multiline_string)
    print('+++++++++++++++++++++++++++++++++ 3')


    write_bus_positions_in_csv_file(busses_info_in_csv_multiline_string, busses_info_csv_file_path)



def debuggg():
    print(xml_to_dict(     b'<?xml version="1.0" encoding="utf-8" ?> <body> <ttt>yyy</ttt> </body>'))
    print(xml_to_dict(     b'<?xml version="1.0" encoding="utf-8" ?> <body rrrr="ssss"/>'))
    print(xml_to_dict(     b'<?xml version="1.0" encoding="utf-8" ?> <body> <ttt>yyy</ttt> <uuuuu>vvvvv</uuuuu> </body>'))
    # print(xml_to_dict(     b'<?xml version="1.0" encoding="utf-8" ?> <body copyright="All data copyright Societe de transport de Laval 2023."/> <vehicle id="1216"
    # print(xml_to_dict(     b'<?xml version="1.0" encoding="utf-8" ?> \n<body copyright="All data copyright Societe de transport de Laval 2023.">\n<vehicle id="1216"
