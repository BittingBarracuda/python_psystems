import xml.etree.ElementTree as etree
from bs4 import BeautifulSoup
from membrane import Membrane 
from multiset import Multiset
from rule import Rule
import os

import constants as c

FILES_DIR = 'files'

def tuple_list_to_dict(list):
    aux = {}
    for key, value in list:
        aux[key] = aux.get(key, 0) + value
    return aux

def config_get_info(membrane_xml, membrane_obj):
    msets, membs = [], []
    for child in membrane_xml:
        if child.tag == 'BO':
            msets.append((child.attrib['v'], int(child.attrib['m'])))
        elif child.tag == 'membrane':
            aux_mem = Membrane(id=child.attrib['id'],
                            parent=membrane_obj,
                            mult_content=Multiset(),
                            mem_content=[],
                            rules=[])
            membs.append(aux_mem)
            config_get_info(child, aux_mem)

    membrane_obj.set_multiset(Multiset(tuple_list_to_dict(msets)))
    membrane_obj.set_membranes(membs)

def read_config(file_name, alphabet=[]):
    tree = etree.parse(os.path.join(FILES_DIR, file_name))
    root_mem_xml = tree.getroot()[0][0]
    
    root_mem = Membrane(id=root_mem_xml.attrib['id'], 
                        parent=None,
                        mult_content=Multiset(), 
                        mem_content=[],
                        rules=[])
    config_get_info(root_mem_xml, root_mem)

    return root_mem

def complete_alphabet(file, alphabet=[]):
    with open(os.path.join(FILES_DIR, file)) as file:
        data = file.read()
    soup = BeautifulSoup(data, 'xml')
    bos = soup.find_all('BO')
    values = [bo['v'] for bo in bos]
    for value in values:
        if value not in alphabet:
            alphabet.append(value)

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
            pb = float(child.attrib['pb'])

            rule = Rule(lhs=Multiset(tuple_list_to_dict(lhs_ms)), 
                        rhs=Multiset(tuple_list_to_dict(rhs_ms)),
                        dest=dest,
                        priority=pr,
                        pb=pb)
            rules.append(rule)
        
        elif child.tag == 'membrane':
            aux = aux | rules_get_info(child)
    try:
        rules = {membrane_xml.attrib['ID']: rules}
    except KeyError:
        rules = {}
    
    return (rules | aux)


def read_rules(file_name):
    tree = etree.parse(os.path.join(FILES_DIR, file_name))
    
    alphabet = []
    root_alphabet = tree.getroot()[0]
    for child in root_alphabet:
        if child.tag == 'v':
            alphabet.append(child.attrib['value'])
    
    complete_alphabet('rules.xml', alphabet)
    complete_alphabet('config.xml', alphabet)
    root_mem_xml = tree.getroot()[1]
    return rules_get_info(root_mem_xml), alphabet
