import textwrap
import csv


class Model(object):
    def __init__(self, config):
        #Creates a record of what variables are added from config, 
        #and then adds the variables to the classes namespace
        self.config_variables = [i for i in config]
        for i in config:
            self.__dict__[i] = config[i]
        
        self.update_layout()
        
    def update_layout(self):
        self.imageSize = (int(self.paperSize[0] * self.pixelsPerInch),
        int(self.paperSize[1] * self.pixelsPerInch))
    
    def generate_card_coordinates(self):
      cards_coordinates = []
      current_coord = (self.xMin, self.yMin)
      cards_coordinates.append(current_coord)
      
      for row in range(self.rows):
          current_coord = (current_coord[0] + self.cardSize[0], current_coord[1])
          cards_coordinates.append(current_coord)
          
          current_coord = (current_coord[0] - self.cardSize[0],
                           current_coord[1] + self.cardSize[1])
          cards_coordinates.append(current_coord)
      cards_coordinates.pop(10)
      
      self.cards_coordinates = cards_coordinates 


#Derived Settings
def derive_config(config):
    logo = Image.open(config["logoPath"])
    logo = logo.resize(config["logoSize"], Image.LANCZOS) #328, 243
    config["fontPath"] = config["resourcePath"] + config["font"]
    config["dataPath"] = config["resourcePath"] + config["defaultData"]
    
    #config["imageSize"] = (int(config["paperSize"][0] * config["pixelsPerInch"]), Transferred
    #                       int(config["paperSize"][1] * config["pixelsPerInch"]))
    config["marginSize"] = 1 * config["pixelsPerInch"]
    config["topMargin"] = int(config["topMargin"] * config["pixelsPerInch"])
    config["sideMargin"] = int(config["sideMargin"] * config["pixelsPerInch"])

    config["xMin"] = config["sideMargin"] + (config["logoMargin"] * 3 // 4) # added logo margin to calibrate to my printer
    config["xMax"] = config["imageSize"][0] - config["sideMargin"] - (config["logoMargin"] * 3 // 4)
    config["yMin"] = config["topMargin"] + config["logoMargin"]
    config["yMax"] = config["imageSize"][1] - config["topMargin"] - config["logoMargin"]

    config["pixelsInRow"] = ((config["yMax"] - config["yMin"]) // config["rows"])
    config["cardSize"] = (((config["xMax"] - config["xMin"]) // 2), config["pixelsInRow"])

    config["font10"] = ImageFont.truetype(config["fontPath"], 100)
    config["font8"] = ImageFont.truetype(config["fontPath"], 100)

    #image = Image.new("RGB", config["imageSize"], config["backgroundColor"]) transferred to View
    #draw = ImageDraw.Draw(image, "RGB")

    config["logoTranslation"] = (config["logoMargin"], config["cardSize"][1] - logo.size[1] - config["logoMargin"])

    # Format        [(UPPER, LEFT), (LOWER, RIGHT), (SIZE)]
    config["titleTextbox"] = [(config["textMargin"] + config["xMin"], config["textMargin"] + config["yMin"]),
                     (config["cardSize"][0] - config["textMargin"] + config["xMin"], config["cardSize"][1] - logo.size[1] - config["logoMargin"] * 2 - config["textMargin"] + config["yMin"]),
                     ()]
    config["titleTextbox"][2] = (config["titleTextbox"][1][0] - config["titleTextbox"][0][0], config["titleTextbox"][1][1] - config["titleTextbox"][0][1])
    config["nameTextbox"] = [(logo.size[0] + config["logoMargin"] * 3 + config["xMin"], config["cardSize"][1] - logo.size[1] - config["logoMargin"] * 2 + config["textMargin"] + config["yMin"]),
                    (config["cardSize"][0] - config["textMargin"] * 2 + config["xMin"], config["cardSize"][1] - config["textMargin"] * 2 + config["yMin"]),
                    ()]
    config["nameTextbox"][2] = (config["nameTextbox"][1][0] - config["nameTextbox"][0][0], config["nameTextbox"][1][1] - config["nameTextbox"][0][1])
        
    #TO REMOVE - DEPRECIATED
    config["titleTranslation"] = (config["textMargin"], config["textMargin"])
    config["nameTranslation"] = (logo.size[0] + config["logoMargin"] * 2, config["cardSize"][1] - config["textMargin"] * 2 - logo.size[1] )
    
    return config, image, draw, logo

#Generates a list containing the upper left coordinate of each card.
def generate_card_coordinates():
    cards_coordinates = []
    current_coord = (config["xMin"], config["yMin"])
    cards_coordinates.append(current_coord)
    for row in range(config["rows"]):
        current_coord = (current_coord[0] + config["cardSize"][0], current_coord[1])
        cards_coordinates.append(current_coord)
        
        current_coord = (current_coord[0] - config["cardSize"][0],
                         current_coord[1] + config["cardSize"][1])
        cards_coordinates.append(current_coord)
    cards_coordinates.pop(10)
    return cards_coordinates 

def draw_static(cards_coordinates):
    #Draws the Vertical Lines
    draw.line([(config["xMin"], config["yMin"]),
               (config["xMin"], config["yMax"])],
               fill="red", width=config["borderWidth"])
    draw.line([(config["xMax"], config["yMin"]),
               (config["xMax"], config["yMax"])],
               fill="red", width=config["borderWidth"])
    draw.line([(((config["xMin"] + config["xMax"]) // 2), config["yMin"]),
               (((config["xMin"] + config["xMax"]) // 2), config["yMax"])],
                 fill="red", width=config["borderWidth"])

    #Draws the Horizontal Lines
    draw.line([(config["xMin"] - config["borderWidth"] // 2, config["yMin"]),
               (config["xMax"] + config["borderWidth"] // 2, config["yMin"])],
               fill="blue", width=config["borderWidth"])
    draw.line([(config["xMin"] - config["borderWidth"] // 2, config["yMax"]),
               (config["xMax"] + config["borderWidth"] // 2, config["yMax"])],
               fill="blue", width=config["borderWidth"])
    
    current_row = config["yMin"]
    
    for row in range(config["rows"]):
        current_row += config["pixelsInRow"]
        draw.line([config["xMin"] - config["borderWidth"] // 2, current_row, config["xMax"] + config["borderWidth"] // 2, current_row],
                    fill="blue", width=config["borderWidth"])

    #Draws the Logo
    for coord in cards_coordinates:
        current_coord = (coord[0] + config["logoTranslation"][0], coord[1] + config["logoTranslation"][1])
        image.paste(logo, box=(current_coord))

    blank_image = image.copy()

def read_data(data_file):
    raw_data = []
    with open(config["dataPath"], 'r') as f:
        data_reader = csv.reader(f)
        for row in data_reader:
            raw_data.append(row)

    table_sep = raw_data.index([])
    raw_data = [raw_data[:table_sep], raw_data[table_sep+1:]]
    return raw_data

def unpack_data(raw_data):
    data = []
    for table in raw_data:
        current_table = []
        for row in table:
            author = row[0]
            artwork = row[1:]
            for art in artwork:
                current_table.append([author, art])
        data.append(current_table)
    return data

def generate_sheets(data):
    sheets = []
    for table in data:
        len_table = len(table)
        i = 0
        while len_table >= 10:
            sheets.append(table[i:i+10])
            i += 10
            len_table -= 10
        if len_table > 0:
            sheets.append(table[i:])
            sheets[len(sheets)-1].extend([['','']] * (10 - len_table))
    return sheets

def write_text(data_list):
    pad = 100
    for i, coord in enumerate(cards_coordinates):
        current_coord = (coord[0] + config["titleTranslation"][0], coord[1] + config["titleTranslation"][1])
        if data_list[i][1] != '':
            text = '"' + data_list[i][1] + '"'
        else:
            text = data_list[i][1]
        text_wrapped = textwrap.wrap(text, width=22)

        delta_h = 0
        
        for text in text_wrapped:
            w, h = draw.textsize(text, font = config["font10"])
            
            if len(text_wrapped) == 1:
                delta_h += 50
            
            draw.text((current_coord[0] + ((config["titleTextbox"][2][0] - w) // 2), current_coord[1] + delta_h), text, fill="black", font=config["font8"])
            delta_h += pad
    
        
        current_coord = (coord[0] + config["nameTranslation"][0], coord[1] + config["nameTranslation"][1])
        text = data_list[i][0]
        text_wrapped = textwrap.wrap(text, width=13)
        
        delta_h = 0
        delta_h += (len(text_wrapped) - 3) * -50
        
        for text in text_wrapped:
            w, h = draw.textsize(text, font = config["font8"])

            draw.text((current_coord[0] + ((config["nameTextbox"][2][0] - w) // 2), current_coord[1] + delta_h), text, fill="black", font=config["font8"])
            delta_h += pad
'''
config = saveload.load_config("default.json")
config, image, draw = derive_config(config)
'''
def main():

    cards_coordinates = generate_card_coordinates()
    draw_static(cards_coordinates)
        
    raw_data = read_data(config["dataPath"])
    data = unpack_data(raw_data)
    sheets = generate_sheets(data)

    for i, sheet in enumerate(sheets):
        image.paste(blank_image)
        write_text(sheet)
        image.save(".//Generated Sheets//Sheet_" + str(i+1) + ".png")

