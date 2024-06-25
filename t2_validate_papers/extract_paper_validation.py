from quera.t2_validate_papers.local_settings import local_settings
from quera.t2_validate_papers.exceptions import (AbstractMaximumRange,
                                                 KeywordsMaximumRange,
                                                 KeywordsNotSorted,
                                                 InvalidPagesCount)


class ExtractPaperValidation:
    def __init__(self, extracted_paper_fields, fields_words_count):
        self.extracted_paper_fields= extracted_paper_fields
        self.fields_words_count= fields_words_count
        self.responses= {}
        self.local_settings= local_settings
        self.validations_ordering= {'1': self.a_abstract_words_count_condition,
                                    '2': self.b_keywrods_words_count_codition,
                                    '3': self.c_keywords_sorted_condition,
                                    '4': self.d_paper_pages_count_condition}

        
        
    def a_abstract_words_count_condition(self):
        max_count= self.local_settings['maximum_abstract_words_count']
        
        fields_words_count= self.fields_words_count.copy()
        abs_wc= fields_words_count['ABSTRACT']
        if abs_wc > max_count:
            raise AbstractMaximumRange(abstract_size= abs_wc)
        return 1
    
    def b_keywrods_words_count_codition(self):
        max_count= self.local_settings['maximum_keywords_words_count']
        
        fields_words_count= self.fields_words_count.copy()
        kws_wc= fields_words_count['KEYWORDS']
        if kws_wc > max_count:
            raise KeywordsMaximumRange(keywords_size= kws_wc)
        return 1
    
    def c_keywords_sorted_condition(self):
        is_reverse= self.local_settings['keywords_sorted_reverse']
        
        extracted_paper_fields= self.extracted_paper_fields.copy()
        kws= extracted_paper_fields['KEYWORDS']
        if sorted(kws, reverse= is_reverse) != kws:
            raise KeywordsNotSorted(keywords= kws)
        return 1
    
    
    def d_paper_pages_count_condition(self):
        max_count= self.local_settings['maximum_pages_count']
        
        extracted_paper_fields= self.extracted_paper_fields.copy()
        pgs_c= extracted_paper_fields['PAGES_COUNT']
        if pgs_c > max_count:
            raise InvalidPagesCount(pages_size= pgs_c)
        return 1
    
    
    def algorithm(self):
        for i, validator in self.validations_ordering.items():
            self.responses[i]= validator()
        return self.responses

    
    def run(self):
        response= self.algorithm()
        if sum(response.values()) == 4:
            return "200000"
     
         
