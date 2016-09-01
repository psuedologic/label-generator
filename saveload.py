import json

def load_config(filePath):
    file = open(filePath, 'r')
    file = json.load(file)
    return file