from PIL import Image, ImageDraw, ImageFont


class MemeEngine:
    def __init__(self, folder: str):
        self.tmp_folder = folder

    def make_meme(self, img: str, quote_body: str,
                  quote_author: str, width=500) -> str:
        img_obj = Image.open(img)
        width, height = img_obj.size
        if width > 500:
            new_width = 500
            new_height = int(float(height/width)*500)
            img_obj = img_obj.resize((new_width, new_height), Image.NEAREST)

        if quote_body is not None and quote_author is not None:
            message = quote_body + ' ' + quote_author
            draw = ImageDraw.Draw(img_obj)
            font = ImageFont.truetype('src/_data/fonts/Lato-Black.ttf',
                                      size=20)
            draw.text((10, 30), message, font=font, fill='white')

        out_path = self.tmp_folder+"/out"+img[-4:]
        img_obj.save(out_path)

        return out_path
