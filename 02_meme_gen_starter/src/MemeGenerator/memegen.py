from PIL import Image, ImageDraw, ImageFont


class MemeEngine:
    def __init__(self, folder: str):
        self.tmp_folder = folder

    def make_meme(self, img: str, quote_body: str,
                  quote_author: str, width=500) -> str:
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
            draw.text((10, 30), message, font=font, fill='white')

        out_path = img[:-4]+"out"+img[-4:]
        img.save(out_path)

        return out_path
