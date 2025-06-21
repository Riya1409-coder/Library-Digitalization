from prime_generator import get_next_size

def polynomial_hash(z, s):
    # print("ahsdhakidhak", s)
    result = 0
    for i in range(len(s) - 1, -1, -1):
        p = 0
        if s[i] <= 'z' and s[i] >= 'a':
            p = ord(s[i]) - ord('a')
        else:
            p = ord(s[i]) - ord('A') + 26
        result = result * z + p
    # print(result)
    return result

def compression_fn(hash_code, MOD):
    return hash_code % MOD

def double_hash(z, s, c2):
    return c2 - compression_fn(polynomial_hash(z, s), c2)

class HashTable:
    def __init__(self, collision_type, params):
        '''
        Possible collision_type:
            "Chain"     : Use hashing with chaining
            "Linear"    : Use hashing with linear probing
            "Double"    : Use double hashing
        '''
        self.collision_type = collision_type
        self.params = params # for collision type
        self.n = 0
        self.N = self.params[-1]
        if collision_type == "Chain":
            self.table = [[] for _ in range(self.N)]
        else:
            self.table = [None] * self.N
        # print(self.table)
    
    def insert(self, x):
        pass
    
    def find(self, key):
        pass
    
    def get_slot(self, key):
        # print(key)
        return compression_fn(polynomial_hash(self.params[0], key), self.N)
    
    def get_load(self):
        return self.n/self.N
    
    def __str__(self):
        ls = ""
        if self.collision_type == "Chain":
            for i in range(len(self.table)):
                # print(i, "HI")
                for j in range(len(self.table[i])):
                    ls += (self.table[i][j] + (" ; " if j != (len(self.table[i]) - 1) else ""))
                if len(self.table[i]) == 0:
                    ls += ("<EMPTY>")
                if i != len(self.table) - 1:
                    ls += (" | ")
        else:
            for i in range(len(self.table)):
                if self.table[i] != None:
                    ls += (self.table[i] + (" | " if i != len(self.table) - 1 else ""))
                else:
                    ls += ("<EMPTY>" + (" | " if i != len(self.table) - 1 else ""))
        return ls
                
    
    # TO BE USED IN PART 2 (DYNAMIC HASH TABLE)
    def rehash(self):
        pass
    
# IMPLEMENT ALL FUNCTIONS FOR CLASSES BELOW
# IF YOU HAVE IMPLEMENTED A FUNCTION IN HashTable ITSELF, 
# YOU WOULD NOT NEED TO WRITE IT TWICE
    
class HashSet(HashTable):
    
    def insert(self, key):
        slot = self.get_slot(key)
        # print(slot)
        if self.collision_type == "Chain":
            for i in range(len(self.table[slot])):
                # print(self.table)
                if self.table[slot][i] == key:
                    return
            self.table[slot].append(key)
            # print(self.table)
            self.n += 1
            # if key not in self.table[slot]:
            #     self.table[slot].append(key)
            #     self.n += 1
            #     print(self.n)
        else:
            if self.collision_type == "Linear":
                probe = 1
            else:
                probe = double_hash(self.params[1], key, self.params[2])
                # print(probe, "HI")
            j = 0
            while (self.table[(slot + j*probe) % self.N] != None and j < self.N):
                if self.table[(slot + j*probe) % self.N] == key:
                    return
                j += 1
            if j == self.N:
                raise Exception("Table is full")
            self.table[(slot + j*probe) % self.N] = key
            self.n += 1
        # print(self.table)
    def find(self, key):
        slot = self.get_slot(key)
        if self.collision_type == "Chain":
            if key in self.table[slot]:
                return True
        else:
            if self.collision_type == "Linear":
                probe = 1
            else:
                probe = double_hash(self.params[1], key, self.params[2])
                # print(probe, "HI")
            j = 0
            while (self.table[(slot + j*probe) % self.N] != None and j < self.N):
                if self.table[(slot + j*probe) % self.N] == key:
                    return True
                j += 1
        return False

class HashMap(HashTable):
    
    def insert(self, x):
        # x = (key, value)
        # print("BYE", x)
        slot = self.get_slot(x[0])
        # print(slot)
        if self.collision_type == "Chain":
            for i in range(len(self.table[slot])):
                if x[0] == self.table[slot][i]:
                    return
            self.table[slot].append(x)
            self.n += 1
        else:
            if self.collision_type == "Linear":
                probe = 1
            else:
                probe = double_hash(self.params[1], x[0], self.params[2])
            j = 0
            while (self.table[(slot + j*probe) % self.N] != None and j < self.N):
                if self.table[(slot + j*probe) % self.N][0] == x[0]:
                    return
                j += 1
            if j == self.N:
                raise Exception("Table is full")
            self.table[(slot + j*probe) % self.N] = x
            self.n += 1
    
    def find(self, key):
        slot = self.get_slot(key)
        # print(slot)
        if self.collision_type == "Chain":
            for i in range(len(self.table[slot])):
                if self.table[slot][i][0] == key:
                    return self.table[slot][i][1]
        else:
            if self.collision_type == "Linear":
                probe = 1
            else:
                probe = double_hash(self.params[1], key, self.params[2])
            j = 0
            while (self.table[(slot + j*probe) % self.N] != None and j < self.N):
                if self.table[(slot + j*probe) % self.N][0] == key:
                    return self.table[(slot + j*probe) % self.N][1]
                j += 1
        return None
    
    def __str__(self):
        ls = ""
        if self.collision_type == "Chain":
            for i in range(len(self.table)):
                # print(i, "HI")
                for j in range(len(self.table[i])):
                    ls += ('(' + self.table[i][j][0] + ', ' + self.table[i][j][1] + ')' + (" ; " if j != (len(self.table[i]) - 1) else ""))
                if len(self.table[i]) == 0:
                    ls += ("<EMPTY>")
                if i != len(self.table) - 1:
                    ls += (" | ")
        else:
            for i in range(len(self.table)):
                if self.table[i] != None:
                    ls += ('(' + self.table[i][0] + ', ' + self.table[i][1] + ')' + " | " if i != len(self.table) - 1 else "")
                else:
                    ls += ("<EMPTY>" + (" | " if i != len(self.table) - 1 else ""))
        return ls
