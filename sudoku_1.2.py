import copy                         # copy is the imported module for the deepcopy
import os
import random
from random import shuffle
from termcolor import colored


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def level_select():
    levels = ["EASY","MEDIUM","HARD","DEMO"]
    for i,level in enumerate(levels):
        print("{}  {}".format(i +1, level))
    diff = input("Choose a number for difficulty: ")
    if diff not in ["1","2","3","4"]:
        level_select()
    elif diff == "1":
        diff = 30
    elif diff == "2":
        diff = 40
    elif diff == "3":
        diff = 60
    elif diff == "4":
        diff = 1
    create_board(diff)




def create_board(diff):
    row1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    shuffle(row1)                   # shuffles the first row witch gives the whole game palette

    seq1 = row1[:3]
    seq2 = row1[3:6]
    seq3 = row1[6:]
    row2 = seq2 + seq3 + seq1
    row3 = seq3 + seq1 + seq2

    row4 = row3[1:]+[row3[0]]
    seq4 = row4[:3]
    seq5 = row4[3:6]
    seq6 = row4[6:]                 # making the board with 'sudoku-slice' lol
    row5 = seq5 + seq6 + seq4
    row6 = seq6 + seq4 + seq5

    row7 = row6[1:]+[row6[0]]
    seq7 = row7[:3]
    seq8 = row7[3:6]
    seq9 = row7[6:]
    row8 = seq8 + seq9 + seq7
    row9 = seq9 + seq7 + seq8

    b = [row1, row2, row3, row4, row5, row6, row7, row8, row9]
    
    board = [list(row) for row in zip(*b)]

    def randnum():
        valid = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        num1 = random.choice(valid)
        num2 = random.choice(valid)
        return num1, num2
    
    i = 0
    while diff > i:
        num1,num2 = randnum()
        if board[num1][num2] == 0:
            num1,num2 = randnum()
        else:
            board[num1][num2] = 0
            i += 1

    original_board(board)


def original_board(board):                  # the original board
    fix_ind = [dict(enumerate(row)) for row in board]
    print_board(board, fix_ind)
    user_input(board, fix_ind)
    checker(row_i, col_i, board, fix_ind)


def print_board(board, fix_ind):                  # this function prints out the board
    clear()
    lst = copy.deepcopy(board)           # this is the making of the deepcopy

    for ind, row in enumerate(lst):
        for i, col in enumerate(row):        # iterates through the rows and changes the 0s to a space--> " "
            if col == 0:                    # checks if the col is 0
                row[i] = " "
            elif fix_ind[ind][i] != 0:
                row[i] = colored(col, "cyan", attrs=['bold'])

    for i in range(1, 10):
        print("   {}".format(i), end='')     # prints out the numbers on the top of the board
    print("\n" + " " + "="*37)
    for i, row in enumerate(lst):
        print("{}| {} : {} : {} | {} : {} : {} | {} : {} : {} |".format(i+1, *row))
        if i == 2 or i == 5 or i == 8:
            print(" " + "="*37)
        else:
            print(" | " + "- "*17 + "|")


def user_input(board, fix_ind):
    rcn = input("\nType NEW for a new game\nType RESET to reset the board\nRow Column Number separated by 'space':  ")
    if rcn.strip().lower() == "reset":
        reset_board(board, fix_ind)
    elif rcn.strip().lower() == "new":
        create_board()
    else:
        rcn = rcn.split(" ")                      # making a list from the rcn input [col_i,row_i,num]
    if len(rcn) != 3:
        invalid_input(board, fix_ind)
    valid = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

    row_i = rcn[0]        # slice the rcn for row,col,num with indexing
    col_i = rcn[1]
    num = rcn[2]

    while row_i not in valid or col_i not in valid or num not in valid:  # checks if the user input is valid or not
        invalid_input(board, fix_ind)

    checker(row_i, col_i, num, board, fix_ind)


def checker(row_i, col_i, num, board, fix_ind):
    sq1 = []
    sq2 = []
    sq3 = []

    if board[int(row_i)-1][int(col_i)-1] == 0:      # checks if the input spot is a 0
        if int(num) in board[int(row_i)-1]:         # checks if the input num is in the input row
            invalid_input(board, fix_ind)

        twisted = [col for col in zip(*board)]
        if int(num) in twisted[int(col_i)-1]:       # checks if the num is int the input column
            invalid_input(board, fix_ind)

        board[int(row_i)-1][int(col_i)-1] = int(num)
        for row in board:
            sq1.append(row[:3])
            sq2.append(row[3:6])
            sq3.append(row[6:])
            if len(sq1) == 3 and len(sq2) == 3 and len(sq3) == 3:
                square_check(row_i, col_i, sq1, sq2, sq3, board, fix_ind)

    elif board[int(row_i)-1][int(col_i)-1] != 0:        # if the given input from the user is not a 0 ask for delete
        ask = input("\nWould you like to delete? [Y/n]? ")
        if ask.strip().upper() == "Y":                  # if the answer is y or Y calls the deleter function
            delete(row_i, col_i, board, fix_ind)
        else:
            pass
    else:
        invalid_input(board, fix_ind)

    print_board(board, fix_ind)
    user_input(board, fix_ind)


def square_check(row_i, col_i, sq1, sq2, sq3, board, fix_ind):
    num1 = [c for char in sq1 for c in char if c != 0]
    num2 = [c for char in sq2 for c in char if c != 0]
    num3 = [c for char in sq3 for c in char if c != 0]
    nums = [num1, num2, num3]

    sq1.clear()
    sq2.clear()
    sq3.clear()

    for num in nums:
        for n in num:
            if num.count(n) > 1:
                board[int(row_i)-1][int(col_i)-1] = 0
                invalid_input(board, fix_ind)


def delete(row_i, col_i, board, fix_ind):
    if fix_ind[int(row_i)-1][int(col_i)-1] != 0:  # if the input from the user is an original number can't delete
        invalid_input(board, fix_ind)
    else:
        board[int(row_i)-1][int(col_i)-1] = 0    # if the input is a user number it can be deleted
    print_board(board, fix_ind)
    print("Deleted")
    user_input(board, fix_ind)


def reset_board(board, fix_ind):
    board.clear()                           # clears the original board
    for row in fix_ind:
        lst = list(row.values())            # create the "new" rows from the original board, using the dictionary values
        board.append(lst)                   # adds the new rows to  the board
    print_board(board, fix_ind)
    print("Reset done, keep trying")
    user_input(board, fix_ind)


def invalid_input(board, fix_ind):
    print_board(board, fix_ind)
    print("Invalid input")
    user_input(board, fix_ind)


clear()
level_select()
