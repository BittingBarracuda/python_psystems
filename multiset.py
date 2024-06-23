class Multiset():
    def __init__(self, input) -> None:
        self.multiset = {}
        if type(input) == str:
            keys = list(input)
            for key in keys:
                self.multiset[key] = self.multiset.get(key, 0) + 1
        elif type(input) == dict:
            if any([type(x) != str for x in input.keys()]):
                raise TypeError('Keys for dictionary should be strings!')
            if any([type(x) != int for x in input.values()]):
                raise TypeError('Values for dictionary should be integers!')
            self.multiset = input
            
            to_del = []
            for key in self.multiset.keys():
                if self.multiset[key] == 0:
                    to_del.append(key)
            for key in to_del:
                del self.multiset[key]  
        elif type(input) == list:
            for key, mult in input:
                self.multiset[key] = self.multiset.get(key, 0) + mult
    
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
        keys = self.__get_all_keys(other)
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

               

    
