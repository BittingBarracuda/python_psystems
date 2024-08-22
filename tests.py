from xml_parser import read_config, read_rules
from datetime import datetime
from multiset import Multiset
from membrane import Membrane
from rule import Rule
from tqdm import tqdm
import time

import cProfile
import pstats

def get_datetime():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def membranes_to_txt(membranes):
    with open('membranes.txt', 'w', encoding='utf-8') as file:
        for membrane in tqdm(membranes):
            contents = ';'.join([f'v={x},m={y}' for x, y in membrane.multiset.multiset.items()])
            rules_str = ''
            for rule in membrane.rules:
                lhs_str = ';'.join([f'v={x},m={y}' for x, y in rule.lhs.multiset.items()])
                rhs_str = ';'.join([f'v={x},m={y}' for x, y in rule.rhs.multiset.items()])
                rules_str += f'{lhs_str}:{rhs_str}:{rule.destination}:{rule.priority}*' 
            if membrane.parent != None:
                parent_id = membrane.parent.id
            else:
                parent_id = ''
            file.write(f'membrane_id={membrane.id},parent_id={parent_id},contents=[{contents}], rules=[{rules_str}]\n')

def run_with_cprofile(membrane_1):
    prof = cProfile.Profile()
    prof.run('membrane_1.run(num_steps=1_00)')
    # prof.sort_stats('cumtime')
    prof.dump_stats('output.prof')

    stream = open('output_3.txt', 'w')
    stats = pstats.Stats('output.prof', stream=stream)
    stats.sort_stats('cumtime')
    stats.print_stats()

if __name__ == "__main__":
    print(f'[{get_datetime()}] Starting computation...')
    print(f'[{get_datetime()}] Reading rules file...')
    rules, alphabet = read_rules()
    
    print(f'[{get_datetime()}] Reading config file...')
    membrane_1 = read_config()
    
    membrane_1.set_rules(rules)
    all_membranes = membrane_1.get_all_membranes()
    print(f'[{get_datetime()}] System contains {len(all_membranes)} membranes!')
    
    # print(f'[{get_datetime()}] Writing membranes to txt file...')
    start_time = time.time()
    print(f'[{get_datetime()}] Computing all steps...')
    membrane_1.run(num_steps=1_00)
    # run_with_cprofile(membrane_1)
    print(f'[{get_datetime()}] Ending computation...')
    end_time = time.time()
    print(f'[{get_datetime()}] Time elapsed: {end_time - start_time} seconds!')