from abc import ABC, abstractmethod
import docx
import pandas as pd
import subprocess
from QuoteEngine.quote import QuoteModel
import random
import pathlib


class IngestionInterface(ABC):
    ''' Interface containing an abstract method which must be implemented by children,
        and a classmethod that will check class list list_of_acceptable for file extensions. '''

    list_of_acceptable = []

    @abstractmethod
    def parse(file: str):
        pass

    @classmethod
    def check_input(cls, file: str):
        if file.split('.')[-1] not in cls.list_of_acceptable:
            raise Exception('File format not supported.')
        else: 
            return True


class Ingestor:
    ''' Encapsulation of all ingestors to provide a simpler interface. '''

    def __init__(self):
        self.pdf_ingestor = PdfIngestor()
        self.txt_ingestor = TxtIngestor()
        self.csv_ingestor = CsvIngestor()
        self.docx_ingestor = DocIngestor()

    def parse(self,file: str):
        ''' Function that will choose the best parser based on the file extension. '''
        lines = []
        file_ext = file.split('.')[-1]
        if file_ext == 'csv':
            lines = self.csv_ingestor.parse(file)
        elif file_ext == 'docx':
            lines = self.docx_ingestor.parse(file)
        elif file_ext == 'txt':
            lines = self.txt_ingestor.parse(file)
        elif file_ext == 'pdf':
            lines = self.pdf_ingestor.parse(file)
        else:
            raise Exception('Format not supported.')
        return lines


class CsvIngestor(IngestionInterface):
    ''' Ingestor for CSV files.'''

    list_of_acceptable = ['csv']
    def parse(self,file: str):
        if self.check_input(file):
            csv_file = pd.read_csv(file)
            result = []
            for index, row in csv_file.iterrows():
                result.append(QuoteModel(row['body'], row['author']))
            return result


class DocIngestor(IngestionInterface):
    ''' Ingestor for docx files. '''

    list_of_acceptable = ['docx']
    def parse(self,file: str):
        if self.check_input(file):
            doc = docx.Document(file)
            result = []
            for line in doc.paragraphs:
                split_line = line.text.split('-')
                if len(split_line) > 1:
                    result.append(QuoteModel(split_line[0], split_line[1]))
            return result


class PdfIngestor(IngestionInterface):
    ''' Ingestor for PDF files. '''

    list_of_acceptable = ['pdf']
    def parse(self,file: str):
        if self.check_input(file):
            current_path = pathlib.Path().absolute()
            tmp = f'tmp/{random.randint(0,1000000)}.txt'
            call = subprocess.call(['pdftotext', file, tmp])
            file_ref = open(tmp, "r")
            lines = []
            for line in file_ref.readlines():
                split_line = line.split('-')
                if len(split_line) > 1:
                    lines.append(QuoteModel(split_line[0], split_line[1]))
            return lines


class TxtIngestor(IngestionInterface):
    ''' Ingestor for txt files. '''
    
    list_of_acceptable = ['txt']
    def parse(self,file: str):
        if self.check_input(file):
            result = []
            with open(file) as f:
                for line in f:
                    split_line = line.split('-')
                    result.append(QuoteModel(split_line[0], split_line[1]))
            return result
