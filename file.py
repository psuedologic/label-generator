import json

class File:
    def __init__(self, filePath):
        self.filePath = filePath
        self.load_file()
        
    def load_file(self):
        self.file = open(self.filePath, 'r')
        self.file = json.load(self.file)
        self.config = self.file

def load_settings():
    settings = {"showGrid":True}
    return settings
    
def load_image(imagePath):
    pass