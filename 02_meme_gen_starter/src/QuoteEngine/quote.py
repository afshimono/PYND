class QuoteModel:
    ''' The base definition of a quote: a body and an author'''
    
    def __init__(self,body:str,author:str):
        self.body = body
        self.author = author


