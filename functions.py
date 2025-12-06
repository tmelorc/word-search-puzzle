# bug: está adiocionando palavras repetidas na lista de palavras adicionadas?
import os
import random
import re
import numpy as np
import unidecode as uni
from variables import *

# Pattern to match only letters A-Z and numbers 0-9
# You can modify it to include other characters if needed
# Check also the validate_word function
PATTERN = re.compile(r"[A-Za-z0-9]+")


def load_file(file_path):
    """Load and return file content."""
    if not os.path.exists(file_path):
        save_log(f"** ERROR: File not found: {file_path}", LOGFILE)
        return None
    with open(file_path, "r") as f:
        return f.read().splitlines()


def save_log(msg, log_file=LOGFILE):
    """Append a string to the logfile and print it to the console."""
    with open(log_file, 'a') as f:
        f.write(msg)


def py2tex(row, col):
    """To adjust indexing from Python (0,0) to LaTeX (2,1)."""
    return row + 2, col + 1,


def random_letter():
    """Choose a random letter in the range [A-Z]."""
    i = random.randint(65, 65 + 25)
    return chr(i)


def random_origin(rows=ROWS, cols=COLS):
    """Choose a random origin (row, col) within the grid dimensions."""
    row, col = np.random.randint(rows), np.random.randint(cols)
    return row, col


def create_letter_matrix(rows, cols):
    """Create and return a random letter matrix of given dimensions."""
    matrix = np.zeros((rows, cols), dtype=str)
    for i in range(rows):
        for j in range(cols):
            matrix[i, j] = random_letter()
    return matrix


def update_letter_matrix(words, matrix):
    """Update the letter matrix with the given words."""
    for word in words:
        add_word(word, matrix)
    return matrix


def get_directions(row, col, word):
    """Return possible directions to add the word from the given origin."""
    directions = {'N': False, 'S': False, 'E': False, 'W': False}
    l = len(word)

    # Find available directions to the word
    if row - (l - 1) - 1 >= 0:
        directions['N'] = NORTH
    if row + (l - 1) < ROWS:
        directions['S'] = SOUTH
    if col + (l - 1) < COLS:
        directions['E'] = EAST
    if col - (l - 1) >= 0:
        directions['W'] = WEST

    # If diagonals are allowed, find available diagonal directions
    if DIAGONALS:
        directions['NE'] = directions['N'] and directions['E']
        directions['SE'] = directions['S'] and directions['E']
        directions['NW'] = directions['N'] and directions['W']
        directions['SW'] = directions['S'] and directions['W']

    return directions


def choose_direction(directions):
    """Choose a random direction from the available ones."""
    available_directions = [k for k, v in directions.items() if v]
    if not available_directions:
        return None

    return random.choice(available_directions)


def get_positions(row, col, word, direction):
    """Return the list of positions (row, col) for the word in the given direction."""
    positions = [DIR_OFFSETS[direction](row, col, i) for i in range(len(word))]
    '''
    if direction == 'N':
        positions = [(row - i, col) for i in range(l)]
    if direction == 'S':
        positions = [(row + i, col) for i in range(l)]
    if direction == 'E':
        positions = [(row, col + i) for i in range(l)]
    if direction == 'W':
        positions = [(row, col - i) for i in range(l)]
    if direction == 'NE':
        positions = [(row - i, col + i) for i in range(l)]
    if direction == 'SE':
        positions = [(row + i, col + i) for i in range(l)]
    if direction == 'NW':
        positions = [(row - i, col - i) for i in range(l)]
    if direction == 'SW':
        positions = [(row + i, col - i) for i in range(l)]
    '''
    return positions


def check_intersections(positions, used_positions, word):
    """Check if the word can be added at the given positions without conflicts."""
    for i, p in enumerate(positions):
        if p in used_positions and word[i] != used_positions[p]:
            return False

    return True


def add_word(word, matrix):
    """Try to add a word to the letter matrix."""
    save_log(f'\n** INFO: trying to add {word}', LOGFILE)

    ctr = 1
    rows, cols = matrix.shape

    while ctr < MAXIMAL_NUMBER_OF_TRIES:
        row, col = random_origin(rows, cols)
        directions = get_directions(row, col, word)

        # If there are available directions, try to add the word checking intersections
        if any(directions.values()):
            direction = choose_direction(directions)
            if direction is None:
                ctr += 1
                continue
            positions = get_positions(row, col, word, direction)
            intersection_ok = check_intersections(
                positions, used_positions, word)

            if intersection_ok and word not in added_words:
                added_words.append(word)
                for i, p in enumerate(positions):
                    print(positions)
                    used_positions[p] = word[i]
                    matrix[p] = word[i]
                used_vector_positions[(row, col)] = (direction, len(word))

                return True

        ctr += 1

    skipped_words.append(word)
    save_log(f'\n** WARNING: skipping {word} after {ctr} tries.')

    return False


def pdflatex(puzzle_id):
    """Run pdflatex to generate the PDF of the puzzle."""
    basename = 'main'
    os.system(f'pdflatex {basename}.tex')
    os.system(f'cp {basename}.pdf {GAME_BOARDS_DIR}{puzzle_id:04d}.pdf')
    os.remove(f'{basename}.log')
    os.remove(f'{basename}.aux')


