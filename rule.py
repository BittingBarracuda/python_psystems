from multiset import Multiset
from constants import DESTS

class Rule():
    def __init__(self, lhs, rhs, dest='here', priority=1.0):
        if not ((type(lhs) == Multiset) and (type(rhs) == Multiset)):
            raise TypeError('Both left-hand side and right-hand side should be an instance of Multiset!')
        if (type(priority) != float):
            raise TypeError('Priority should be defined as a decimal number!')
        if (type(dest) != str):
            raise TypeError('Destination should be a string!')
        
        self.lhs = lhs 
        self.rhs = rhs
        self.destination = dest
        self.priority = priority
    
    def __str__(self):
        return f'{self.lhs.__str__()} ---> {self.rhs.__str__()} - (dest:{self.destination}, pr:{self.priority})'
    
    def __repr__(self):
        return self.__str__()