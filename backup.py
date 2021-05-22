from matrix_values import matrix, letters_and_val, special_squares, filename
import itertools
from pprint import pprint
import copy

optimal_answer_horizontal = []
max_possible_score_horizontal = 0
optimal_answer_vertical = []
max_possible_score_vertical = 0
horizontal_answer = {}


def get_scrabble_words(file_path):
    import json
    with open(file_path) as json_file:
        dictionary_words = json.load(json_file)
    return set(dictionary_words)


all_scrabble_words = get_scrabble_words(filename)


class SquareAttributes:
    def __init__(self):
        self.top = False
        self.left = False
        self.right = False
        self.bottom = False
        self.touching = False
        self.letter_exists = False

    def is_touching(self):
        self.touching = self.top or self.bottom or self.right or self.left
        return self.touching


def get_playable_rows(current_position):
    playable_rows = {}
    non_empty_rows = set()
    matrix_len = len(current_position[0])
    for i in range(matrix_len):
        flag = False
        count = 0
        for j in range(matrix_len):
            if current_position[i][j] != " ":
                count += 1
                non_empty_rows.add(i)
                flag = True
        if flag:
            playable_rows[i] = matrix_len - count

    for row in non_empty_rows:
        if row - 1 >= 0 and row - 1 not in non_empty_rows:
            playable_rows[row - 1] = matrix_len
        if row + 1 < matrix_len and row + 1 not in non_empty_rows:
            playable_rows[row + 1] = matrix_len
    return playable_rows


def get_playable_cols(current_position):
    playable_cols = {}
    non_empty_cols = set()
    matrix_len = len(current_position[0])
    for i in range(matrix_len):
        flag = False
        count = 0
        for j in range(matrix_len):
            if current_position[j][i] != " ":
                count += 1
                non_empty_cols.add(i)
                flag = True
        if flag:
            playable_cols[i] = matrix_len - count

    for cols in non_empty_cols:
        if cols - 1 >= 0 and cols - 1 not in non_empty_cols:
            playable_cols[cols - 1] = matrix_len
        if cols + 1 < matrix_len and cols + 1 not in non_empty_cols:
            playable_cols[cols + 1] = matrix_len
    return playable_cols


def get_letters_to_use(given_letters):
    for i in range(1, len(given_letters) + 1):
        for val in itertools.combinations(given_letters, i):
            for perm in itertools.permutations(val, i):
                yield list(perm)


def get_word_score(row, i, letter_score, multiplier, matrix_details, current_position):
    score = letter_score
    if not matrix_details[row][i].letter_exists:
        while row - 1 >= 0 and current_position[row - 1][i] != ' ':
            score += letters_and_val[current_position[row - 1][i]]
            row -= 1
        while row + 1 < len(current_position[0]) and current_position[row - 1][i] != ' ':
            score += letters_and_val[current_position[row + 1][i]]
            row += 1
    if score == letter_score:
        return 0
    return score


def calculate_score(current_position, matrix_details, row, placed_word_start_index, placed_word_end_index):
    total_multiplier = 1
    total_score = 0
    for i in range(placed_word_start_index, placed_word_end_index + 1):
        if matrix[row][i] in special_squares and not matrix_details[row][i].letter_exists:
            total_score += special_squares[matrix[row][i]] * letters_and_val[current_position[row][i]]
        else:
            total_score += letters_and_val[current_position[row][i]]
        if matrix[row][i] == 'TW' and not matrix_details[row][i].letter_exists:
            total_multiplier *= 3
        if matrix[row][i] == 'DW' and not matrix_details[row][i].letter_exists:
            total_multiplier *= 2
    total_score *= total_multiplier

    for i in range(placed_word_end_index, placed_word_end_index + 1):
        multiplier = 1
        if matrix[row][i] in special_squares:
            letter_score = special_squares[matrix[row][i]] * letters_and_val[current_position[row][i]]
        else:
            letter_score = letters_and_val[current_position[row][i]]
        if matrix[row][i] == 'TW':
            multiplier *= 3
        if matrix[row][i] == 'DW':
            multiplier *= 2
        total_score += get_word_score(row, i, letter_score, multiplier, matrix_details, current_position)
    return total_score


