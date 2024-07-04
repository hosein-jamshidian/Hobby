import string 
import numpy as np
import pandas as pd
from collections import Counter


class WordsCheck:
    def __init__(self, text):
        self.data_temp= {}
        self.words= self._spliter(text)
        
        
        
    def _spliter(self, text):
        splited= text.split(" ")
        self.data_temp['1_initial_words']= splited
        return splited


    def recognize_bad_word(self):
        words= self.data_temp['1_initial_words'].copy()
        word_df= pd.DataFrame({'words':words})
        word_df['words_len']=word_df['words'].apply(len) 
        word_df['bad_words_len']= word_df['words'].apply(lambda row : len([c for c in row if c not in string.ascii_letters]))
        word_df['condition']= np.where(word_df['bad_words_len'] < (word_df['words_len']/2), True, False)
        bad_words= word_df[~word_df['condition']]['words'].tolist()
        removed_bad_words= word_df[word_df['condition']]['words'].tolist()
        self.data_temp['2_bad_words']= bad_words
        self.data_temp['3_removed_bad_words']= removed_bad_words
        return 
    
    def clean_bad_character(self):
        words= self.data_temp['3_removed_bad_words'].copy()
        word_df= pd.DataFrame({"words": words})
        word_df['clean_words']= word_df['words'].apply(lambda row : "".join([c for c in row if c in string.ascii_letters]))
        # cleaned_words= ["".join([c for c in word if c in string.ascii_letters]) for word in words ]
        cleaned_words= word_df['clean_words'].tolist()
        self.data_temp['4_cleaned_bad_chars']= cleaned_words
        return 
    
    def fix_font(self):
        words= self.data_temp['4_cleaned_bad_chars'].copy()
        word_df= pd.DataFrame({"words": words})
        word_df['fix_font']= word_df['words'].str.title()
        fixed_fonts= word_df['fix_font'].tolist()
        self.data_temp['5_fixed_fonts']= fixed_fonts
        return 
        
    def counter(self):
        words= self.data_temp['5_fixed_fonts'].copy()
        counted= dict(Counter(words))
        self.data_temp['6_counted_words']= counted
        return counted
        
    def run(self):
        self.recognize_bad_word()
        self.clean_bad_character()
        self.fix_font()
        self.counter()
        return self.data_temp['6_counted_words']


