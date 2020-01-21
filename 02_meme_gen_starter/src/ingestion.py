from abc import ABC, abstractmethod 
import docx
import pandas as pd


class IngestionStrategy(ABC):
    @staticmethod
    @abstractmethod
    def parse(file:str):
        pass

    def check_input(acceptable:list, extension:str):
        if extension not in acceptable:
            raise Exception('File format not supported.')

class Ingestor:
    @staticmethod
    def parse(file:str):
        lines = []
        file_ext = file.split('.')[-1]
        if file_ext == 'csv':
            lines = CsvIngestor.parse(file)
        elif file_ext == 'doc' or file_ext == 'txt':
            lines = DocIngestor.parse(file)
        elif file_ext == 'pdf':
            lines = PdfIngestor.parse(file)
        print(lines)
    

class CsvIngestor(IngestionStrategy):
    suported_types=['csv']
    
    @staticmethod
    def parse(file:str):
        super.check_input(suported_types,file.split('.')[-1])

        csv_file = pd.read_csv(file)
        result = []
        for index, row in csv_file.iterrows():
            result.append(row)

class DocIngestor(IngestionStrategy):
    suported_types=['doc','docx','txt']

    @staticmethod
    def parse(file:str):
        super.check_input(suported_types,file.split('.')[-1])

        doc = docx.Document(file)
        result = []
        for line in doc.paragraphs:
            result.append(line)
        return result

class PdfIngestor(IngestionStrategy):
    @staticmethod
    def parse(file:str):
        pass