def check_word_vertically(current_position, row, placed_word_start_index):
    size = len(current_position[0])
    word_start_i = row
    while word_start_i - 1 >= 0 and word_start_i < size and current_position[word_start_i - 1][
        placed_word_start_index] != " ":
        word_start_i -= 1

    word = current_position[word_start_i][placed_word_start_index]
    while word_start_i + 1 < size and current_position[word_start_i + 1][placed_word_start_index] != " ":
        word += current_position[word_start_i + 1][placed_word_start_index]
        word_start_i += 1

    if len(word) == 1:
        return True

    if word.lower() in all_scrabble_words:
        return True

    return False


def check_word_horizontally(current_position, row, placed_word_start_index):
    size = len(current_position[0])
    word_start_i = placed_word_start_index
    while word_start_i - 1 >= 0 and word_start_i < size and current_position[row][word_start_i - 1] != " ":
        word_start_i -= 1

    word = current_position[row][word_start_i]
    while word_start_i + 1 < size and current_position[row][word_start_i + 1] != " ":
        word += current_position[row][word_start_i + 1]
        word_start_i += 1
    # print(word)
    if len(word) == 1:
        return True
    if word.lower() in all_scrabble_words:
        # print("vertical word",word)
        return True
    return False


def check_if_all_valid_words_formed(current_position, placed_word_start_index, placed_word_end_index, row,
                                    ):
    if check_word_horizontally(current_position, row, placed_word_start_index):
        size = len(current_position[0])
        word_start_i = placed_word_start_index
        while word_start_i - 1 >= 0 and word_start_i < size and current_position[row][word_start_i - 1] != " ":
            word_start_i -= 1
        while word_start_i < size and current_position[row][word_start_i] != " ":
            if not check_word_vertically(current_position, row, word_start_i):
                return False
            word_start_i += 1

        return True
    return False


def flip_matrix(matrix1):
    for i in range(len(matrix1)):
        for j in range(i, len(matrix1[0])):
            tmp = matrix1[i][j]
            matrix1[i][j] = matrix1[j][i]
            matrix1[j][i] = tmp


def copy_matrix(matrix1, flipped=False):
    # copy matrix1 to matrix2
    global optimal_answer_horizontal
    global optimal_answer_vertical
    if flipped:
        flip_matrix(matrix1)
        optimal_answer_vertical = matrix1.copy()
        pprint(optimal_answer_vertical)
        flip_matrix(matrix1)

    else:
        optimal_answer_horizontal = matrix1.copy()
        pprint(optimal_answer_horizontal)
    if flipped:
        flip_matrix(matrix1)


