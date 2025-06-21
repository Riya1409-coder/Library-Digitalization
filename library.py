import hash_table as ht

def merge(S1, S2, S):
    """Merge two sorted Python lists S1 and S2 into properly sized list S."""
    i = j = 0
    while i + j < len(S):
        if j == len(S2) or (i < len(S1) and S1[i] < S2[j]):
            S[i + j] = S1[i]  # Copy ith element of S1 as next item of S
            i += 1
        else:
            S[i + j] = S2[j]  # Copy jth element of S2 as next item of S
            j += 1

def merge_sort(S):
    """Sort the elements of Python list S using the merge-sort algorithm."""
    n = len(S)
    if n < 2:
        return  # List is already sorted if it has fewer than 2 elements
    # Divide
    mid = n // 2
    S1 = S[0:mid]  # Copy of first half
    S2 = S[mid:n]  # Copy of second half
    # Conquer (with recursion)
    merge_sort(S1)  # Sort copy of first half
    merge_sort(S2)  # Sort copy of second half
    # Merge results
    merge(S1, S2, S)

def binary_search_books(books_sorted, target_title):
    """Binary search for a book title in the sorted list of books."""
    left, right = 0, len(books_sorted) - 1
    while left <= right:
        mid = (left + right) // 2
        mid_title, distinct_words = books_sorted[mid]  # Unpack title and words
        if mid_title == target_title:
            return distinct_words  # Return list of distinct words if title matches
        elif mid_title < target_title:
            left = mid + 1
        else:
            right = mid - 1
    return None  # Return None if title is not found

def binary_search_words(words_sorted, target_word):
    """Binary search for a word in a sorted list of words."""
    left, right = 0, len(words_sorted) - 1
    while left <= right:
        mid = (left + right) // 2
        if words_sorted[mid] == target_word:
            return True  # Word found
        elif words_sorted[mid] < target_word:
            left = mid + 1
        else:
            right = mid - 1
    return False  # Word not found


class DigitalLibrary:
    # DO NOT CHANGE FUNCTIONS IN THIS BASE CLASS
    def __init__(self):
        pass
    
    def distinct_words(self, book_title):
        pass
    
    def count_distinct_words(self, book_title):
        pass
    
    def search_keyword(self, keyword):
        pass
    
    def print_books(self):
        pass
    
class MuskLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, book_titles, texts):
        self.books_sorted = []
        for i in range(len(book_titles)):
            copy_text = texts[i][:]
            merge_sort(copy_text)
            distinct_text = []
            temp = None
            for j in range(len(copy_text)):
                if copy_text[j] != temp:
                    distinct_text.append(copy_text[j])
                    # words.append(texts[i][j])
                temp = copy_text[j]
            self.books_sorted.append( (book_titles[i], distinct_text))
        # print(self.books_sorted) 
        merge_sort(self.books_sorted)
        
    
    def distinct_words(self, book_title):
        text = binary_search_books(self.books_sorted, book_title)
        return text
    
    def count_distinct_words(self, book_title):
        return len(binary_search_books(self.books_sorted, book_title))
    
    def search_keyword(self, keyword):
        res = []
        for i in range(len(self.books_sorted)):
            word = binary_search_words(self.books_sorted[i][1], keyword)
            if word:
                res.append(self.books_sorted[i][0])
        return res
    
    def print_books(self):
        for i in range(len(self.books_sorted)):
            print(self.books_sorted[i][0] + ": ", end = "")
            for j in range(len(self.books_sorted[i][1])):
                print(self.books_sorted[i][1][j], end = " | " if j != len(self.books_sorted[i][1])-1 else "")
            print()

class JGBLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, name, params):
        '''
        name    : "Jobs", "Gates" or "Bezos"
        params  : Parameters needed for the Hash Table:
            z is the parameter for polynomial accumulation hash
            Use (mod table_size) for compression function
            
            Jobs    -> (z, initial_table_size)
            Gates   -> (z, initial_table_size)
            Bezos   -> (z1, z2, c2, initial_table_size)
                z1 for first hash function
                z2 for second hash function (step size)
                Compression function for second hash: mod c2
        '''
        self.params = params
        if name == "Jobs":
            self.collision_type = "Chain"
        elif name == "Gates":
            self.collision_type = "Linear"
        else:
            self.collision_type = "Double"
        self.books_map = ht.HashMap(self.collision_type, params)
        self.books_list = []
    
    def add_book(self, book_title, text):
        # print("Before", book_title)
        text_map = ht.HashSet(self.collision_type, self.params)
        for word in text:
            text_map.insert(word)
        # print("After", book_title)
        book = (book_title, text_map)
        # print("HI", book)
        old_n = self.books_map.n
        self.books_map.insert(book)
        if self.books_map.n > old_n:
            self.books_list.append(book)
    
    def distinct_words(self, book_title):
        ls = []
        if self.collision_type == "Chain":
            text = self.books_map.find(book_title).table # is a hashset based on chaining
            # print(text)
            temp = None
            for i in range(len(text)):
                for j in range(len(text[i])):
                    if text[i][j] != temp:
                        ls.append(text[i][j])
                    temp = text[i][j]

                # print(self.books_map.find(book_title))
        else:
            text = self.books_map.find(book_title).table
            temp = None
            for i in range(len(text)):
                if text[i] != temp and text[i] != None:
                    ls.append(text[i])
                temp = text[i]
                
        return ls
    
    def count_distinct_words(self, book_title):
        text_map = self.books_map.find(book_title)
        return text_map.n
    
    def search_keyword(self, keyword):
        ls = []
        for book in self.books_list:
            if book[1].find(keyword):
                ls.append(book[0])
        return ls
    
    def print_books(self):
        if self.collision_type == "Chain":
            # print(self.books_map.table)
            for i in range(len(self.books_list)):
                print(self.books_list[i][0] + ": ", end = "") # print book name
                print(self.books_list[i][1]) # print text
        else:
            for i in range(len(self.books_list)):
                if self.books_list[i] != None:
                    print(self.books_list[i][0] + ": ", end = "") # print book name
                    print(self.books_list[i][1]) # print text
        

book_titles = ["Physics", "Mathematics", "Astronomy", "Biology"]
texts = [
    ["force", "mass", "energy", "mass", "acceleration"],
    ["algebra", "calculus", "geometry", "calculus"],
    ["planet", "star", "comet", "planet"],
    ["cell", "biology", "genetics", "evolution", "cell"]
]

# Test MuskLibrary
print("### Testing MuskLibrary ###")
musk_library = MuskLibrary(book_titles, texts)

print("\nTesting distinct_words for 'Physics':")
print(musk_library.distinct_words("Physics"))  # Expected distinct words list for "Physics"

print("\nTesting count_distinct_words for 'Mathematics':")
print(musk_library.count_distinct_words("Mathematics"))  # Expected count of distinct words

print("\nTesting search_keyword 'cell':")
print(musk_library.search_keyword("cell"))  # Should find "Biology"

print("\nTesting print_books:")
musk_library.print_books()  # Expected sorted titles and words within each title


# Test JGBLibrary for different collision handling strategies
# Testing Jobs Library (Chaining)
print("\n### Testing JGBLibrary with 'Jobs' (Chaining) ###")
jobs_library = JGBLibrary("Jobs", [33, 11])
for title, text in zip(book_titles, texts):
    jobs_library.add_book(title, text)

print("\nTesting distinct_words for 'Astronomy':")
print(jobs_library.distinct_words("Astronomy"))  # Expected distinct words for "Astronomy"

print("\nTesting count_distinct_words for 'Biology':")
print(jobs_library.count_distinct_words("Biology"))  # Expected distinct word count

print("\nTesting search_keyword 'geometry':")
print(jobs_library.search_keyword("geometry"))  # Should find "Mathematics"

print("\nTesting print_books:")
jobs_library.print_books()  # Expected titles with associated words

# Testing Gates Library (Linear Probing)
print("\n### Testing JGBLibrary with 'Gates' (Linear Probing) ###")
gates_library = JGBLibrary("Gates", [31, 11])
for title, text in zip(book_titles, texts):
    gates_library.add_book(title, text)

print("\nTesting distinct_words for 'Physics':")
print(gates_library.distinct_words("Physics"))  # Expected distinct words for "Physics"

print("\nTesting count_distinct_words for 'Mathematics':")
print(gates_library.count_distinct_words("Mathematics"))  # Expected count of distinct words

print("\nTesting search_keyword 'star':")
print(gates_library.search_keyword("star"))  # Should find "Astronomy"

print("\nTesting print_books:")
gates_library.print_books()  # Expected titles with associated words

# Testing Bezos Library (Double Hashing)
print("\n### Testing JGBLibrary with 'Bezos' (Double Hashing) ###")
bezos_library = JGBLibrary("Bezos", [5, 7, 3, 11])
for title, text in zip(book_titles, texts):
    bezos_library.add_book(title, text)

print("\nTesting distinct_words for 'Biology':")
print(bezos_library.distinct_words("Biology"))  # Expected distinct words for "Biology"

print("\nTesting count_distinct_words for 'Astronomy':")
print(bezos_library.count_distinct_words("Astronomy"))  # Expected distinct word count

print("\nTesting search_keyword 'evolution':")
print(bezos_library.search_keyword("evolution"))  # Should find "Biology"

print("\nTesting print_books:")
bezos_library.print_books()  # Expected titles with associated words
