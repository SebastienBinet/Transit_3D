import json
from pathlib import Path
import time

RAW_TYPES = {'routeTag':'str', 'lat':0.0, 'lon':0.0, 'secsSinceReport':0, 'heading':0, 'speedKmHr':0}
RAW_KEYS = ['routeTag', 'lat', 'lon', 'secsSinceReport', 'heading', 'speedKmHr']


def get_folder_path_for_raw_opendata():
    return Path('C:/GitHub/Transit_3D/Transit_3D_Raw_OpenData/Current_Busses_Positions')

def get_folder_path_for_partially_processed_opendata():
    return Path('C:/GitHub/Transit_3D/Transit_3D_Raw_OpenData')

def get_busses_info_raw_csv_file_path():
    return get_folder_path_for_raw_opendata() / 'Busses_current_position.csv'

def get_unreal_xyz_busses_info_csv_file_path():
    return 'C:/GitHub/Transit_3D/Transit_3D_UnrealProject/Content/CsvOfCurrentBussesPositionsToDisplay/DT_CurrentBusInfo.csv'

def read_geo_bus_positions_in_csv_file(busses_info_raw_csv_file_path):
    """Returns a list of dict"""
    ret_geo_busses_info_as_list_of_dict = []
    with open(busses_info_raw_csv_file_path, 'r') as fid:
        json_string_for_busses_info = fid.read()
    json_lines = json_string_for_busses_info.split('\n')
    header_line = json_lines[0]
    epoch_of_rest_response = int(header_line.split('epochOfRestResponse=')[-1])
    for json_line in json_lines[1:]:
        if not json_line: continue
        info_line = json_line.split(',')
        print(f'info_line: {info_line}')
        line_dict = {}
        for i, key in enumerate(RAW_KEYS):
            # Extract and cast to proper type.
            line_dict[key] = type(RAW_TYPES[key])(info_line[i])
        ret_geo_busses_info_as_list_of_dict.append(line_dict)
    return ret_geo_busses_info_as_list_of_dict, epoch_of_rest_response

def get_current_lat_lon_epoch():
    """Return lat,long,epoch to use as zero"""
    return {'lat':45.525, 'lon':-73.6, 'epoch':int(time.time())}

def zeroise_geo(geo_busses_info_as_list_of_dict, epoch_of_rest_response, app_start_lat_lon_epoch):
    ret_zeroised_geo_busses_info_as_list_of_dict = []
    for bus_info in geo_busses_info_as_list_of_dict:
        zeroised_geo_bus_info = {}
        zeroised_geo_bus_info['routeTag'] = bus_info['routeTag']
        zeroised_geo_bus_info['heading'] = bus_info['heading']
        zeroised_geo_bus_info['speedKmHr'] = bus_info['speedKmHr']
        zeroised_geo_bus_info['lat'] = bus_info['lat'] - app_start_lat_lon_epoch['lat']
        zeroised_geo_bus_info['lon'] = bus_info['lon'] -  app_start_lat_lon_epoch['lon']
        zeroised_geo_bus_info['minutes_from_app_started'] = epoch_of_rest_response - app_start_lat_lon_epoch['epoch'] - bus_info['secsSinceReport']
        ret_zeroised_geo_busses_info_as_list_of_dict.append(zeroised_geo_bus_info)
    return ret_zeroised_geo_busses_info_as_list_of_dict

def unrealize_zeroised_geo(zeroised_geo_busses_info_as_list_of_dict):
    ret_unreal_xyz_buses_info_as_list_of_dict = []
    for zeroised in zeroised_geo_busses_info_as_list_of_dict:
        unreal_xyz_bus_info = {
            'routeTag': zeroised['routeTag'],
            'headingInDegreeFromNorth': zeroised['heading'],
            'speedInMeterPerMinute': zeroised['speedKmHr'] * 60 / 1000,
            'x': zeroised['lon'] * 111139,
            'y': zeroised['lat'] * 111139,
            'z': zeroised['minutes_from_app_started'] / 60,
        }
        ret_unreal_xyz_buses_info_as_list_of_dict.append(unreal_xyz_bus_info)
    print(f'unreal_xyz_bus_info: {ret_unreal_xyz_buses_info_as_list_of_dict}')
    return ret_unreal_xyz_buses_info_as_list_of_dict

def write_xyz_format_buses_info_in_csv_file(busses_info_xyz_csv_file_path, unreal_xyz_busses_info_as_list_of_dict):
    print('33333333333333333333333333333333')
    print(unreal_xyz_busses_info_as_list_of_dict)

    result_multiline_string = ','.join(['index', 'routeTag', 'headingInDegreeFromNorth', 'speedInMeterPerMinute', '           x', '           y', '           z'])
    for index, bus_info in enumerate(sorted(unreal_xyz_busses_info_as_list_of_dict, key=lambda x: x['routeTag'])):
        routeTag = bus_info['routeTag']
        headingInDegreeFromNorth = bus_info['headingInDegreeFromNorth']
        speedInMeterPerMinute = bus_info['speedInMeterPerMinute']
        x = bus_info['x']
        y = bus_info['y']
        z = bus_info['z']
        bus_info_line_string = ','.join([
            str(f'{index:>5}'),
            str(f'{routeTag:>8}'),
            str(f'{headingInDegreeFromNorth:>24}'),
            str(f'{speedInMeterPerMinute:>21.1f}'),
            str(f'{x:>+12.2f}'),
            str(f'{y:>+12.2f}'),
            str(f'{z:>+12.2f}'),
        ])
        result_multiline_string = '\n'.join([result_multiline_string, bus_info_line_string])
    print('44444444444444444444444444444444')
    print(result_multiline_string)
    with open(busses_info_xyz_csv_file_path, 'w') as fid:
        fid.write(result_multiline_string)

def convert(app_start_lat_lon_epoch):
    busses_info_raw_csv_file_path = get_busses_info_raw_csv_file_path()
    geo_busses_info_as_list_of_dict, epoch_of_rest_response = read_geo_bus_positions_in_csv_file(busses_info_raw_csv_file_path)
    print('445')
    print(geo_busses_info_as_list_of_dict)
    print('446')
    zeroised_geo_busses_info_as_list_of_dict = zeroise_geo(geo_busses_info_as_list_of_dict, epoch_of_rest_response, app_start_lat_lon_epoch)
    print('447')
    unreal_xyz_busses_info_as_list_of_dict = unrealize_zeroised_geo(zeroised_geo_busses_info_as_list_of_dict)
    print('448')
    print(unreal_xyz_busses_info_as_list_of_dict)
    print('449')
    unreal_xyz_busses_info_csv_file_path = get_unreal_xyz_busses_info_csv_file_path()
    write_xyz_format_buses_info_in_csv_file(unreal_xyz_busses_info_csv_file_path, unreal_xyz_busses_info_as_list_of_dict)
