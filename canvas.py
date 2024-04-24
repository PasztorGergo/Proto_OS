from PIL import ImageDraw, ImageFont, Image

class Canvas:
    def __init__(self,width, height, font_src):
        self.image = Image.new("RGB", (width,height))
        self.w = width
        self.h = height
        self.font_src
        self.d = Image.draw(self.image)
    
    def get_canvas(self):
        return self.image
    
    def get_draw(self):
        return self.d

    def static_text(self, text, size=16, position=(0,0), color=(6, 182, 212)):
        font = ImageFont.truetype(self.font_src, size)
        d.text(position, text, font, color)

    def clear(self):
        self.d.rectangle([(0,0),(w,h)], (0,0,0))

