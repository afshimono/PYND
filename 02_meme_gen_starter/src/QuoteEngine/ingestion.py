from abc import ABC, abstractmethod 
import docx
import pandas as pd
import subprocess
from QuoteEngine.quote import QuoteModel


class IngestionStrategy(ABC):
    @staticmethod
    @abstractmethod
    def parse(file:str):
        pass

    @staticmethod
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
        elif file_ext == 'docx':
            lines = DocIngestor.parse(file)
        elif file_ext == 'txt':
            lines = TxtIngestor.parse(file)
        elif file_ext == 'pdf':
            lines = PdfIngestor.parse(file)
        else:
            raise Exception('Format not supported.')
        return lines
    

class CsvIngestor(IngestionStrategy):
    
    @staticmethod
    def parse(file:str):

        csv_file = pd.read_csv(file)
        result = []
        for index, row in csv_file.iterrows():
            split_line = row.split('-')
            result.append(QuoteModel(split_line[0],split_line[1]))
        return result

class DocIngestor(IngestionStrategy):

    @staticmethod
    def parse(file:str):

        doc = docx.Document(file)
        result = []
        for line in doc.paragraphs:
            split_line = line.text.split('-')
            result.append(QuoteModel(split_line[0],split_line[1]))
        return result

class PdfIngestor(IngestionStrategy):
    @staticmethod
    def parse(file:str):
        tmp = f'./tmp/{random.randint(0,1000000)}.txt'
        call = subprocess.call(['pdftotext', file, tmp])

        file_ref = open(tmp, "r")
        lines = []
        for line in file_ref.readlines():
            split_line = line.split('-')
            result.append(QuoteModel(split_line[0],split_line[1]))
        return lines

class TxtIngestor(IngestionStrategy):
    @staticmethod
    def parse(file:str):
        result = []
        with open(file) as f:
            for line in f:
                split_line = line.split('-')
                result.append(QuoteModel(split_line[0],split_line[1]))
        return result