def place_horizontally(current_position, playable_rows_and_empty_space, letters,
                       matrix_squares_details, flipped=False):
    global optimal_answer_horizontal
    global max_possible_score_horizontal
    global optimal_answer_vertical
    global max_possible_score_vertical

    matrix_size = len(current_position[0])
    for row in playable_rows_and_empty_space.keys():
        if len(letters) <= playable_rows_and_empty_space[row]:
            for start_index in range(0, matrix_size - (len(letters) - 1)):
                if start_index + len(letters) < matrix_size:
                    row_copy = current_position[row].copy()
                    word_successfully_placed = False
                    letters_i = 0
                    row_index = start_index
                    touching_existing_word = False
                    placed_word_start_index = None
                    placed_word_end_index = None
                    while letters_i < len(letters) and row_index < matrix_size:
                        if current_position[row][row_index] == " ":
                            current_position[row][row_index] = letters[letters_i]
                            touching_existing_word = touching_existing_word or \
                                                     matrix_squares_details[row][row_index].is_touching()
                            if letters_i == len(letters) - 1:
                                word_successfully_placed = True
                                placed_word_end_index = row_index
                            if letters_i == 0:
                                placed_word_start_index = row_index
                            row_index += 1
                            letters_i += 1
                        else:
                            row_index += 1
                            touching_existing_word = True

                    if touching_existing_word and word_successfully_placed:
                        if check_if_all_valid_words_formed(current_position, placed_word_start_index,
                                                           placed_word_end_index, row):
                            score = calculate_score(current_position, matrix_squares_details, row,
                                                    placed_word_start_index, placed_word_end_index)

                            if not flipped and score > max_possible_score_horizontal:
                                max_possible_score_horizontal = score
                                optimal_answer_horizontal = copy.deepcopy(current_position)
                                print("max possible score with following is  ", max_possible_score_horizontal, flipped)
                                pprint(optimal_answer_horizontal)

                            if flipped and score > max_possible_score_vertical:
                                max_possible_score_vertical = score
                                # copy_matrix(current_position, flipped)
                                flip_matrix(current_position)
                                optimal_answer_vertical = copy.deepcopy(current_position)
                                flip_matrix(current_position)
                                print("max possible score with following is  ", max_possible_score_vertical, flipped)
                                pprint(optimal_answer_vertical)

                    for i in range(len(row_copy)):
                        current_position[row][i] = row_copy[i]


def get_matrix_touching_detials(current_position):
    matrix_square_detials = [[SquareAttributes() for i in range(len(current_position[0]))] for j in
                             range(len(current_position[0]))]
    for i in range(len(current_position[0])):
        for j in range(len(current_position[0])):
            if current_position[i][j] != ' ':
                if i - 1 >= 0:
                    matrix_square_detials[i - 1][j].bottom = True
                if i + 1 < len(current_position[0]):
                    matrix_square_detials[i + 1][j].top = True
                if j - 1 >= 0:
                    matrix_square_detials[i][j - 1].right = True
                if j + 1 < len(current_position[0]):
                    matrix_square_detials[i][j + 1].left = True
                if current_position[i][j] != ' ':
                    matrix_square_detials[i][j].letter_exists = True
    return matrix_square_detials


def solve_horizontal(current_position, all_letters, matrix):
    global optimal_answer_horizontal
    optimal_answer_horizontal = current_position.copy()
    playable_rows_and_empty_space = get_playable_rows(current_position)
    matrix_squares_details = get_matrix_touching_detials(current_position)
    for letters in get_letters_to_use(all_letters):
        place_horizontally(current_position, playable_rows_and_empty_space, letters, matrix_squares_details)


def solve_vertical(current_position, all_letters, matrix):
    global optimal_answer_vertical
    optimal_answer_vertical = current_position.copy()
    flip_matrix(current_position)
    for letters in get_letters_to_use(all_letters):
        # for vertical
        playable_rows_and_empty_space = get_playable_rows(current_position)
        matrix_squares_detials = get_matrix_touching_detials(current_position)
        place_horizontally(current_position, playable_rows_and_empty_space, letters, matrix_squares_detials,
                           flipped=True)
    flip_matrix(current_position)


def solve(current_position, letters_to_use):
    global optimal_answer_horizontal
    global max_possible_score_horizontal
    global optimal_answer_vertical
    global max_possible_score_vertical
    optimal_answer_horizontal = []
    max_possible_score_horizontal = 0
    optimal_answer_vertical = []
    max_possible_score_vertical = 0

    letters_to_use = [x for x in letters_to_use]

    solve_horizontal(current_position, letters_to_use, matrix)
    solve_vertical(current_position, letters_to_use, matrix)

    if max_possible_score_horizontal > max_possible_score_vertical:
        return optimal_answer_horizontal
    else:
        return optimal_answer_vertical

