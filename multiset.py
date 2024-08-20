import numpy as np
import scipy as sp

class Multiset():
    def __init__(self, input={}) -> None:
        # self.multiset = {}
        # if any([type(x) != str for x in input.keys()]):
        #     raise TypeError('Keys for dictionary should be strings!')
        # if any([type(x) != int for x in input.values()]):
        #     raise TypeError('Values for dictionary should be integers!')
        # self.multiset = input    
        self.multiset = {x:y for x, y in input.items() if y != 0}
    
    def support(self):
        return self.multiset.keys()  
    
    def cardinality(self):
        return self.__len__()
    
    def union(self, other):
        return self.__add__(other)
    
    def __get_all_keys(self, other):
        return set(list(self.multiset.keys()) + list(other.multiset.keys()))
    
    def contains(self, other):
        if type(other) != Multiset:
            raise TypeError('Contains operation can only be applied between Multisets!')
        # keys = self.__get_all_keys(other)
        keys = list(other.multiset.keys())
        return all([other.multiset.get(key, 0) <= self.multiset.get(key, 0) for key in keys])
        
    def __add__(self, other):
        if type(other) != Multiset:
            raise TypeError('Multisets can only be sumed with other Multiset!')
        keys = self.__get_all_keys(other)
        return Multiset({key : (self.multiset.get(key, 0) + other.multiset.get(key, 0)) for key in keys}) 
    
    def __sub__(self, other):
        if type(other) != Multiset:
            raise TypeError('Multisets can only be substracted with other Multiset!')
        keys = self.__get_all_keys(other)
        return Multiset({key: max(self.multiset.get(key, 0) - other.multiset.get(key, 0), 0) for key in keys})

    def __mul__(self, other):
        if type(other) != int:
            raise TypeError('Multisets can only be multiplied by integers!')
        return Multiset({key : other * value for key, value in self.multiset.items()})  

    def __len__(self):
        return sum(self.multiset.values())   
    
    def __getitem__(self, key):
        return self.multiset[key]
      
    def __setitem__(self, key, item):
        if type(key) != str:
            raise TypeError('Keys should be strings!')
        if type(item) != int:
            raise TypeError('Values should be integers!')
        self.multiset[key] = item

    def __contains__(self, item):
        return item in self.multiset.keys()
    
    def __str__(self):
        return ''.join([key * value for key, value in self.multiset.items()])
    
    def __repr__(self):
        return self.__str__()

    def items(self):
        return self.multiset.items()


# class MultisetNp():
#     def __init__(self, input=[], alphabet=[], np_arr=np.array([])):
#         if np_arr.size != 0:
#             self.arr = np_arr
#         else:
#             n = len(alphabet)
#             self.arr = np.zeros(shape=(1, n), dtype=int)
#             for key, value in input:
#                 index = alphabet.index(key)
#                 self.arr[0][index] = value
#             self.arr = sp.sparse.csr_array(self.arr)
#         # self.alphabet = alphabet
    
#     def contains(self, other):
#         aux = self.arr - other.arr
#         return aux[aux < 0].size == 0

#     def __add__(self, other):
#         aux = self.arr + other.arr
#         return MultisetNp(np_arr=aux) 
    
#     def __sub__(self, other):
#         aux = self.arr - other.arr
#         aux[aux < 0] = 0
#         return MultisetNp(np_arr=aux)
    
#     def __len__(self):
#         return self.arr[self.arr > 0].size
