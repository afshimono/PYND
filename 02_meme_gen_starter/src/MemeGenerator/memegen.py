from PIL import Image, ImageDraw, ImageFont
import random
import string
import pathlib


class MemeEngine:
    def __init__(self, folder: str):
        self.tmp_folder = folder

    def make_meme(self, img: str, quote_body: str,
                  quote_author: str, width=500) -> str:
    ''' This function will return the path to a meme saved on the self.tmp folder'''

    
        img_obj = Image.open(img)
        width, height = img_obj.size
        if width > 500:
            new_width = 500
            new_height = int(float(height/width)*500)
            img_obj = img_obj.resize((new_width, new_height), Image.NEAREST)

        if quote_body is not None and quote_author is not None:
            message = quote_body + ' ' + quote_author
            draw = ImageDraw.Draw(img_obj)
            font = ImageFont.truetype(str(pathlib.Path('src/_data/fonts/Lato-Black.ttf').absolute()),
                                      size=20)
            draw.text((10, 30), message, font=font, fill='white')

        img_name = ''.join([random.choice(string.ascii_letters +
                            string.digits) for n in range(16)])
        out_path = self.tmp_folder+f"/{img_name}"+img[-4:]
        img_obj.save(out_path)

        return out_path
