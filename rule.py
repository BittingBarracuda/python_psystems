from multiset import Multiset
from constants import check_correct_dest, DESTS

class Rule():
    def __init__(self, lhs, rhs, dest='here', priority=1.0):
        if (type(lhs) != Multiset) or (type(rhs) != Multiset):
            raise TypeError('Both left-hand side and right-hand side should be an instance of Multiset!')
        if (type(priority != float)):
            raise TypeError()
        self.lhs = lhs 
        self.rhs = rhs
        if check_correct_dest(dest):
            self.destination = dest
        else:
            raise ValueError(f'Destination should have one of the following formats:\n{DESTS}')