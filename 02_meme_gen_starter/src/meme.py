import os
import random
from abc import ABC, abstractmethod
import docx
from PIL import Image, ImageDraw, ImageFont
from QuoteEngine.ingestion import Ingestor
from QuoteEngine.quote import QuoteModel
from MemeGenerator.memegen import MemeEngine
import argparse
import pathlib


def generate_meme(path=None, body=None, author=None):
    """ Generate a meme given an path and a quote .
        Will load a list of saved quotes, a list of saved dog pics,
        and if no quote or pic is provided, will use one from the lists randomly."""

    img = None
    quote = None

    if path is None:
        current_path = pathlib.Path("src/_data/photos/dog").absolute()
        images = str(current_path)
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    else:
        img = path[0]

    if body is None:
        quote_files = [str(pathlib.Path('src/_data/DogQuotes/DogQuotesTXT.txt').absolute()),
                       str(pathlib.Path('src/_data/DogQuotes/DogQuotesDOCX.docx').absolute()),
                       str(pathlib.Path('src/_data/DogQuotes/DogQuotesPDF.pdf').absolute()),
                       str(pathlib.Path('src/_data/DogQuotes/DogQuotesCSV.csv').absolute())]
        quotes = []
        ingestor = Ingestor()
        for f in quote_files:
            quotes.extend(ingestor.parse(f))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = QuoteModel(body, author)

    meme = MemeEngine('tmp')
    path = meme.make_meme(img, quote.body, quote.author)
    return path


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="The best Meme \
         Generator of the entire internet.")
    parser.add_argument('--path', help="The path to the image file.",
                        default=None)
    parser.add_argument('--body', help="Quote body to add to the image.",
                        default=None)
    parser.add_argument('--author', help="Quote author to add to the image.",
                        default=None)

    args = parser.parse_args()

    print(str(pathlib.Path(generate_meme(args.path, args.body, args.author)).absolute()))
