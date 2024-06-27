from itertools import combinations
from collections import Counter , defaultdict

class HotelContinental:
    def __init__(self, s, n):
        '''s: decoding name
           n: true length'''
        self.name= s
        self.len= n
        self.data_dict= {}
        
    
    def input_validation(self):
        '''check input parameters.'''
        self.name= self.name.strip().lower()
        name_size= len(self.name)  
        if not isinstance(self.name, str):
            raise TabError("Invalid name type.")
        if not isinstance(self.len, int):
            raise TypeError("Invalid True length.")
        if (name_size < 1) or (name_size > 2*(10**5)):
            raise ValueError("Invalid name size.")
        if (self.len < 1) or (self.len > name_size):
            raise ValueError("Invalid True length.")
        return True
    
    
    def chars_validation(self): 
        '''calculate each name's'charachter value.'''
        chars_val= dict(Counter(list(self.name)))
        self.data_dict.update({"chars_val":chars_val})
        return
    
    def combinations(self):
        '''find all true combinations of name's charachters'''
        combs= list(combinations(list(self.name), self.len))
        True_combinations= [list(dict.fromkeys(c)) for c in combs if len(list(dict.fromkeys(c))) == self.len]
        self.data_dict.update({"combinations":True_combinations})
        return
    
    def combinations_validation(self):
        '''calculate combinations value.'''
        chars_val= self.data_dict['chars_val']
        combinations= self.data_dict['combinations']
        combinations_values= [sum([chars_val[v] for v in c]) for c in combinations]
        self.data_dict.update({"combinations_values":combinations_values})
        return 
    
    
    def calculator(self):
        '''calculate number of most valuable combinations.'''
        combinations= self.data_dict['combinations']
        combinations_values= self.data_dict["combinations_values"]
        valuable_combs= [c for c, v in zip(combinations, combinations_values) if v == max(combinations_values)]
        final_result= len(valuable_combs)
        # because we maybe have a big result we calculate remaining final_result to 1-000-000-007
        final_result= final_result % ((10**9)+7)
        self.data_dict.update({"valuable_combs": valuable_combs})
        self.data_dict.update({"final_result": final_result})
        return 
    

    def algorithm(self):
        response= self.input_validation()
        if response:
            self.chars_validation()
            self.combinations()
            self.combinations_validation()
            self.calculator()

        return self.data_dict
    
    
    def run(self):
        response= self.algorithm()
        final_result= response['final_result']
        return final_result
    
    

if __name__ == "__main__":
    tool= HotelContinental(s= "leech",n= 4)
    result= tool.run()



