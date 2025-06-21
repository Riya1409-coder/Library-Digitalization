from hash_table import HashSet, HashMap
from prime_generator import get_next_size

class DynamicHashSet(HashSet):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        new_size = get_next_size()
        prev_table = self.table
        self.N = new_size
        self.n = 0
        if self.collision_type == "Chain":
            self.table = [[] for _ in range(new_size)]
            self.params = (self.params[0], new_size)
            for l in prev_table:
                for x in l:
                    super().insert(x)
        else:
            if self.collision_type == "Linear":
                self.params = (self.params[0], new_size)
            else:
                self.params = (self.params[0], self.params[1], self.params[2], new_size)
            self.table = [None] * new_size
            for x in prev_table:
                if x:
                    super().insert(x)
        
        
    def insert(self, x):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(x)
        
        if self.get_load() >= 0.5:
            self.rehash()
            
            
class DynamicHashMap(HashMap):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        new_size = get_next_size()
        prev_table = self.table
        self.N = new_size
        self.n = 0
        if self.collision_type == "Chain":
            self.table = [[] for _ in range(new_size)]
            for l in prev_table:
                for x in l:
                    super().insert(x)
        else:
            self.table = [None] * new_size
            for x in prev_table:
                if x:
                    super().insert(x)
        
    def insert(self, key):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(key)
        
        if self.get_load() >= 0.5:
            self.rehash()