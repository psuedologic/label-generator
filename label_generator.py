from PIL import Image, ImageDraw, ImageFont
import textwrap
import csv
import json #test to-remove

#Configuration Settings

''' Depreciated - Use JSON file for config settings
PIXELS_PER_INCH = 300
PAPER_SIZE = (8.5, 11)
ROWS = 5
COLUMNS = 2

BORDER_WIDTH = 40
LOGO_MARGIN = 40
TOP_MARGIN = .5
SIDE_MARGIN = .75
TEXT_MARGIN = 30

IMAGE_BACKGROUND = "white"
logo = Image.open("fair_logo.jpg")
logo = logo.resize((369, 273), Image.LANCZOS) #328, 243
RESOURCE_PATH = "..//resource//"
FONT_PATH = RESOURCE_PATH + "times.ttf"
DATA_PATH = RESOURCE_PATH + "fair-data.csv"
'''

#Derived Settings
def derive_config(config):
    pass
''' Convert from json config file
IMAGE_SIZE = (int(PAPER_SIZE[0] * PIXELS_PER_INCH),
              int(PAPER_SIZE[1] * PIXELS_PER_INCH))
MARGIN_SIZE = 1 * PIXELS_PER_INCH
TOP_MARGIN = int(TOP_MARGIN * PIXELS_PER_INCH)
SIDE_MARGIN = int(SIDE_MARGIN * PIXELS_PER_INCH)

X_MIN = SIDE_MARGIN + (LOGO_MARGIN * 3 // 4) # added logo margin to calibrate to my printer
X_MAX = IMAGE_SIZE[0] - SIDE_MARGIN - (LOGO_MARGIN * 3 // 4)
Y_MIN = TOP_MARGIN + LOGO_MARGIN
Y_MAX = IMAGE_SIZE[1] - TOP_MARGIN - LOGO_MARGIN

PIXELS_IN_ROW = ((Y_MAX - Y_MIN) // ROWS)
CARD_SIZE = (((X_MAX - X_MIN) // 2), PIXELS_IN_ROW)

font10 = ImageFont.truetype(FONT_PATH, 100)
font8 = ImageFont.truetype(FONT_PATH, 100)

image = Image.new("RGB", IMAGE_SIZE, IMAGE_BACKGROUND)
draw = ImageDraw.Draw(image, "RGB")

LOGO_TRANSLATION = (LOGO_MARGIN, CARD_SIZE[1] - logo.size[1] - LOGO_MARGIN)

# Format        [(UPPER, LEFT), (LOWER, RIGHT), (SIZE)]
title_textbox = [(TEXT_MARGIN + X_MIN, TEXT_MARGIN + Y_MIN),
                 (CARD_SIZE[0] - TEXT_MARGIN + X_MIN, CARD_SIZE[1] - logo.size[1] - LOGO_MARGIN * 2 - TEXT_MARGIN + Y_MIN),
                 ()]
title_textbox[2] = (title_textbox[1][0] - title_textbox[0][0], title_textbox[1][1] - title_textbox[0][1])
name_textbox = [(logo.size[0] + LOGO_MARGIN * 3 + X_MIN, CARD_SIZE[1] - logo.size[1] - LOGO_MARGIN * 2 + TEXT_MARGIN + Y_MIN),
                (CARD_SIZE[0] - TEXT_MARGIN * 2 + X_MIN, CARD_SIZE[1] - TEXT_MARGIN * 2 + Y_MIN),
                ()]
name_textbox[2] = (name_textbox[1][0] - name_textbox[0][0], name_textbox[1][1] - name_textbox[0][1])
'''    
#TO REMOVE - DEPRECIATED
TITLE_TRANSLATION = (TEXT_MARGIN, TEXT_MARGIN)
NAME_TRANSLATION = (logo.size[0] + LOGO_MARGIN * 2, CARD_SIZE[1] - TEXT_MARGIN * 2 - logo.size[1] )

#Generates a list containing the upper left coordinate of each card.
def generate_card_coordinates():
    cards_coordinates = []
    current_coord = (X_MIN, Y_MIN)
    cards_coordinates.append(current_coord)
    for row in range(ROWS):
        current_coord = (current_coord[0] + CARD_SIZE[0], current_coord[1])
        cards_coordinates.append(current_coord)
        
        current_coord = (current_coord[0] - CARD_SIZE[0],
                         current_coord[1] + CARD_SIZE[1])
        cards_coordinates.append(current_coord)
    cards_coordinates.pop(10)

