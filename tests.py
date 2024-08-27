from xml_parser import read_config, read_rules
from datetime import datetime
from multiset import Multiset
from membrane import Membrane
from rule import Rule
from tqdm import tqdm
import time
import csv

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

def tracked_to_csv(objs_to_track, track):
    with open('output_2.csv', mode='w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file, delimiter=';')
        objs_to_track = sorted(objs_to_track, key=lambda x: x[x.rindex('-')+1:])
        csv_writer.writerow(objs_to_track)
        for aux in tqdm(track):
            csv_writer.writerow([aux[x] for x in objs_to_track])
    
if __name__ == "__main__":
    print(f'[{get_datetime()}] Starting computation...')
    print(f'[{get_datetime()}] Reading rules file...')
    rules, alphabet = read_rules('pru_rules.xml')
    
    print(f'[{get_datetime()}] Reading config file...')
    membrane_1 = read_config('pru_config.xml')
    
    membrane_1.set_rules(rules)
    all_membranes = membrane_1.get_all_membranes()
    print(f'[{get_datetime()}] System contains {len(all_membranes)} membranes!')

    print(f'[{get_datetime()}] Setting objects to track...')
    aux = []
    mems_track = ['eco','zonacomun','zonahospital','zonatrabajo','zonaescuela']
    for z in ['e1', 'e2', 'e3']:
        for y in ['s', 'i', 'in']:
            for x in ['t', 'c', 'e']:
                aux.append(f'h_{x}_{y}_{z}')
    membrane_1.set_objects_to_track(aux)
    membrane_1.set_membranes_to_track(mems_track)
    
    start_time = time.time()
    print(f'[{get_datetime()}] Computing all steps...')
    track = membrane_1.run(num_steps=1_000)
    # run_with_cprofile(membrane_1)
    print(f'[{get_datetime()}] Ending computation...')
    end_time = time.time()
    print(f'[{get_datetime()}] Time elapsed: {end_time - start_time} seconds!')
    
    print(f'[{get_datetime()}] Writing tracked objects to csv file...')
    tracked_to_csv([f'<{obj}-{mem}>' for obj in aux for mem in mems_track], track)