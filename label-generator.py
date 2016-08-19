from PIL import Image, ImageDraw, ImageFont
import textwrap

''' TODO:
Add text-wrapping
Add centering code
Add csv support / automated pdf production
    
'''
#Configuration Settings
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
FONT_PATH = "times.ttf"

#Derived Settings
IMAGE_SIZE = (int(PAPER_SIZE[0] * PIXELS_PER_INCH),
              int(PAPER_SIZE[1] * PIXELS_PER_INCH))
MARGIN_SIZE = 1 * PIXELS_PER_INCH
TOP_MARGIN = int(TOP_MARGIN * PIXELS_PER_INCH)
SIDE_MARGIN = int(SIDE_MARGIN * PIXELS_PER_INCH)

X_MIN = SIDE_MARGIN
X_MAX = IMAGE_SIZE[0] - SIDE_MARGIN
Y_MIN = TOP_MARGIN
Y_MAX = IMAGE_SIZE[1] - TOP_MARGIN

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
name_textbox = [(logo.size[0] + LOGO_MARGIN * 2 + X_MIN, CARD_SIZE[1] - logo.size[1] - LOGO_MARGIN * 2 + TEXT_MARGIN + Y_MIN),
                (CARD_SIZE[0] - TEXT_MARGIN * 2 + X_MIN, CARD_SIZE[1] - TEXT_MARGIN * 2 + Y_MIN),
                ()]
name_textbox[2] = (name_textbox[1][0] - name_textbox[0][0], name_textbox[1][1] - name_textbox[0][1])
    
#TO REMOVE - DEPRECIATED
TITLE_TRANSLATION = (TEXT_MARGIN, TEXT_MARGIN)
NAME_TRANSLATION = (logo.size[0] + LOGO_MARGIN * 2, CARD_SIZE[1] - TEXT_MARGIN * 2 - logo.size[1] )

#Generates a list containing the upper left coordinate of each card.
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
draw.line([(X_MIN, Y_MIN),
           (X_MAX, Y_MIN)],
           fill="blue", width=BORDER_WIDTH)
draw.line([(X_MIN, Y_MAX),
           (X_MAX, Y_MAX)],
           fill="blue", width=BORDER_WIDTH)
current_row = Y_MIN
for row in range(ROWS):
    current_row += PIXELS_IN_ROW
    draw.line([X_MIN, current_row, X_MAX, current_row],
                fill="blue", width=BORDER_WIDTH)

#Draws the Logo
for coord in cards_coordinates:
    current_coord = (coord[0] + LOGO_TRANSLATION[0], coord[1] + LOGO_TRANSLATION[1])
    image.paste(logo, box=(current_coord))

blank_image = image.copy()

current_data = [ #[Name, Title, Name_Modifier, Title Modifier]
    ["George Martin", "Painting of a Cat"], 
    ["George Martin", "Painting of a Dog"],
    ["George Martin", "Painting of a Train"],
    ["Perry the Platypus", "Bach is Nice"],
    ["Perry the Platypus", "Nicity"],
    ["Perry the Platypus", "The French Explorer,\n Bachurat the Brave"],
    ["San Jean Von Eisenvon", "123"],
    ["San Jean Von Eisenvon", "456"],
    ["San Jean Von Eisenvon", "789"],
    ["San Jean Von Eisenvon", "022"]]

def text_format(text, text_box_size, font):
    text_size = draw.multiline_textsize(text, font=font, spacing=6)
    
    if text_size >= text_box_size:
        number_of_lines = 2
    else:
        number_of_lines = 1
    
    
    text_center(text, text_box_size, font, number_of_lines)

def text_center(text, text_box_size, font, number_of_lines):
    text_size = draw.multiline_textsize(text, font=font, spacing=6)
    if text_size >= text_box_size:
        pass
    else:
        pass

    formatted_text = text
    
    xy_adjustment = (0,0)

    return formatted_text, xy_adjustment


def write_text(data_list):
    image = blank_image
    for i, coord in enumerate(cards_coordinates):
        current_coord = (coord[0] + TITLE_TRANSLATION[0], coord[1] + TITLE_TRANSLATION[1])
        draw.multiline_text((current_coord), '"' + data_list[i][1] + '"', fill="black",
                            font=font10, spacing=6, align="center" )

        current_coord = (coord[0] + NAME_TRANSLATION[0], coord[1] + NAME_TRANSLATION[1])
        draw.multiline_text((current_coord), data_list[i][0], fill="black",
                            font=font8, spacing=6, align="center" )


#TO REMOVE, Locates name and title textboxes
draw.line(title_textbox[0:2],
            fill="black", width=5)
draw.line(name_textbox[0:2],
            fill="black", width=5)

write_text(current_data)
image.save("Test.png")

