exceptions_ref = {
    "AbstractMaximumRange" : {"code" : "400001",
                            "message" : "The abstract section can't be more than 150 words",
                            "p_message" : "The abstract section can't be more than 150 words.\ncurrent abstract words is {abstract_size}"},
    
    "KeywordsMaximumRange" : {"code" : "400002",
                            "message" : "You can't put more than 5 keywords",
                            "p_message" : "You can't put more than 5 keywords.\ncurrent keywords is {keywords_size}"},

    "KeywordsNotSorted" : {"code" : "400003",
                            "message" : "Keywords are not sorted",
                            "p_message" : "Keywords are not sorted.\ncurrent keywords is {keywords}"},
        
    "InvalidPagesCount" : {"code" : "400004",
                            "message" : "The whole paper can't be more than 9 pages",
                            "p_message" : "The whole paper can't be more than 9 pages.\ncurrent pages is {pages_size}"},
    }


class MyBaseException(Exception):
    
    def __init__(self,**kwargs):
        self.code = exceptions_ref[self.__class__.__qualname__]["code"]
        self.message = exceptions_ref[self.__class__.__qualname__]["message"].format(**kwargs)
        self.p_message = exceptions_ref[self.__class__.__qualname__]["p_message"].format(**kwargs)
        super().__init__(self.message)


class AbstractMaximumRange(MyBaseException):
    pass

class KeywordsMaximumRange(MyBaseException):
    pass

class KeywordsNotSorted(MyBaseException):
    pass

class InvalidPagesCount(MyBaseException):
    pass