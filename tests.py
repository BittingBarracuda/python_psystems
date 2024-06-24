from xml_parser import read_config, read_rules
from datetime import datetime
from multiset import Multiset
from membrane import Membrane
from rule import Rule
import time

def get_datetime():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

if __name__ == "__main__":
    # rules_1 = [Rule(Multiset('a'), Multiset('b'), 'here', 1.0),
    #            Rule(Multiset('b'), Multiset('b'), '2', 1.0)]
    # rules_2 = [Rule(Multiset('b'), Multiset('c'), 'out', 1.0)]
    # membrane_2 = Membrane('2', None, Multiset(''), [], rules_2)
    # membrane_1 = Membrane('1', None, Multiset('a'*10_000), [membrane_2], rules_1)
    # membrane_2.set_parent(membrane_1)

    start_time = time.time()
    print(f'[! {get_datetime()}] Starting computation...')
    
    print(f'[! {get_datetime()}] Reading config file...')
    membrane_1 = read_config()
   
    print(f'[! {get_datetime()}] Reading rules file...')
    rules, alphabet = read_rules()
    
    membrane_1.set_rules(rules)
    all_membranes = membrane_1.get_all_membranes()
    print(f'[! {get_datetime()}] System contains {len(all_membranes)} membranes!')
    
    print(f'[! {get_datetime()}] Computing all steps...')
    membrane_1.run(num_steps=1_00)
    print(f'[! {get_datetime()}] Ending computation...')
    end_time = time.time()
    print(f'[! {get_datetime()}] Time elapsed: {end_time - start_time} seconds!')