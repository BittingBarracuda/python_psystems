from datetime import datetime
from multiset import Multiset
from rule import Rule
from random import choice

import constants as c

def get_datetime():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

class Membrane():
    def __init__(self, id, parent=None, mult_content=Multiset(''), mem_content=[], rules=[]):
        if type(mult_content) != Multiset:
            raise TypeError('Membrane contents should be instance of Multiset!')
        if any([type(mem) != Membrane for mem in mem_content]):
            raise TypeError('Membrane inner membranes should be instances of Membrane!')
        if any([type(rule) != Rule for rule in rules]):
            raise TypeError('Membrane rules should be instances of Rule!')
        if (parent != None) and (type(parent) != Membrane):
            raise TypeError('Parent membrane should be None or instance of Membrane!')
        
        self.multiset = mult_content
        self.parent = parent
        self.membranes = mem_content
        self.rules = sorted(rules, key=lambda x: x.priority, reverse=True)
        self.new_multiset = Multiset('')
        self.new_membranes = Multiset('')
        
        aux = set([rule.priority for rule in self.rules])
        aux_dict = {}
        for priority in aux:
            aux_dict[priority] = [rule for rule in self.rules if rule.priority == priority]
        self.priority_blocks = aux_dict

        self.id = id
        self.membranes_ids = {}
        for membrane in self.membranes:
            self.membranes_ids[membrane.id] = self.membranes_ids.get(membrane.id) + [membrane.id]
        # aux = list(self.membranes_ids.keys()) + [self.id]
        # if len(aux) != len(set(aux)):
        #     raise ValueError('Membrane IDs should be unique! Repeated IDs found...')
        self.steps_computed = 0
    

    def set_parent(self, parent):
        if (parent != None) and (type(parent) != Membrane):
            raise TypeError('Parent membrane should be None or instance of Membrane!')
        self.parent = parent
    
    def set_membranes(self, membranes):
        if any([type(x) != Membrane for x in membranes]):
            raise TypeError('All elements should be instances of Membrane!')
        self.membranes = membranes
        self.membranes_ids = {}
        for membrane in self.membranes:
            self.membranes_ids[membrane.id] = self.membranes_ids.get(membrane.id, []) + [membrane]
    
    def set_multiset(self, multiset):
        if type(multiset) != Multiset:
            raise TypeError('Contents of membrane should be instance of Multiset!')
        self.multiset = multiset
    
    def set_rules(self, rules):
        if type(rules) != dict:
            raise TypeError('')
        
        try:
            current_rules = rules[self.id]
            self.rules = current_rules
        except KeyError:
            pass
        
        for _, mems in self.membranes_ids.items():
            for mem in mems:
                mem.set_rules(rules)
    
    def __get_applicable_rules(self):
        step_1 = [rule for rule in self.rules if self.multiset.contains(rule.lhs)]
        step_2 = [rule for rule in step_1 if (rule.destination in c.DESTS) or (rule.destination in self.membranes_ids.keys())]
        return step_2

    def __is_applicable(self, rule):
        return (self.multiset.contains(rule.lhs) and ((rule.destination in c.DESTS) or (rule.destination in self.membranes_ids.keys())))
    
    def __get_priority_blocks(self, applicable_rules=[]):
        ret = {}
        for rule in applicable_rules:
            ret[rule.priority] = ret.get(rule.priority, []) + [rule]
        return ret
    
    def __apply_rule(self, rule):
        if rule.destination == c.DEST_HERE:
            self.new_multiset = (self.multiset - rule.lhs) + rule.rhs
            # self.new_multiset = self.multiset + rule.rhs
        elif rule.destination == c.DEST_OUT:
            self.new_multiset = self.multiset - rule.lhs
            if self.parent != None:
                self.parent.new_multiset = self.parent.multiset + rule.rhs
        else:
            dest_mem = self.membranes_ids.get(rule.destination, None)
            if dest_mem != None:
                self.new_multiset = self.multiset - rule.lhs
                dest_mem.new_multiset = dest_mem.multiset + rule.rhs

    def __dump_buffers(self):
        self.multiset = self.new_multiset
        self.new_multiset = Multiset('')
    
    def compute_step(self):
        rules = self.__get_applicable_rules()
        rule_blocks = self.__get_priority_blocks(rules)
        rule_blocks = [rule_blocks[prior] for prior in sorted(list(rule_blocks.keys()), reverse=True)]
        
        for rule_block in rule_blocks:
            rule_to_apply = choice(rule_block)
            if self.__is_applicable(rule_to_apply):
                self.__apply_rule(rule_to_apply)
        
        self.__dump_buffers()
        self.steps_computed += 1
        # print(f'[!] Contents of membrane {self.id} at step {self.steps_computed}: {self.multiset.multiset}')
        
        keep_comp = False
        for membrane in self.membranes:
            aux = membrane.compute_step()
            keep_comp = keep_comp or aux
        
        keep_comp = keep_comp or (len(self.multiset) != 0)
        return keep_comp
    
    def degree(self):
        return len(self.membranes)
    
    def depth(self):
        if len(self.membranes) == 0:
            return 0
        else:
            return max([mem.depth() for mem in self.membranes]) + 1
    
    def get_all_membranes(self):
        ret = [self]
        for membrane in self.membranes:
            ret.extend(membrane.get_all_membranes())
        return ret
    
    def run(self, num_steps=1_00):
        for i in range(num_steps):
            print(f'\n[{get_datetime()}] Computing step {i+1}...')
            if not self.compute_step():
                break
