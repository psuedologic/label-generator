#import PIL
from PIL import Image, ImageDraw

PIXELS_PER_INCH = 300
PAPER_SIZE = (8.5, 11)
IMAGE_SIZE = (int(PAPER_SIZE[0] * PIXELS_PER_INCH),
              int(PAPER_SIZE[1] * PIXELS_PER_INCH))
MARGIN_SIZE = 1 * PIXELS_PER_INCH
ROWS = 5
COLUMNS = 2
BORDER_WIDTH = 5

image = Image.new("RGB", IMAGE_SIZE, "white")
draw = ImageDraw.Draw(image, "RGB")

"""
UPPER_LEFT = (MARGIN_SIZE, MARGIN_SIZE)
BOTTOM_RIGHT = (IMAGE_SIZE[0] - MARGIN_SIZE, IMAGE_SIZE[1] - MARGIN_SIZE)
PRINTABLE_AREA = UPPER_LEFT + BOTTOM_RIGHT
"""

X_MIN = MARGIN_SIZE
X_MAX = IMAGE_SIZE[0] - MARGIN_SIZE
Y_MIN = MARGIN_SIZE
Y_MAX = IMAGE_SIZE[1] - MARGIN_SIZE
PIXELS_IN_ROW = ((Y_MAX - Y_MIN) // ROWS)
CARD_SIZE = (((X_MAX - X_MIN) // 2), PIXELS_IN_ROW)
LOGO_MARGIN = 20

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

#Draws the Border
draw.line([(X_MIN, Y_MIN),
           (X_MAX, Y_MIN),
           (X_MAX, Y_MAX),
           (X_MIN, Y_MAX),
           (X_MIN, Y_MIN)],
           fill="black", width=BORDER_WIDTH)

#Draws the Vertical Line
draw.line([(((X_MIN + X_MAX) // 2), Y_MIN),
           (((X_MIN + X_MAX) // 2), Y_MAX)],
             fill="black", width=BORDER_WIDTH)

#Draws the Horizontal Line
current_row = Y_MIN
for row in range(ROWS):
    current_row += PIXELS_IN_ROW
    draw.line([X_MIN, current_row, X_MAX, current_row],
                fill="black", width=BORDER_WIDTH)

#Draws the Logo
logo = Image.open("C:\\Users\\gonyeau\\AppData\\Local\\Programs\\Python\\Tag\\fair_logo.jpg")
logo = logo.resize((328, 243), Image.LANCZOS)
logo_translation = (LOGO_MARGIN, CARD_SIZE[1] - logo.size[1] - LOGO_MARGIN)


image.paste(logo, box=(500,500)) #, box=(((X_MIN + X_MAX) // 2), ((Y_MIN + Y_MAX) // 2)))

image.save("Test.png")

