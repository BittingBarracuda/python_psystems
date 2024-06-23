from xml_parser import read_config, read_rules
from multiset import Multiset
from membrane import Membrane
from rule import Rule
import time

if __name__ == "__main__":
    # rules_1 = [Rule(Multiset('a'), Multiset('b'), 'here', 1.0),
    #            Rule(Multiset('b'), Multiset('b'), '2', 1.0)]
    # rules_2 = [Rule(Multiset('b'), Multiset('c'), 'out', 1.0)]
    # membrane_2 = Membrane('2', None, Multiset(''), [], rules_2)
    # membrane_1 = Membrane('1', None, Multiset('a'*10_000), [membrane_2], rules_1)
    # membrane_2.set_parent(membrane_1)

    start_time = time.time()
    print(f'[!] Starting computation...')
    print(f'[!] Reading config file...')
    membrane_1 = read_config()
    print(f'[!] Reading rules file...')
    rules = read_rules()
    membrane_1.set_rules(rules)
    print(f'[!] Computing all steps...')
    # membrane_1.run(num_steps=100_000)
    print(f'[!] Ending computation...')
    end_time = time.time()
    print(f'[!] Time elapsed: {end_time - start_time} seconds!')