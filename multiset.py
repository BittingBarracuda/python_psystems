class Multiset():
    def __init__(self, input={}) -> None: 
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
        try:
            # if not (set(other.multiset.keys()) <= set(self.multiset.keys())):
            #     return False
            for key, value in other.multiset.items():
                val_self =  self.multiset[key]
                if val_self < value:
                    return False
        except KeyError:
            return False
        return True
        
    def __add__(self, other):
        ret = self.multiset.copy()
        for key, value in other.multiset.items():
            if key in ret:
                ret[key] += value
            else:
                ret[key] = value
        return Multiset(ret)

    def add(self, other):
        for key, value in other.multiset.items():
            if key in self.multiset:
                self.multiset[key] += value 
            else:
                self.multiset[key] = value
    
    def __sub__(self, other):
        ret = self.multiset.copy()
        for key, value in other.multiset.items():
            ret[key] -= value
        return Multiset(ret)

    def sub(self, other):
        for key, value in other.multiset.items():
            self.multiset[key] -= value

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
    
    @staticmethod
    def have_common_elems(ms_1, ms_2):
        return bool(set(ms_1) & set(ms_2))


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
