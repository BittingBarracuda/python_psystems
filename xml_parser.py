import xml.etree.ElementTree as etree
from membrane import Membrane 
from multiset import Multiset
from rule import Rule
import os

import constants as c

FILES_DIR = 'files'

def config_get_info(membrane_xml, membrane_obj):
    msets, membs = [], []
    for child in membrane_xml:
        if child.tag == 'BO':
            msets.append((child.attrib['v'], int(child.attrib['m'])))
        elif child.tag == 'membrane':
            aux_mem = Membrane(id=child.attrib['id'],
                               parent=membrane_obj,
                               mult_content=Multiset(''),
                               mem_content=[],
                               rules=[])
            membs.append(aux_mem)
            config_get_info(child, aux_mem)

    membrane_obj.set_multiset(Multiset(msets))
    membrane_obj.set_membranes(membs)

def read_config():
    tree = etree.parse(os.path.join(FILES_DIR, 'config.xml'))
    root_mem_xml = tree.getroot()[0][0]
    
    root_mem = Membrane(id=root_mem_xml.attrib['id'], 
                        parent=None,
                        mult_content=Multiset(''), 
                        mem_content=[],
                        rules=[])
    config_get_info(root_mem_xml, root_mem)

    return root_mem

def rules_get_info(membrane_xml):
    rules = []
    aux = {}
    for child in membrane_xml:
        if child.tag == 'rBO':
            lhs, rhs = child[0], []
            try:
                rhs = child[1]
            except IndexError:
                pass
            
            lhs_ms, rhs_ms = [], []
            for obj in lhs:
                if obj.tag == 'BO':
                    lhs_ms.append((obj.attrib['v'], int(obj.attrib['m'])))
            for obj in rhs:
                if obj.tag == 'BO':
                    rhs_ms.append((obj.attrib['v'], int(obj.attrib['m'])))
            
            if rhs != []:
                move = rhs.attrib['move']
                if (move != None): 
                    move = move.lower()
                    if (move in c.DESTS):
                        dest = move
                    else:
                        dest = rhs.attrib['destination']
            else:
                dest = 'here'
            pr = float(child.attrib['pr'])

            rule = Rule(lhs=Multiset(lhs_ms), 
                        rhs=Multiset(rhs_ms),
                        dest=dest,
                        priority=pr)
            rules.append(rule)
        
        elif child.tag == 'membrane':
            aux = aux | rules_get_info(child)
    try:
        rules = {membrane_xml.attrib['ID']: rules}
    except KeyError:
        rules = {}
    
    return (rules | aux)


def read_rules():
    tree = etree.parse(os.path.join(FILES_DIR, 'rules.xml'))
    root_mem_xml = tree.getroot()[1]
    return rules_get_info(root_mem_xml)


if __name__ == "__main__":
    read_config()