def validate_word(word):
    """Validate and normalize a word."""
    if ' ' in word:
        save_log(
            f'\n** WARNING: blank space in {word.upper()} deleted.')
        word = word.replace(' ', '')

    word = uni.unidecode(word).upper()

    if not PATTERN.fullmatch(word):
        save_log(
            f'\n** WARNING: only letters in range A-Z or numbers in range 0-9 are allowed. Skipping {word.upper()}.')
        return False

    return word


def create_tex_files(matrix, puzzle_id=None):
    """Create the .info and .solution LaTeX files for the puzzle."""
    with open(f'{GAME_BOARDS_DIR}current.info', 'w') as f:
        f.write('% !TeX root = ../main.tex\n')

        code = r'\node[title,above=.5em of board] (title) {%s\hfill\#%04s\hfill\today};' % (
            WSP, puzzle_id)
        code += '\n\n'
        code += r'\node[words list,below=of board] (words) {' + ' \\quad '.join(
            sorted(added_words)) + '};'
        code += '\n\n'
        code += r'\node[words list,below=.5em of words] (total) {Number of words: ' + str(
            len(added_words)) + '};'
        code += '\n\n'
        f.write(code)
        f.close

    # tikz code to higlight the solutions on the puzzle
    with open(f'{GAME_BOARDS_DIR}current.solution', 'w') as f:
        f.write('% !TeX root = ../main.tex\n')

        for p in used_vector_positions:
            direction, word_len = used_vector_positions[p]
            row, col = p[0], p[1]

            a, b = py2tex(row, col)
            delta = word_len - 1

            if direction == 'N':
                word = ''.join(matrix[row - word_len + 1:row + 1, col][::-1])
                code = '\\node[fit=(board-%d-%d)(board-%d-%d),solution vertical] (%s) {};\n' % (
                    a, b, a - word_len + 1, b, word)
                code += '\\draw[-latex,thick, solution vertical,fill opacity=1] (%s.south)++(0:.6em) -- ++ (90:1em);\n' % word
            if direction == 'S':
                word = ''.join(matrix[row:row + word_len, col])
                code = '\\node[fit=(board-%d-%d)(board-%d-%d),solution vertical] (%s) {};\n' % (
                    a, b, row + 1 + word_len, col + 1, word)
                code += '\\draw[-latex,thick, solution vertical,fill opacity=1] (%s.north)++(180:.6em) -- ++ (-90:1em);\n' % word

            if direction == 'E':
                word = ''.join(matrix[row, col:col + word_len])
                code = '\\node[fit=(board-%d-%d)(board-%d-%d),solution horizontal] (%s) {};\n' % (
                    a, b, a, b + word_len - 1, word)
                code += '\\draw[-latex,thick, solution horizontal,fill opacity=1] (%s.west)++(90:.6em) -- ++ (0:1em);\n' % word

            if direction == 'W':
                word = ''.join(matrix[row, col - word_len + 1:col + 1][::-1])
                code = '\\node[fit=(board-%d-%d)(board-%d-%d),solution horizontal] (%s) {};\n' % (
                    a, b - word_len + 1, a, b, word)
                code += '\\draw[-latex,thick, solution horizontal,fill opacity=1] (%s.east)++(90:.6em) -- ++ (180:1em);\n' % word

            ''' diagonals '''
            if direction == 'SE':
                word = ''.join(matrix[row:row + word_len,
                               col:col + word_len].diagonal())
                code = '\\node[rotate fit=-45,fit=(board-%d-%d)(board-%d-%d),solution diagonal] (%s) {};\n' % (
                    a, b, row + 1 + word_len, col + word_len, word)
                code += '\\draw[-latex,thick, solution diagonal,fill opacity=1] (%s.west)++(45:.6em) -- ++ (-45:1em);\n' % word

            if direction == 'NE':
                word = ''.join(matrix[row - word_len + 1:row + 1,
                               col:col + word_len][::-1].diagonal())
                code = '\\node[rotate fit=45,fit=(board-%d-%d)(board-%d-%d),solution diagonal] (%s) {};\n' % (
                    a, b, row + 3 - word_len, col + word_len, word)
                code += '\\draw[-latex,thick, solution diagonal,fill opacity=1] (%s.west)++(135:.6em) -- ++ (45:1em);\n' % word

            if direction == 'NW':
                word = ''.join([matrix[row-i][col-i]
                                for i in range(word_len)])
                code = '\\node[rotate fit=-45,fit=(board-%d-%d)(board-%d-%d),solution diagonal] (%s) {};\n' % (
                    a, b, a - delta, b - delta, word)
                code += '\\draw[-latex,thick, solution diagonal,fill opacity=1] (%s.east)++(45:.6em) -- ++ (135:1em);\n' % word

            if direction == 'SW':
                word = ''.join([matrix[row+i][col-i]
                                for i in range(word_len)])
                code = '\\node[rotate fit=45,fit=(board-%d-%d)(board-%d-%d),solution diagonal] (%s) {};\n' % (
                    a, b, a + delta, b - delta, word)
                code += '\\draw[-latex,thick, solution diagonal,fill opacity=1] (%s.east)++(135:.6em) -- ++ (-135:1em);\n' % word

            f.write(code)
        f.close

    os.system(
        f'cp {GAME_BOARDS_DIR}current.info {GAME_BOARDS_DIR}{puzzle_id:04d}.info ; '
        f'cp {GAME_BOARDS_DIR}current.solution {GAME_BOARDS_DIR}{puzzle_id:04d}.solution')


if __name__ == "__main__":
    None
