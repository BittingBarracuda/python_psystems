from multiset import Multiset
from rule import Rule
from random import choice

import constants as c

class Membrane():
    def __init__(self, id, parent=None, mult_content=[], mem_content=[], rules=[]):
        if any([type(mult) != Multiset for mult in mult_content]):
            raise TypeError('Membrane contents should be instances of Multiset!')
        if any([type(mem) != Membrane for mem in mem_content]):
            raise TypeError('Membrane inner membranes should be instances of Membrane!')
        if any([type(rule) != Rule for rule in rules]):
            raise TypeError('Membrane rules should be instances of Rule!')
        if (parent != None) and (type(parent) != Membrane):
            raise TypeError('Parent membrane should be None or instance of Membrane!')
        
        self.multiset = sum(mult_content)
        self.parent = parent
        self.membranes = mem_content
        self.rules = sorted(rules, key=lambda x: x.priority, reverse=True)
        self.new_multiset = Multiset('')
        self.new_membranes = Multiset('')
        self.id = id
        self.membranes_ids = {mem.id : mem for mem in self.membranes}
        
        aux = set([rule.priority for rule in self.rules])
        aux_dict = {}
        for priority in aux:
            aux_dict[priority] = [rule for rule in self.rules if rule.priority == priority]
        self.priority_blocks = aux_dict

    
    def __get_applicable_rules(self):
        step_1 = [rule for rule in self.rules if self.multiset.contains(rule.lhs)]
        step_2 = [rule for rule in step_1 if (rule.destination in c.DESTS) or (rule.destination in self.membranes_ids.keys())]
        return step_2

    def __is_applicable(self, rule):
        return (self.multiset.contains(rule.lhs) and ((rule.destination in c.DESTS) or (rule.destination in self.membranes_ids.keys())))
    
    def __get_priority_blocks(self, applicable_rules=[]):
        ret = {}
        for rule in applicable_rules:
            ret[rule.priority] = ret.get(rule.priority, []).extend(rule)
        return ret
    
    def __apply_rule(self, rule):
        if rule.destination == c.DEST_HERE:
            self.new_multiset = (self.multiset - rule.lhs) + rule.rhs
        elif rule.destination == c.DEST_OUT:
            self.new_multiset = self.multiset - rule.lhs
            if self.parent != None:
                self.parent.new_multiset = self.parent.multiset + rule.rhs
        elif rule.destination == c.DEST_IN:
            dest = rule.destination[rule.destination.rindex('-')+1:]
            dest_mem = self.membranes_ids.get(dest, None)
            if dest_mem != None:
                self.new_multiset = self.multiset - rule.lhs
                dest_mem.new_multiset = dest_mem.multiset + rule.rhs

    def __dump_buffers(self):
        self.multiset = self.new_multiset
        self.new_multiset = Multiset('')
    
    def compute_step(self, compute_inner=True):
        rules = self.__get_applicable_rules()
        rule_blocks = self.__get_priority_blocks(rules)
        rule_blocks = [rule_blocks[prior] for prior in sorted(rule_blocks.keys(), reverse=True)]
        
        for rule_block in rule_blocks:
            rule_to_apply = choice(rule_block)
            if self.__is_applicable(rule_to_apply):
                self.__apply_rule(rule_to_apply)
        
        if compute_inner:
            for membrane in self.membranes:
                membrane.compute_step(compute_inner=True)

        self.__dump_buffers()
        if compute_inner:
            for membrane in self.membranes:
                membrane.__dump_buffers()
    
    def degree(self):
        return len(self.membranes)
    
    def depth(self):
        if len(self.membranes) == 0:
            return 0
        else:
            return max([mem.depth() for mem in self.membranes]) + 1
        
