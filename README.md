# word-search-puzzle
A Python tool that creates customizable word search puzzles and exports them using TikZ for high-quality LaTeX typesetting. Includes grid generation, automatic word placement, and optional solution output.

<img width="1070" height="1048" alt="screenshot0" src="https://github.com/user-attachments/assets/1d5d33c7-ddaa-4740-b24d-bb09a34b258b" />

<img width="1070" height="1048" alt="screenshot" src="https://github.com/user-attachments/assets/308af2fe-f6e4-4741-b93e-3444350569d7" />

1. Edit the list of words in `words.txt`
2. Run `python main.py`
3. Run `pdflatex main.tex`

**Note 1.** To hide the solutions, comment out the line `\input{./game_boards/current.solution}` in the `main.tex` file.

**Note 2.** The position of each word on the board is random. The script attempts to place each word up to 30 times in random mode. If it fails, the word is skipped. You can change this number by redefining `MAXIMAL_NUMBER_OF_TRIES = 30` in `variables.py`.

**Note 3.** The data for each game board is saved in the `game_boards` folder. You can restore an old game simply by copying its data into the current files.

# Project structure
```
word-search-puzzle/
│
├── main.py                 # Main script that generates the puzzle
├── variables.py            # Configuration values (e.g., max attempts)
├── words.txt               # Input word list
├── main.tex                # LaTeX output file
│
├── game_boards/            # Stores generated boards and solutions
│   ├── current.board
│   ├── current.solution
│   └── ...
│
└── tikz_templates/         # LaTeX/TikZ templates used for rendering

```
