import os
import random
from abc import ABC, abstractmethod
import docx
from PIL import Image, ImageDraw, ImageFont
from ingestion import Ingestor
from QuoteEngine.quote import QuoteModel
import argparse



def generate_meme(path=None, body=None, author=None):
    """ Generate a meme given an path and a quote """
    img = None
    quote = None

    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    else:
        img = path[0]

    if body is None:
        quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                       './_data/DogQuotes/DogQuotesDOCX.docx',
                       './_data/DogQuotes/DogQuotesPDF.pdf',
                       './_data/DogQuotes/DogQuotesCSV.csv']
        quotes = []
        for f in quote_files:
            quotes.extend(Ingestor.parse(f))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = QuoteModel(body, author)

    meme = MemeEngine('./tmp')
    path = meme.make_meme(img, quote.body, quote.author)
    return path

class MemeEngine:
    def __init__(self,folder:str):
        self.tmp_folder = folder

    def make_meme(self,img:str, quote_body:str, quote_author:str, width=500)->str:
        img = Image.open(img)
        width, height = img.size
        if width > 500:
            new_width = 500
            new_height = int(float(height/width)*500)
            img = img.resize((new_width, new_height), Image.NEAREST)

        if quote_body is not None and quote_author is not None:
            message = quote_body + ' ' + quote_author
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype('_data/Lato-Black.ttf', size=20)
            draw.text((10,30),message,font=font,fill='white')

        out_path = img[:-4]+"out"+img[-4:]
        img.save(out_path)

        return out_path
        
        return 



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="The best Meme Generator of the entire internet.")
    parser.add_argument('path', type=str,help="The path to the image file.")
    parser.add_argument('body', type=str, help="Quote body to add to the image.")
    parser.add_argument('author', type=str, help="Quote author to add to the image.")

    args = parser.parse_args()

    print(generate_meme(args.path, args.body, args.author))
