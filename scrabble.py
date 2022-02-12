import pygame
from matrix_values import matrix, font_path, save_scrabble_matrix_dir
import backend_scrabble_solver
# import threading
from queue import Queue
import os

import json

pygame.font.init()
que = Queue()
f1_flag = False

class Grid:

    def __init__(self, rows, cols, width, height, matrix):
        self.rows = rows
        self.cols = cols
        self.board = [[" " for j in range(cols)] for i in range(rows)]
        self.cubes = [[Cube(self.board[i][j], i, j, width, height, rows, cols, matrix[i][j]) for j in range(cols)] for i
                      in
                      range(rows)]
        self.width = width
        self.height = height
        self.selected_box = None
        self.selected = False
        self.selected_matrix = 1
        self.current_position = list()
        self.text_box_text = ""
        self.saved_board_detials = dict()
        self.saved_board_detials['current_position'] = self.current_position
        self.saved_board_detials['text_box_text'] = self.text_box_text

        self.count_changes = 0
        self.save_after_no_of_changes = 2

    def place(self, val):
        row, col = self.selected_box
        self.cubes[row][col].set(val)
        self.count_changes += 1
        if self.count_changes > self.save_after_no_of_changes:
            self.count_changes = 0
            self.write_file()

    def clear(self):
        row, col = self.selected_box
        self.cubes[row][col].set(" ")
        if self.count_changes > self.save_after_no_of_changes - 1:
            self.count_changes = 0
            self.write_file()

    def draw(self, win, thick=1):
        # Draw Grid Lines
        gap = self.width / self.cols

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

        for i in range(self.rows + 1):
            pygame.draw.line(win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

    def update_current_position(self, text_box_text):
        for i in range(self.rows):
            for j in range(self.cols):
                self.saved_board_detials['current_position'][i][j] = self.cubes[i][j].value
        self.saved_board_detials['text_box_text'] = text_box_text

    def update_cubes(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].value = self.saved_board_detials['current_position'][i][j]
                self.cubes[i][j].new_word_letter = " "

    def write_file(self):
        saved_matrix = os.path.join(save_scrabble_matrix_dir, "saved_matrix" + str(self.selected_matrix))
        with open(saved_matrix, 'w') as f:
            json.dump(self.saved_board_detials, f)

    def read_file(self):
        saved_matrix = os.path.join(save_scrabble_matrix_dir, "saved_matrix" + str(self.selected_matrix))
        with open(saved_matrix) as f:
            self.saved_board_detials = json.load(f)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected_box = (row, col)

    def confirm_new_word(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == " ":
                    self.cubes[i][j].value = self.cubes[i][j].new_word_letter
                self.cubes[i][j].new_word_letter = " "

    def touch_all_matrix_files(self):

        saved_board_details = {
            "current_position" : [[" " for i in range(self.rows)] for j in range(self.cols)],
            "text_box_text" : ""
        }
        for i in range(1, 10):
            saved_matrix = os.path.join(save_scrabble_matrix_dir, "saved_matrix" + str(i))
            if not os.path.isfile(saved_matrix):
                with open(saved_matrix, 'w') as f:
                    json.dump(saved_board_details, f)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / self.cols
            x = pos[0] // gap
            y = pos[1] // gap
            self.selected = True
            return (int(y), int(x))
        else:
            return None


class Cube:

    def __init__(self, value, row, col, width, height, no_rows, no_cols, box_value):
        self.value = value
        self.new_word_letter = " "
        self.box_value = box_value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.no_rows = no_rows
        self.no_cols = no_cols
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.Font(font_path, 40)
        gap = self.width / self.no_cols
        x = self.col * gap
        y = self.row * gap

        if self.new_word_letter != " ":
            text = fnt.render(str(self.new_word_letter), 1, (255, 0, 0))
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        elif not self.value == " ":
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            special_box = pygame.Rect(x, y, gap, gap)
            pygame.draw.rect(win, (195,155,119), special_box)
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        elif self.box_value != "  ":
            color = "green"  # for "TL"
            if self.box_value == "DW":
                color = "red2"
            elif self.box_value == "TW":
                color = "orange2"
            elif self.box_value == "DL":
                color = "blue2"
            elif self.box_value == "+":
                color = "purple3"

            box_font = pygame.font.Font(font_path, 20)
            text = box_font.render(str(self.box_value), 1, (0, 0, 0))
            special_box = pygame.Rect(x, y, gap, gap)
            pygame.draw.rect(win, color, special_box)
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
            pass

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val


class TextBox:
    def __init__(self, x1_co, y1_co, x2_co, y2_co):
        self.base_font = pygame.font.Font(font_path, 40)
        self.user_text = ""
        self.selected = False
        self.input_rect = pygame.Rect(x1_co, y1_co, x2_co, y2_co)
        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('grey15')
        self.color = self.color_passive

    def set_selected(self, flag):
        self.selected = flag
        if flag:
            self.color = self.color_active
        else:
            self.color = self.color_passive


def redraw_window(win, board, pastel = False ):
    if pastel:
        win.fill((222,165,164))
    else:
        win.fill((255, 255, 255))
    board.draw(win)


def draw_textbox(win, textbox):
    pygame.draw.rect(win, textbox.color, textbox.input_rect, 2)
    text_surface = textbox.base_font.render(textbox.user_text, True, (0, 0, 0))
    win.blit(text_surface, (textbox.input_rect.x + 5, textbox.input_rect.y + 5))
    pass


def get_answer(current_position, textbox):
    ans = backend_scrabble_solver.solve(current_position, textbox)
    que.put(ans)


window_size = (600, 650)
textbox_size = 50
rows = 15
columns = 15
win = pygame.display.set_mode(window_size)

pygame.display.set_caption("Paikro Scrabble Solver")
board = Grid(rows, columns, window_size[0], window_size[0], matrix)
board.touch_all_matrix_files()
board.read_file()
board.update_cubes()
textbox = TextBox(0, window_size[0], window_size[0], window_size[0] + textbox_size)
textbox.user_text = board.saved_board_detials['text_box_text']
key = None
run = True
pink = False


def reinitialize():
    global window_size, textbox, rows, columns, win, board, textbox, key, run
    window_size = (600, 650)
    textbox_size = 50
    rows = 15
    columns = 15
    win = pygame.display.set_mode(window_size)

    pygame.display.set_caption("Paikro Scrabble Solver")
    board = Grid(rows, columns, window_size[0], window_size[0], matrix)
    board.touch_all_matrix_files()
    board.read_file()
    board.update_cubes()
    textbox = TextBox(0, window_size[0], window_size[0], window_size[0] + textbox_size)
    textbox.user_text = board.saved_board_detials['text_box_text']



def main():
    global window_size, textbox, rows, columns, win, board, textbox, key, run
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                flag = False
                if event.key == pygame.K_a:
                    key = "A"
                    flag = True
                elif event.key == pygame.K_b:
                    key = "B"
                    flag = True
                elif event.key == pygame.K_c:
                    key = "C"
                    flag = True
                elif event.key == pygame.K_d:
                    key = "D"
                    flag = True
                elif event.key == pygame.K_e:
                    key = "E"
                    flag = True
                elif event.key == pygame.K_f:
                    key = "F"
                    flag = True
                elif event.key == pygame.K_g:
                    key = "G"
                    flag = True
                elif event.key == pygame.K_h:
                    key = "H"
                    flag = True
                elif event.key == pygame.K_i:
                    key = "I"
                    flag = True
                elif event.key == pygame.K_j:
                    key = "J"
                    flag = True
                elif event.key == pygame.K_k:
                    key = "K"
                    flag = True
                elif event.key == pygame.K_l:
                    key = "L"
                    flag = True
                elif event.key == pygame.K_m:
                    key = "M"
                    flag = True
                elif event.key == pygame.K_n:
                    key = "N"
                    flag = True
                elif event.key == pygame.K_o:
                    key = "O"
                    flag = True
                elif event.key == pygame.K_p:
                    key = "P"
                    flag = True
                elif event.key == pygame.K_q:
                    key = "Q"
                    flag = True
                elif event.key == pygame.K_r:
                    key = "R"
                    flag = True
                elif event.key == pygame.K_s:
                    key = "S"
                    flag = True
                elif event.key == pygame.K_t:
                    key = "T"
                    flag = True
                elif event.key == pygame.K_u:
                    key = "U"
                    flag = True
                elif event.key == pygame.K_v:
                    key = "V"
                    flag = True
                elif event.key == pygame.K_w:
                    key = "W"
                    flag = True
                elif event.key == pygame.K_x:
                    key = "X"
                    flag = True
                elif event.key == pygame.K_y:
                    key = "Y"
                    flag = True
                elif event.key == pygame.K_z:
                    key = "Z"
                    flag = True
                elif event.key == pygame.K_1:
                    board.update_current_position(textbox.user_text)
                    board.write_file()
                    board.selected_matrix = 1
                    board.read_file()
                    board.update_cubes()
                    textbox.user_text = board.saved_board_detials['text_box_text']
                elif event.key == pygame.K_2:
                    board.update_current_position(textbox.user_text)
                    board.write_file()
                    board.selected_matrix = 2
                    board.read_file()
                    board.update_cubes()
                    textbox.user_text = board.saved_board_detials['text_box_text']
                elif event.key == pygame.K_3:
                    board.update_current_position(textbox.user_text)
                    board.write_file()
                    board.selected_matrix = 3
                    board.read_file()
                    board.update_cubes()
                    textbox.user_text = board.saved_board_detials['text_box_text']
                elif event.key == pygame.K_4:
                    board.update_current_position(textbox.user_text)
                    board.write_file()
                    board.selected_matrix = 4
                    board.read_file()
                    board.update_cubes()
                    textbox.user_text = board.saved_board_detials['text_box_text']
                elif event.key == pygame.K_5:
                    board.update_current_position(textbox.user_text)
                    board.write_file()
                    board.selected_matrix = 5
                    board.read_file()
                    board.update_cubes()
                    textbox.user_text = board.saved_board_detials['text_box_text']
                elif event.key == pygame.K_6:
                    board.update_current_position(textbox.user_text)
                    board.write_file()
                    board.selected_matrix = 6
                    board.read_file()
                    board.update_cubes()
                    textbox.user_text = board.saved_board_detials['text_box_text']
                elif event.key == pygame.K_7:
                    board.update_current_position(textbox.user_text)
                    board.write_file()
                    board.selected_matrix = 7
                    board.read_file()
                    board.update_cubes()
                    textbox.user_text = board.saved_board_detials['text_box_text']
                elif event.key == pygame.K_8:
                    board.update_current_position(textbox.user_text)
                    board.write_file()
                    board.selected_matrix = 8
                    board.read_file()
                    board.update_cubes()
                    textbox.user_text = board.saved_board_detials['text_box_text']
                elif event.key == pygame.K_9:
                    board.update_current_position(textbox.user_text)
                    board.write_file()
                    board.selected_matrix = 9
                    board.read_file()
                    board.update_cubes()
                    textbox.user_text = board.saved_board_detials['text_box_text']

                if event.key == pygame.K_F1:
                    global f1_flag
                    if f1_flag:
                        f1_flag = False
                    else:
                        f1_flag = True


                if board.selected:
                    if flag:
                        i, j = board.selected_box
                        board.place(key)
                        key = None
                        flag = False

                    if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                        board.clear()
                        key = None
                        flag = False
                    if event.key == pygame.K_LEFT:
                        row_x, column_y = board.selected_box
                        if column_y - 1 >= 0:
                            board.select(row_x, column_y - 1)
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_SPACE:
                        row_x, column_y = board.selected_box
                        if column_y + 1 < columns:
                            board.select(row_x, column_y + 1)
                    if event.key == pygame.K_UP:
                        row_x, column_y = board.selected_box
                        if row_x - 1 >= 0:
                            board.select(row_x - 1, column_y)
                    if event.key == pygame.K_DOWN:
                        row_x, column_y = board.selected_box
                        if row_x + 1 < rows:
                            board.select(row_x + 1, column_y)

                if textbox.selected:
                    if flag:
                        if len(textbox.user_text) < 7:
                            board.confirm_new_word()
                            textbox.user_text += key

                    if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                        board.confirm_new_word()
                        textbox.user_text = textbox.user_text[:-1]

                    if event.key == pygame.K_RETURN:
                        board.update_current_position(textbox.user_text)
                        print("\n\n\n")
                        placed_word_matrix = backend_scrabble_solver.solve(board.saved_board_detials['current_position']
                                                                           , textbox.user_text)
                        for i in range(rows):
                            for j in range(columns):
                                if board.cubes[i][j].value == " ":
                                    board.cubes[i][j].new_word_letter = placed_word_matrix[i][j]

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                board_clicked = board.click(pos)
                if board_clicked:
                    board.confirm_new_word()
                    board.select(board_clicked[0], board_clicked[1])
                    textbox.set_selected(False)
                    key = None

                elif textbox.input_rect.collidepoint(event.pos):
                    textbox.set_selected(True)
                    board.selected = False


        else:
            redraw_window(win, board, pink)
            draw_textbox(win, textbox)
            pygame.display.update()


main()
pygame.quit()
