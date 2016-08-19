from PIL import Image, ImageDraw

#Configuration Settings
PIXELS_PER_INCH = 300
PAPER_SIZE = (8.5, 11)
ROWS = 5
COLUMNS = 2
BORDER_WIDTH = 40
LOGO_MARGIN = 40
IMAGE_BACKGROUND = "white"
logo = Image.open("fair_logo.jpg")
logo = logo.resize((369, 273), Image.LANCZOS) #328, 243

#Derived Settings
IMAGE_SIZE = (int(PAPER_SIZE[0] * PIXELS_PER_INCH),
              int(PAPER_SIZE[1] * PIXELS_PER_INCH))
MARGIN_SIZE = 1 * PIXELS_PER_INCH
TOP_MARGIN = int(.5 * PIXELS_PER_INCH)
SIDE_MARGIN = int(.75 * PIXELS_PER_INCH)
X_MIN = SIDE_MARGIN
X_MAX = IMAGE_SIZE[0] - SIDE_MARGIN
Y_MIN = TOP_MARGIN
Y_MAX = IMAGE_SIZE[1] - TOP_MARGIN
PIXELS_IN_ROW = ((Y_MAX - Y_MIN) // ROWS)
CARD_SIZE = (((X_MAX - X_MIN) // 2), PIXELS_IN_ROW)
LOGO_TRANSLATION = (LOGO_MARGIN, CARD_SIZE[1] - logo.size[1] - LOGO_MARGIN)
image = Image.new("RGB", IMAGE_SIZE, IMAGE_BACKGROUND)
draw = ImageDraw.Draw(image, "RGB")

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
current_coord
for coord in cards_coordinates:
    current_coord = (coord[0] + LOGO_TRANSLATION[0], coord[1] + LOGO_TRANSLATION[1])
    image.paste(logo, box=(current_coord))

blank_image = image.copy()

current_data = [ #[Name, Title, Name_Modifier, Title Modifier]
    ["George Martin", "Painting of a Cat"], 
    ["George Martin", "Painting of a Dog"],
    ["George Martin", "Painting of a Train"],
    ["Perry the Platypus", "Bach is Nude"],
    ["Perry the Platypus", "Nudity"],
    ["Perry the Platypus", "The French Explorer, Bachurat the Brave"],
    ["San Jean Von Eisenvon", "123"],
    ["San Jean Von Eisenvon", "456"]]

def write_text(data_list):
    image = blank_image
    for entry in data_list:
        pass



image.save("Test.png")

