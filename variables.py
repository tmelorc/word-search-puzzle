# Constants and Global Variables
LOGFILE = 'LOGFILE'
WORDS_FILE = 'words.txt'
GAME_BOARDS_DIR = 'game_boards/'
WSP = 'Word Search Puzzle'

# Boolean flags
PDFLATEX = True
# SHOW_ANSWERS = True

# Board dimensions
ROWS = 20
COLS = 20

# Directions allowed for words
NORTH = True
SOUTH = True
EAST = True
WEST = True
DIAGONALS = True

MAXIMAL_NUMBER_OF_TRIES = 30

added_words = []
skipped_words = []
used_positions = {}
used_vector_positions = {}

DIR_OFFSETS = {
    "N": lambda r, c, i: (r - i,     c),
    "S": lambda r, c, i: (r + i,     c),
    "E": lambda r, c, i: (r,         c + i),
    "W": lambda r, c, i: (r,         c - i),
    "NE": lambda r, c, i: (r - i,     c + i),
    "SE": lambda r, c, i: (r + i,     c + i),
    "NW": lambda r, c, i: (r - i,     c - i),
    "SW": lambda r, c, i: (r + i,     c - i),
}
