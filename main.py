"""
Word Search Puzzle Generator Main Module
Author: Thiago de Melo
This module generates a word search puzzle by loading words from a specified file. It creates a letter matrix, places the words in it, and saves the puzzle in various formats. It also logs the process and can generate a PDF version of the puzzle using LaTeX.

Check booleans in variables.py to enable/disable features like PDF generation.
"""

import sys
import numpy as np
import os
from functions import *
from variables import *


def main(rows=ROWS, cols=COLS, words_file=WORDS_FILE):
    """Main function to generate the word search puzzle."""

    # # Reset global state
    # global added_words, skipped_words, used_positions, used_vector_positions

    # added_words = []
    # skipped_words = []
    # used_positions = {}
    # used_vector_positions = {}

    puzzle_id = np.random.randint(1000, 10000)
    matrix = create_letter_matrix(rows, cols)

    # Remove existing log file
    if os.path.isfile(LOGFILE):
        os.remove(LOGFILE)

    # Check if an argument was passed and use it as file path
    if len(sys.argv) > 1:
        words_file = sys.argv[1]
        save_log(f"** INFO: Using words file from command line: {words_file}")

    # Load the words file. In case of failure, exit the program
    words = load_file(words_file)
    if words:
        words = [vw for w in words if (vw := validate_word(w))]
        num_words = len(words)

        save_log(
            f"{num_words} words loaded successfully from file {words_file}!", LOGFILE)
    else:
        msg = f"** ERROR: Failed to load words from {words_file}. Exiting."
        save_log(msg, LOGFILE)
        print(msg)
        return

    # MAIN PART
    # Add the words to the matrix
    matrix = update_letter_matrix(words, matrix)

    if len(added_words) == 0:
        save_log("** WARNING: no words could be added to the puzzle!")

    # Save the matrix of letters to a file to be used as backup
    np.savetxt(f"{GAME_BOARDS_DIR}{puzzle_id}.table",
               matrix, fmt="%s")
    # Save the matrix of letters to a current file to be used in LaTeX
    np.savetxt(f"{GAME_BOARDS_DIR}current.table",
               matrix, fmt="%s")

    create_tex_files(matrix, puzzle_id)

    # Runs pdflatex to generate the PDF
    if PDFLATEX:
        pdflatex(puzzle_id)

    msg = (
        f"\n\n"
        f"Puzzle ID: {puzzle_id:04d}.\n"
        f"Added words ({len(added_words)} of {num_words}): {added_words}\n"
        f"Skipped words ({len(skipped_words)} of {num_words}): {skipped_words}\n"
        f"Bye!\n"
    )
    save_log(msg, LOGFILE)
    print(msg)


if __name__ == "__main__":
    main()
