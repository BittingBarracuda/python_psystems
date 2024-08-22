from multiprocessing import cpu_count, Process, Lock
from datetime import datetime
from multiset import Multiset
from rule import Rule
from random import choice, random

import constants as c

def get_datetime():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

class Membrane():
    def __init__(self, id, parent=None, mult_content=Multiset(), mem_content=[], rules=[], alphabet=[]):
        if (type(mult_content) != Multiset):
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
        self.rule_blocks = self.__get_priority_blocks(self.rules)
        aux = []
        for rule_block in self.rule_blocks:
            aux.append([])
            aux[-1] = self.__shared_lhs(rule_block)
        self.rule_blocks_lhs = aux

        self.new_multiset = Multiset()
        self.new_membranes = Multiset()

        self.id = id
        self.membranes_ids = {}
        for membrane in self.membranes:
            self.membranes_ids[membrane.id] = self.membranes_ids.get(membrane.id, []) + [membrane]
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
        if (type(multiset) != Multiset):
            raise TypeError('Contents of membrane should be instance of Multiset')
        self.multiset = multiset
    
    def set_rules(self, rules):
        if type(rules) != dict:
            raise TypeError('')
        
        try:
            current_rules = rules[self.id]
            self.rules = sorted(current_rules, key=lambda x: x.priority, reverse=True)
            self.rule_blocks = self.__get_priority_blocks(self.rules)
            aux = []
            for rule_block in self.rule_blocks:
                aux.append([])
                aux[-1] = self.__shared_lhs(rule_block)
            self.rule_blocks_lhs = aux
        except KeyError:
            pass
        
        for _, mems in self.membranes_ids.items():
            for mem in mems:
                mem.set_rules(rules)
    
    def __get_applicable_rules(self, step):
        step_1 = [rule for rule in self.rule_blocks[step] if self.__is_applicable(rule)]
        return step_1

    def __is_applicable(self, rule):
        return (self.multiset.contains(rule.lhs) and ((rule.destination in c.DESTS) or (rule.destination in self.membranes_ids.keys())))
    
    def __get_priority_blocks(self, applicable_rules=[]):
        ret = []
        if applicable_rules != []:
            current_pr = applicable_rules[0].priority
            ret.append([applicable_rules[0]])
            for i in range(1, len(applicable_rules)):
                if applicable_rules[i].priority == current_pr:
                    ret[-1].append(applicable_rules[i])
                else:
                    current_pr = applicable_rules[i].priority
                    ret.append([applicable_rules[i]])
        return ret
    
    def __apply_rule(self, rule):
        self.multiset.sub(rule.lhs)
        if rule.destination == c.DEST_HERE:
            self.new_multiset.add(rule.rhs)
        elif rule.destination == c.DEST_OUT:
            if self.parent != None:
                self.parent.new_multiset.add(rule.rhs)
        else:
            dest_mem = self.membranes_ids.get(rule.destination, None)
            if dest_mem != None:
                dest_mem.new_multiset.add(rule.rhs)

    def __dump_buffers(self):
        self.multiset.add(self.new_multiset)
        self.new_multiset = Multiset()
    
    def __filter_shared_lhs(self, rules, i):
        ret = []
        rule_block_lhs = self.rule_blocks_lhs[i]
        for rule_block in rule_block_lhs:
            ret.append([])
            for rule in rule_block:
                if rule in rules:
                    ret[-1].append(rule)
        ret = [x for x in ret if x != []]
        return ret
    
    def __shared_lhs(self, rules):
        shared_lhs_blocks = []
        if rules != []:
            shared_lhs_blocks = [[rules[0]]]
            for i in range(1, len(rules)):
                create_new = True
                for block in shared_lhs_blocks:
                    for rule in block:
                        if Multiset.have_common_elems(rules[i].lhs, rule.lhs):
                            block.append(rules[i])
                            create_new = False
                            break
                    if not create_new:
                        break
                if create_new:
                    shared_lhs_blocks.append([rules[i]])
            
            i, n = 0, len(shared_lhs_blocks)
            while i < n:
                j = i + 1
                any_removed = False
                while j < n:
                    removed = False
                    for rule_1 in shared_lhs_blocks[i]:
                        for rule_2 in shared_lhs_blocks[j]:
                            if Multiset.have_common_elems(rule_1.lhs, rule_2.lhs):
                                shared_lhs_blocks[i].extend(shared_lhs_blocks[j])
                                shared_lhs_blocks.remove(shared_lhs_blocks[j])
                                removed, any_removed = True, True
                                break
                        if removed:
                            break
                    n = len(shared_lhs_blocks)
                    if not removed:
                        j = j + 1
                if not any_removed:
                    i = i + 1

        return shared_lhs_blocks

    def __shared_elem(self, rules, elem):
        shared_elems = []
        for rule in rules:
            if elem in rule.lhs:
                shared_elems.append(rule)
        return shared_elems  
    
    def __get_execs(self, k):
        rand = random()
        ke = int(k)
        d = k - ke
        if rand <= d:
            return ke + 1
        else:
            return ke
    
    def __algorithm_1(self):
        n = len(self.rule_blocks)
        if n > 0:
            for i in range(n):
                curr_rules = self.__get_applicable_rules(i) # Obtenemos el bloque i de los bloques de reglas ordenados por prioridad
                if curr_rules != []:
                    rule_blocks_lhs = self.__filter_shared_lhs(curr_rules, i) # Dentro del bloque i, subdividimos de nuevo en bloques de reglas que tienen algún elemento común en su LHS
                    for rule_block_lhs in rule_blocks_lhs: # Recorremos los sub-bloques generados
                        for rule in rule_block_lhs: # Recorremos cada regla del bloque
                            execs = []
                            for elem in rule.lhs.multiset: # Recorremos los elementos de la lhs de la regla actual
                                mult_mem = self.multiset[elem] # Multiplicidad en la membrana actual de elem
                                mult_lhs = rule.lhs[elem] # Multiplicidad en la lhs de la regla actual de elem
                                num_rules = len(self.__shared_elem(rule_block_lhs, elem)) # Número de reglas del bloque actual en las que aparece elem
                                execs.append((mult_mem * rule.pb) / (mult_lhs * num_rules)) # Calculamos el número de aplicaciones de la regla
                            
                            n_exec = min(execs)
                            n_exec = self.__get_execs(n_exec) # Calculamos el número verdadero de ejecuciones en caso de que n_exec sea un número no entero
                            for _ in range(n_exec):
                                self.__apply_rule(rule) # Aplicamos la regla n_exec veces

    def __algorithm_2(self):
        n = len(self.rule_blocks)
        if n > 0:
            for i in range(n):
                curr_rules = self.__get_applicable_rules(i)
                if curr_rules != []:
                    rule_blocks_lhs = self.__filter_shared_lhs(curr_rules, i)
                    for rule_block_lhs in rule_blocks_lhs:
                        subint = [0.0]
                        sum_rule_block = sum([rule.pb for rule in rule_block_lhs])
                        for rule in rule_block_lhs:
                            subint.append(subint[-1] + (rule.pb / sum_rule_block))
                        rand = random()
                        for j in range(1, len(subint)):
                            if (rand >= subint[j - 1]) and (rand < subint[j]):
                                self.__apply_rule(rule_block_lhs[j - 1])
    
    def compute_step(self):
        # n = len(self.rule_blocks)
        # if n > 0:
        #     for i in range(n):
        #         rules = self.__get_applicable_rules(i)
        #         if rules != []:
        #             rule_to_apply = choice(rules)
        #             if self.__is_applicable(rule_to_apply):
        #                 self.__apply_rule(rule_to_apply)
        # self.__algorithm_1()
        self.__algorithm_2()
            
        self.steps_computed += 1 
        keep_comp = False
        for membrane in self.membranes:
            aux = membrane.compute_step()
            keep_comp = keep_comp or aux
        
        self.__dump_buffers()
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
            print(f'[{get_datetime()}] Computing step {i+1}...')
            if not self.compute_step():
                break
