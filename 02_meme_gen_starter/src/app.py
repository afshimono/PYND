import random
import os
import requests
from flask import Flask, render_template, abort, request, send_from_directory
from QuoteEngine.ingestion import Ingestor, QuoteModel
from MemeGenerator.memegen import MemeEngine
import glob
import validators
import string


app = Flask(__name__, static_url_path="")
meme = MemeEngine('static')


def setup():
    """ Load all resources """

    quote_files = ['src/_data/DogQuotes/DogQuotesTXT.txt',
                   'src/_data/DogQuotes/DogQuotesDOCX.docx',
                   'src/_data/DogQuotes/DogQuotesPDF.pdf',
                   'src/_data/DogQuotes/DogQuotesCSV.csv']

    quote_list = []
    for file in quote_files:
        quote_list.extend(Ingestor.parse(file))
    quotes = quote_list

    images_path = "src/_data/photos/dog/"
    imgs = glob.glob(images_path+'*.jpg')

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """

    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=f"/{path}")


@app.route('/static/<path:path>')
def send_js(path):
    root_path = os.path.abspath(os.path.dirname(__file__))[:-3]
    return send_from_directory(root_path+'static', path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme """

    # @TODO:
    # 1. Use requests to save the image from the image_url
    #    form param to a temp local file.
    # 2. Use the meme object to generate a meme using this temp
    #    file and the body and author form paramaters.
    # 3. Remove the temporary saved image.

    url = request.form.get('image_url')
    if not validators.url(url):
        raise Exception('Not a valid URL!')
    r = requests.get(url, stream=True)
    if '.jpg' in url:
        img = f'./tmp/img.jpg'
    elif '.png'in url:
        img = f'./tmp/img.png'
    else:
        raise Exception('Unknown image format.')
    if r.status_code == 200:
        with open(img, 'wb') as f:
            for chunk in r.iter_content():
                f.write(chunk)
    body = request.form.get('body')
    author = request.form.get('author')
    if body and author:
        quote = QuoteModel(body, author)
    else:
        quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    os.remove(img)

    return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()
