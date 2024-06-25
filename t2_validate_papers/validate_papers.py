import pandas as pd 
import numpy as np

from quera.t2_validate_papers.extract_paper_validation import ExtractPaperValidation

class Operation:
    def __init__(self, paper_file_path, font_size):
        self.path= paper_file_path
        self.font_size= font_size
        self.fields_words_count={}
        self.page_words_count= 0
        self.paper= self.open_paper(path= self.path)
        self.paper_fields= {"TITLE": "",
                           "ABSTRACT": "",
                            "KEYWORDS": "",
                            "INTRODUCTION": "",
                            "BODY": "",
                            "CONCLUSION": "",
                            "REFERENCES": "",
                            "WORDS_COUNT": 0,
                            "PAGES_COUNT": 0
                            }
        self.paper_field_order= {1:"TITLE",
                                2:"ABSTRACT",
                                3:"KEYWORDS",
                                4:"INTRODUCTION",
                                5:"BODY",
                                6:"CONCLUSION",
                                7:"REFERENCES",
                                }
        
    def open_paper(self, path):
        with open(path) as file :
            paper= file.read()
        return paper
            
    def keywords(self):
        keywords= self.paper_fields['KEYWORDS'].split(",")
        tune_keywords= [word.strip() for word in keywords]
        tune_keywords.sort()
        return tune_keywords
    
    def references(self):
        references= self.paper_fields['REFERENCES']
        refs= []
        end_at, counter= 0, 0
        while end_at != -1:
            counter+=1
            current_ref= f"[{counter}]"
            start_at= references.find(current_ref)+len(current_ref)+1
            next_ref= f"[{counter+1}]"
            end_at= references.find(next_ref)
            refs.append(references[start_at: end_at].replace("\n","").strip())
            
        return refs
    
    def _field_words_count(self, field):
        text= self.paper_fields[field]
        text= text.replace(",", " ")
        words= text.split(" ")
        words= [word for word in words if word not in ["", " "]]
        size= len(words)
        return size

    def words_count(self):
        for key in self.paper_field_order:
            field= self.paper_field_order[key]
            self.fields_words_count[field]= self._field_words_count(field)
        
        total_words_count= sum(self.fields_words_count.values())
        return total_words_count
    
    
    def pages_count(self):
        base_page_words_count, base_font_size= 512, 16
        self.font_size= round(self.font_size, 1)
        self.page_words_count= np.ceil((self.font_size * base_page_words_count ) / base_font_size)
        total_words_count= sum(self.fields_words_count.values())
        dev= total_words_count / self.page_words_count
        total_pages= np.ceil(dev)
        return total_pages
    
        
    def initial_extract_papers(self):
        total_fields= len(self.paper_field_order.keys())
        for key in self.paper_field_order:
            current_field= self.paper_field_order[key]
            start_at= self.paper.find(current_field)+len(current_field)+1
            if key <= (total_fields - 1):
                next_field= self.paper_field_order[key+1]
                end_at= self.paper.find(next_field)
            else:
                end_at= -1
            self.paper_fields[current_field]= self.paper[start_at: end_at].replace("\n","").strip()
        return self.paper_fields
    
    
    def extract_papers(self):
        paper_fields= self.initial_extract_papers()
        self.paper_fields['WORDS_COUNT']= self.words_count()
        self.paper_fields['PAGES_COUNT']= self.pages_count()
        self.paper_fields['KEYWORDS']= self.keywords()
        self.paper_fields['REFERENCES']= self.references()
        return self.paper_fields
    
    
    def validation(self):
        tool= ExtractPaperValidation(self.paper_fields, self.fields_words_count)
        response= tool.run()
        return response
        
        
    def run(self):
        res= self.extract_papers()
        validation_response= self.validation()
        if validation_response == "200000":
            return res
        

path= 'H:/sherkat_project_3.9.7/quera/t2_validate_papers/paper1_sample.txt'

tool= Operation(paper_file_path= path, font_size= 16)
res= tool.run()