def draw_static():
    #Draws the Vertical Lines
    draw.line([(X_MIN, Y_MIN),
               (X_MIN, Y_MAX)],
               fill="red", width=BORDER_WIDTH)
    draw.line([(X_MAX, Y_MIN),
               (X_MAX, Y_MAX)],
               fill="red", width=BORDER_WIDTH)
    draw.line([(((X_MIN + X_MAX) // 2), Y_MIN),
               (((X_MIN + X_MAX) // 2), Y_MAX)],
                 fill="red", width=BORDER_WIDTH)

    #Draws the Horizontal Lines
    draw.line([(X_MIN - BORDER_WIDTH // 2, Y_MIN),
               (X_MAX + BORDER_WIDTH // 2, Y_MIN)],
               fill="blue", width=BORDER_WIDTH)
    draw.line([(X_MIN - BORDER_WIDTH // 2, Y_MAX),
               (X_MAX + BORDER_WIDTH // 2, Y_MAX)],
               fill="blue", width=BORDER_WIDTH)
    current_row = Y_MIN
    for row in range(ROWS):
        current_row += PIXELS_IN_ROW
        draw.line([X_MIN - BORDER_WIDTH // 2, current_row, X_MAX + BORDER_WIDTH // 2, current_row],
                    fill="blue", width=BORDER_WIDTH)

    #Draws the Logo
    for coord in cards_coordinates:
        current_coord = (coord[0] + LOGO_TRANSLATION[0], coord[1] + LOGO_TRANSLATION[1])
        image.paste(logo, box=(current_coord))

    blank_image = image.copy()

''' Test Data - Depreciated
current_data = [ #[Name, Title]
    ["George Martin", "Painting of a Cat"], 
    ["George Martin", "2 Mandalas - Peppermints + Snails in the Garden"],
    ["George Martin", "Painting of a Train"],
    ["Perry the Platypus", "Bach is Nice"],
    ["Perry the Platypus", "Nicity"],
    ["Perry the Platypus", "The French Explorer, Bachurat the Brave"],
    ["San Jean Von Eisenvon", "123"],
    ["San Jean Von Eisenvon the Second", "456"],
    ["San Jean Von Eisenvon", "789"],
    ["San Jean Von Eisenvon", "022"]]
'''

def read_data(data_file):
    raw_data = []
    with open(DATA_PATH, 'r') as f:
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
        current_coord = (coord[0] + TITLE_TRANSLATION[0], coord[1] + TITLE_TRANSLATION[1])
        if data_list[i][1] != '':
            text = '"' + data_list[i][1] + '"'
        else:
            text = data_list[i][1]
        text_wrapped = textwrap.wrap(text, width=22)

        delta_h = 0
        
        for text in text_wrapped:
            w, h = draw.textsize(text, font = font10)
            
            if len(text_wrapped) == 1:
                delta_h += 50
            
            draw.text((current_coord[0] + ((title_textbox[2][0] - w) // 2), current_coord[1] + delta_h), text, fill="black", font=font8)
            delta_h += pad
    
        
        current_coord = (coord[0] + NAME_TRANSLATION[0], coord[1] + NAME_TRANSLATION[1])
        text = data_list[i][0]
        text_wrapped = textwrap.wrap(text, width=13)
        
        delta_h = 0
        delta_h += (len(text_wrapped) - 3) * -50
        
        for text in text_wrapped:
            w, h = draw.textsize(text, font = font8)

            draw.text((current_coord[0] + ((name_textbox[2][0] - w) // 2), current_coord[1] + delta_h), text, fill="black", font=font8)
            delta_h += pad
    
generate_card_coordinates()
draw_static()
    
raw_data = read_data(DATA_PATH)
data = unpack_data(raw_data)
sheets = generate_sheets(data)

for i, sheet in enumerate(sheets):
    image.paste(blank_image)
    write_text(sheet)
    image.save(".//Generated Sheets//Sheet_" + str(i+1) + ".png")

