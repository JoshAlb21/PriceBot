import datetime
import unicodedata
import functools
import pathlib
import os
import json
from typing import List

def extract_float_from_price(price:str) -> float:
    price = price.replace('€', '')
    price = price.replace('.', '')
    price = price.replace('.', '')
    price = price.replace(',', '.')
    price = float(price)
    return price

def get_current_time():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    return current_time

def log_error(error):
    with open('error_log.txt', 'w') as f: 
        f.write(f'{get_current_time()}: {error}\n')
    
def convert_back_to_euro(line:str) -> str:
    new_line = unicodedata.normalize("NFKD", line)
    return new_line

def check_lists(old_list, new_list):
    
    checked = False
    if len(new_list) == len(old_list):
        if functools.reduce(lambda x, y: x and y, map(lambda a, b: a == b, new_list, old_list), True): #TODO check. not all cases covered??
            print(f"{get_current_time()} Both List are same")
            checked = True
    return checked

def load_config_from_file(config_file:str) -> dict:
    current_path = pathlib.Path(__file__).parent.resolve()
    config_path = os.path.join(current_path, config_file)
    with open(config_path) as json_data_file:
        config = json.load(json_data_file)

    return config

def read_logfiles(log_file:str) -> List[str]:
    with open(log_file, 'r') as f:
        lines = f.readlines()
        lines = [line.rstrip() for line in lines ]
        lines = [convert_back_to_euro(line) for line in lines ]

    return lines