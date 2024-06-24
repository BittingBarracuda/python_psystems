import xml.etree.ElementTree as etree
from bs4 import BeautifulSoup
from membrane import Membrane 
from multiset import Multiset, MultisetNp
from rule import Rule
import os

import constants as c

FILES_DIR = 'files'

def config_get_info(membrane_xml, membrane_obj, np_arr=False, alphabet=[]):
    msets, membs = [], []
    for child in membrane_xml:
        if child.tag == 'BO':
            msets.append((child.attrib['v'], int(child.attrib['m'])))
        elif child.tag == 'membrane':
            if np_arr:
                aux_mem = Membrane(id=child.attrib['id'],
                                parent=membrane_obj,
                                mult_content=MultisetNp(''),
                                mem_content=[],
                                rules=[],
                                alphabet=alphabet)
            else:
                aux_mem = Membrane(id=child.attrib['id'],
                                parent=membrane_obj,
                                mult_content=Multiset(''),
                                mem_content=[],
                                rules=[])
            membs.append(aux_mem)
            config_get_info(child, aux_mem, np_arr, alphabet)
    if np_arr:
        membrane_obj.set_multiset(MultisetNp(msets, alphabet))
    else:
        membrane_obj.set_multiset(Multiset(msets))
    membrane_obj.set_membranes(membs)

def read_config(alphabet=[]):
    tree = etree.parse(os.path.join(FILES_DIR, 'config.xml'))
    root_mem_xml = tree.getroot()[0][0]
    
    root_mem = Membrane(id=root_mem_xml.attrib['id'], 
                        parent=None,
                        mult_content=Multiset(''), 
                        mem_content=[],
                        rules=[])
    config_get_info(root_mem_xml, root_mem, False, alphabet)

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

def rules_get_info(membrane_xml, np_arr=False, alphabet=[]):
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

            if np_arr:
                rule = Rule(lhs=MultisetNp(lhs_ms, alphabet),
                            rhs=MultisetNp(rhs_ms, alphabet),
                            dest=dest,
                            priority=pr)
            else:
                rule = Rule(lhs=Multiset(lhs_ms), 
                            rhs=Multiset(rhs_ms),
                            dest=dest,
                            priority=pr)
            rules.append(rule)
        
        elif child.tag == 'membrane':
            aux = aux | rules_get_info(child, np_arr, alphabet)
    try:
        rules = {membrane_xml.attrib['ID']: rules}
    except KeyError:
        rules = {}
    
    return (rules | aux)


def read_rules():
    tree = etree.parse(os.path.join(FILES_DIR, 'rules.xml'))
    
    alphabet = []
    root_alphabet = tree.getroot()[0]
    for child in root_alphabet:
        if child.tag == 'v':
            alphabet.append(child.attrib['value'])
    
    complete_alphabet('rules.xml', alphabet)
    complete_alphabet('config.xml', alphabet)
    root_mem_xml = tree.getroot()[1]
    return rules_get_info(root_mem_xml, False, alphabet), alphabet
