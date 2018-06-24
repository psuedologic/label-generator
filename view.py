from PIL import Image, ImageDraw, ImageFont

class View():
    def __init__(self, model, settings, mode="default"):
        self.model = model
        self.settings = settings
        self.mode = mode
        self.image = Image.new("RGB", model.imageSize, model.backgroundColor)
        self.draw = ImageDraw.Draw(self.image, "RGB")
        
    def create_image(self):
        return self.image
