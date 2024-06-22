from multiset import Multiset
from constants import DESTS

class Rule():
    def __init__(self, lhs, rhs, dest='here', priority=1.0):
        if (type(lhs) != Multiset) or (type(rhs) != Multiset):
            raise TypeError('Both left-hand side and right-hand side should be an instance of Multiset!')
        if (type(priority != float)):
            raise TypeError('Priority should be defined as a decimal number!')
        self.lhs = lhs 
        self.rhs = rhs
        self.destination = dest
        self.priority = priority