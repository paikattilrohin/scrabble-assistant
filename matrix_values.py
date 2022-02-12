matrix = [
    ["  ", "  ", "  ", "TW", "  ", "  ", "TL", "  ", "TL", "  ", "  ", "TW", "  ", "  ", "  "],
    ["  ", "  ", "DL", "  ", "  ", "DW", "  ", "  ", "  ", "DW", "  ", "  ", "DL", "  ", "  "],
    ["  ", "DL", "  ", "  ", "DL", "  ", "  ", "  ", "  ", "  ", "DL", "  ", "  ", "DL", "  "],
    ["TW", "  ", "  ", "TL", "  ", "  ", "  ", "DW", "  ", "  ", "  ", "TL", "  ", "  ", "TW"],
    ["  ", "  ", "DL", "  ", "  ", "  ", "DL", "  ", "DL", "  ", "  ", "  ", "DL", "  ", "  "],
    ["  ", "DW", "  ", "  ", "  ", "TL", "  ", "  ", "  ", "TL", "  ", "  ", "  ", "DW", "  "],
    ["TL", "  ", "  ", "  ", "DL", "  ", "  ", "  ", "  ", "  ", "DL", "  ", "  ", "  ", "TL"],
    ["  ", "  ", "  ", "DW", "  ", "  ", "  ", "+", "  ", "  ", "  ", "DW", "  ", "  ", "  "],
    ["TL", "  ", "  ", "  ", "DL", "  ", "  ", "  ", "  ", "  ", "DL", "  ", "  ", "  ", "TL"],
    ["  ", "DW", "  ", "  ", "  ", "TL", "  ", "  ", "  ", "TL", "  ", "  ", "  ", "DW", "  "],
    ["  ", "  ", "DL", "  ", "  ", "  ", "DL", "  ", "DL", "  ", "  ", "  ", "DL", "  ", "  "],
    ["TW", "  ", "  ", "TL", "  ", "  ", "  ", "DW", "  ", "  ", "  ", "TL", "  ", "  ", "TW"],
    ["  ", "DL", "  ", "  ", "DL", "  ", "  ", "  ", "  ", "  ", "DL", "  ", "  ", "DL", "  "],
    ["  ", "  ", "DL", "  ", "  ", "DW", "  ", "  ", "  ", "DW", "  ", "  ", "DL", "  ", "  "],
    ["  ", "  ", "  ", "TW", "  ", "  ", "TL", "  ", "TL", "  ", "  ", "TW", "  ", "  ", "  "]
]

special_squares = {
    "DL" : 2,
    "TL" : 3,
}

letters_and_val = {
    "A" : 1,
    "B" : 4,
    "C" : 4,
    "D" : 2,
    "E" : 1,
    "F" : 4,
    "G" : 3,
    "H" : 3,
    "I" : 1,
    "J" : 10,
    "K" : 5,
    "L" : 2,
    "M" : 4,
    "N" : 2,
    "O" : 1,
    "P" : 4,
    "Q" : 10,
    "R" : 1,
    "S" : 1,
    "T" : 1,
    "U" : 2,
    "V" : 5,
    "W" : 4,
    "X" : 8,
    "Y" : 3,
    "Z" : 10
}

import os
filename = 'scrabble_words.json'
font_path = "COMIC.TTF"

working_dir = os.path.dirname(os.path.abspath(__file__))


filename = os.path.join(working_dir, filename)
font_path = os.path.join(working_dir, font_path)
home_folder = os.getenv('HOME')
save_scrabble_matrix_dir = os.path.join(home_folder, "Desktop")
save_scrabble_matrix_dir = os.path.join(save_scrabble_matrix_dir, ".scrabble_saved_matrices")
if not os.path.isdir(save_scrabble_matrix_dir):
    os.mkdir(save_scrabble_matrix_dir)

#    pyinstaller --onefile --add-data  'scrabble_words.json:.' --add-data 'COMIC.TTF:.'  scrabble.py