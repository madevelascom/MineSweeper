################################################################
# -*- coding: utf-8 -*-
# Title: Buscaminas
# Developed by: Madelyne Velasco
# SavedVariables: board, match
# Notes: Minesweeper game that supports different size games.
# It can save game on files and load them later.
# TODO: Support several languages
################################################################

__author__ = 'Administrator'

from numpy import zeros, shape
from random import *
import time
import pickle


################################################################
# Function: menu()
# Main menu
################################################################

def menu():
    print('========================================')
    print('========================================')
    print('¡Bienvenidos a Buscaminas!')
    print('Seleccione alguna de las opciones para continuar ')
    print('1.- Nuevo Juego Inicial (8x8) ')
    print('2.- Nuevo Juego Intermedio (16x16)')
    print('3.- Nuevo Juego Avanzado (30x16)')
    print('4.- Nuevo Juego Personalizado (Tamaño a escoger)')
    print('5.- Cargar una partida Guardada')
    print('6.- Acerca del juego')
    print('0.- Salir')
    print('=======================================')
    get_option()

################################################################
# Function: get_option()
# Initialize each option of the menu. Calls several functions.
################################################################

def get_option():

    INSTRUCTIONS = ("""

    OBJETIVO
    Encontrar los cuadrados vacíos evitando las minas. ¡Mientras más rápido, mejor!

    EL TABLERO
    Buscaminas tiene tres tableros predefinidos en varias dificultades:
    [*]Principiante: 8x8  con 10 minas
    [*]Intermedio:  16x16 con 40 minas
    [*]Avanzado:    30x16 con 99 minas

    También puedes crear un tablero personalizado de tamaño máximo 30x30 con hasta 841 minas.

    CÓMO JUGAR
    Las reglas son sencillas:
    [*]Descubre una mina y el juego termina.
    [*]Descubre un cuadrado vacío y el juego continía
    [*]Descubre un número y te dará información sobre cuantas minas se encuentran escondidas en
    los cuadrados circundantes.""")

    GOODBYE = ("""
                _
             .-T |   _
             | | |  / |
             | | | / /`|
          _  | | |/ / /
          \`\| '.' / /
           \ \`-. '--|
            \    '   |
             \  .`  /
              |    |""")
    option = input('Ingrese alguna de las opciones anteriores para continuar: ')

    if option == "6":
        option = input(INSTRUCTIONS)

    while not option_is_valid(option):
        option = input('Entrada incorrecta, escriba 6 para ayuda.Ingrese una opcion del menú válida: ')
        if option == "6":
            option = input(INSTRUCTIONS)

    if option == "1":
        x = 8
        y = 8
        mines = 10
        board = create_board(x, y)
        match = bomb_maping(x, y, mines)
        play_game(board, match, x, y)
    elif option == "2":
        x = 16
        y = 16
        mines = 40
        board = create_board(x, y)
        match = bomb_maping(x, y, mines)
        play_game(board, match, x, y)
    elif option == "3":
        x = 30
        y = 16
        mines = 99
        board = create_board(x, y)
        match = bomb_maping(x, y, mines)
        play_game(board, match, x, y)
    elif option == "4":
        x = input('Ingrese el ancho de la cuadrilla (Máximo 30')
        y = input('Ingrese el alto de la cuadrilla (Máximo 30')
        mines = input ('Ingrese la cantida de minas. Máximo xy/2')

        while not per_size_is_valid(x, y, mines):
            print('Alguna de las opciones ingresadas no es válida')
            x = input('Ingrese el ancho de la cuadrilla (Máximo 30')
            y = input('Ingrese el alto de la cuadrilla (Máximo 30')
            mines = input ('Ingrese la cantida de minas. Máximo xy/2')

        x = int(x)
        y = int(y)
        mines = int(mines)
        board = create_board(x, y)
        match = bomb_maping(x, y, mines)
        play_game(board, match, x, y)

    elif option == "5":
        [board,match] = load_game()

        if board == [0, 0] or match == [0, 0]:
            print('No hay una partida guardada con anterioridad. \n')
            get_option()
        else:
            [x, y] = shape(board)
            mines = 0
            for i in range (len(match)-1):
                for j in range (len(match[i])-1):
                    if match[i, j] == '-1':
                        mines += 1
            play_game(board, match, x-1, y-1 )

    else:
        print (GOODBYE)
        print ('Gracias por iniciar el juego. Lo esperamos una próxima ocasión.')


################################################################
# Function: option_is_valid(option_input)
# Determines TRUE or FALSE statement for get_option
################################################################


def option_is_valid(option_input):
    try:
        option_input = int(option_input)
        if option_input >= 0 and option_input <=7:
            return True
        else:
            return False
    except:
        return False

################################################################
# Function: per_size_is_valid(x_size, y_size, mines)
# Determines TRUE or FALSE statement for the custom game.
# Verifies if the given dimensions are between boundaries
################################################################

def per_size_is_valid(x_size, y_size, mines):
    try:
        x_size = int(x_size)
        y_size = int(y_size)
        mines = int(mines)

        if x_size>0 and x_size <=30 and y_size>0 and y_size<=30 and mines<=x_size*y_size/2:
            return True
        else:
            return False
    except:
        return False


################################################################
# Function: create_board(x_size, y_size)
# Creates visual board for the player. Size is given by chosen
# option
################################################################

def create_board(x_size, y_size):
    board = zeros([x_size+2, y_size+2], dtype = str)

    for i in range(1, len(board)-1):
        for j in range(1, len(board[i])-1):
            board[i,j] = ' '

    for i in range(0, x_size+1):
        board[i, 0] = i
        board[i, y_size+1] = i

    for j in range(0, y_size+1):
        board [0, j] = j
        board [x_size+1, j] = j

    return board

################################################################
# Function: bomb_maping(x_size, y_size, mines)
# Creates hidden map of the mines and their surroundings. Size
# is given by chosen option.
################################################################

def bomb_maping(x_size, y_size, mines):
    x_size += 2
    y_size += 2
    pox_mines = []
    for i in range(mines):
        row = randint(1, x_size-2)
        col = randint(1, y_size-2)
        new_mine = [row, col]
        while new_mine in pox_mines:
            row = randint(1, x_size-2)
            col = randint(1, y_size-2)
            new_mine = [row, col]
        pox_mines.append(new_mine)

    match_board = zeros((x_size, y_size), dtype = int)

    for i in range(len(pox_mines)):
        [row, col] = pox_mines[i]
        match_board[row, col] = -1

    for i in range(len(pox_mines)):
        [row, col] = pox_mines[i]
        SURROUNDING = ((row-1, col-1),(row-1,  col), (row-1,  col+1),
                       (row  , col-1),               (row  ,  col+1),
                       (row+1, col-1),(row+1 ,  col),(row+1,  col+1))
        for (surr_row, surr_col) in SURROUNDING:
            if(surr_row != 0 and surr_row != x_size-1 and surr_col != 0 and surr_col != y_size-1) \
                and (match_board[surr_row, surr_col] != -1):
                match_board[surr_row, surr_col] += 1
    return match_board

################################################################
# Function: get_move(x, y):
# Receives string for the coords of unveiling cell. Range
# between given size of the game
################################################################

def get_move(x, y):
    INSTRUCTIONS = ("""
Primero ingresa la fila, luego la columna separadas con un punto (.).
Para añadir una bandera, escribe \"f\" al final de las coordenadas (Ej: 5.4f donde sería la quinta
en la cuarta columna donde iría la bandera. Para salir escriba \"e\" y para guardar \"s\".
\n Ingrese las coordenadas de la celda: """)

    global is_ended
    is_ended = False

    move = input('Ingrese las coordenadas de una celda. Escriba \"H"\ para ayuda: ')

    if move == 'H' or move == 'h':
        move = input(INSTRUCTIONS)

    if move == 'S' or move == 's':
        print('El juego ha sido guardado.')
        save_game(board_display, mine_camp)
        return (0, 0, '3')

    if move == 'E' or move == 'e':
        question = input('Presione Y para salir, N para continuar o S para salir y guardar: ')

        while not end_is_valid(question):
            question = input('Presione Y para salir, N para continuar o S para salir y guardar: ')

        if question == 'Y' or question == 'y':
            is_ended = True
            return (0, 0, '2')
        elif question == 'N' or question == 'n':
            move = input('Ingrese las coordenadas de una celda. Escriba \"H"\ para ayuda: ')
        elif question == 'S' or question == 's':
            is_ended = True
            save_game(board_display, mine_camp)
            return (0, 0, '3')

    while not move_is_valid(move, x, y):
        move = input('Ingrese las coordenadas de una celda. Escriba \"H"\ para ayuda: ')
        if move == 'H' or move == 'h':
            move = input(INSTRUCTIONS)
        if move == 'E' or move == 'e':
            question = input('Presione Y para salir, N para continuar o S para salir y continuar: ')
            while not end_is_valid(question):
                question = input('Presione Y para salir, N para continuar o S para salir y guardar: ')

            if question == 'Y' or question == 'y':
                is_ended = True
                move = ('1.1')
                row = 1
                col = 1
                flag = 2
                return (row, col, flag)
            elif question == 'N' or question == 'n':
                move = input('Ingrese las coordenadas de una celda. Escriba \"H"\ para ayuda: ')
            elif question == 'S' or question == 's':
                is_ended = True
                move = ('1.1')
                row = 1
                col = 1
                flag = 2
                save_game(board_display, mine_camp)
                return (row, col, flag)
        if move == 'S' or move == 's':
            save_game(board_display, mine_camp)
            move = input('Ingrese las coordenadas de una celda. Escriba \"H"\ para ayuda: ')

    if is_ended == False:
        chain = len(move)
        vec = list(move)
        row = 0
        col = 0
        flag = 0

        k = vec.index('.')
        if vec[-1] == 'F' or vec[-1] == 'f':
            chain -= 1
            flag = 1

        for i in range(k):
            a = int(vec[i])
            row += a*10**(k-i-1)
        for i in range (k+1, chain):
            a = int(vec[i])
            col += a*10**(chain-i-1)

    else:
        flag = 2

    return (row, col, flag)



################################################################
# Function: move_is_valid(move_input, x, y)
# Determines if the string gives valid coords or string.
################################################################

def move_is_valid(move_input, x, y):
    chain = len(move_input)
    vec = list(move_input)

    if not ('.' in vec):
        return False
    else:
        k = vec.index('.')
        if vec[-1] == 'F' or vec[-1] == 'f':
            chain -= 1

        row = 0
        col = 0

        for i in range(k):
            if vec[i].isdigit():
                a = int(vec[i])
                row += a*10**(k-i-1)
            else:
                return False

        for i in range(k+1, chain):
            if vec[i].isdigit():
                a = int(vec[i])
                col += a*10**(chain-i-1)
            else:
                return False

        if row > 0 and row <=x and col > 0 and col <=y:
            return True
        else:
            return False


################################################################
# Function: end_is_valid(end_input)
# Determines if the given input for ending the game is valid
################################################################

def end_is_valid(end_input):
    if end_input == 'Y' or end_input == 'y':
        return True
    elif end_input == 'N' or end_input == 'n':
        return True
    elif end_input == 'S' or end_input == 's':
        return True
    else:
        return False


################################################################
# Function: is_flagged(cell_content)
# Determines if an specific cell on the game board has a flag
################################################################

def is_flagged(cell_content):
    if cell_content == "F":
        return True
    else:
        return False

################################################################
# Function: is_visible(cell_content)
# Determines if an specific cell on the game board was discovered.
################################################################

def is_visible(cell_content):
    if cell_content != " ":
        return True
    else:
        return False

################################################################
# Function: is_mine(cell_content)
# Determines if an specific cell on the hidden map has a mine
################################################################

def is_mine(cell_content):
    if cell_content == -1:
        return True
    else:
        return False

################################################################
# Function: show(board_display, mine_camp, row, col)
# Discovers the content of the cell. Results may vary depending
# of flags, mines, etc.
################################################################

def show(board_display, mine_camp, row, col):
    a = mine_camp[row,col]
    b = board_display[row,col]
    [x_size, y_size] = shape(board_display)

    if is_visible(b) or is_flagged(b):
        return
    elif is_mine(a) and not is_flagged(b):
        return
    elif a > 0:
        board_display[row,col] = mine_camp[row,col]
        return board_display
    elif a == 0:
        board_display[row,col] = '0'
        SURROUNDING = ((row-1, col-1),(row-1, col),(row-1, col+1),
                       (row  , col-1),             (row  , col+1),
                       (row+1, col-1),(row+1, col),(row+1, col+1))
        for(surr_row, surr_col) in SURROUNDING:
            if(surr_row != 0 and surr_row != x_size and surr_col != 0 and surr_col != y_size):
                show(board_display, mine_camp, surr_row, surr_col)
################################################################
# Function: save_game(board_display, mine_camp)
# Saves the current game to files. Creates two files and not txt
################################################################

def save_game(board_display, mine_camp):
    file_display = 'last_game'
    file_Mine = 'mine_camp'

    display = open(file_display, 'wb')
    mines = open(file_Mine, 'wb')
    pickle.dump(board_display, display)
    pickle.dump(mine_camp, mines)

    display.close()
    mines.close()

    return

################################################################
# Function: load_game()
# Loads game from previously saved game.
################################################################

def load_game():
    file_display = 'last_game'
    file_Mine = 'mine_camp'
    try:
        obj1 = open(file_display, 'rb')
        obj2 = open(file_Mine, 'rb')
        display = pickle.load(obj1)
        mines = pickle.load(obj2)
    except:
        mines = [0, 0]
        display = [0, 0]

    return (display, mines)

################################################################
# Function: game_is_solved(board_display, x_size, y_size)
# Determines if the game is solved and no mines exploded
################################################################

def game_is_solved(board_display, x_size, y_size):
    for i in range(1, x_size):
        for j in range(1, y_size):
            a = board_display[i, j]
            if is_visible(a) or is_flagged(a):
                continue
            elif a != 'X':
                return False
            else:
                return False

    return True

################################################################
# Function: play_game(board_display, mine_camp, mines, x, y):
# Initialize the game. Size varies by the chosen option
################################################################

def play_game(board, mine_c, x, y):

    global is_playing
    global is_ended
    global board_display
    global mine_camp
    is_playing = True
    is_ended = False
    board_display = board
    mine_camp = mine_c
    counter = 0
    start_time = time.clock()

    while is_playing and not game_is_solved(board_display, x, y) and not is_ended:
        counter += 1
        print('\n Esta es la jugada No. ', counter)
        print(board_display)
        (x_pox, y_pox, flag) = get_move(x, y)
        a = board_display[x_pox, y_pox]
        b = mine_camp[x_pox, y_pox]
        if flag == 1:
            if not is_flagged(a) and not is_visible(a):
                board_display[x_pox, y_pox] = 'F'
            elif is_flagged(a) and is_visible(a):
                board_display[x_pox, y_pox] = ' '
        elif flag == 2 :
            is_ended = True
            break
        else:
            if is_visible(a) or is_flagged(a):
                pass
            elif is_mine(b):
                is_playing = False
                board_display[x_pox, y_pox] = 'X'
            else:
                show(board_display, mine_camp, x_pox, y_pox)

    print (board_display)

    end_time = time.clock()
    total_time = int(end_time - start_time)

    BOMB = ("""
                    \|/
                   .-*-
                  /
                 _|_
               ,"   ".
           (\ /  O O  \ /)
            \|    _    |/
              \  (_)  /
              _/.___,\_
            (_/       \_)
    """)

    FROG = ("""
               .-.   .-.
              ( o )_( o )
          __ / '-'   '-' \ __
         /  /      "
        |   \    _____,   /   |
         \  \`-._______.-'/  /
     _.-`   /\)         (/\   `-._
   (_     / /  /.___.\  \ \     _)
    (_.(_/ /  (_     _)  \ \_)._)
           (_(_)_)   (_(_)_)
    """)
    if game_is_solved(board_display,x, y) and not is_ended:
        print(FROG)
        print('Felicidades')
        print('Tu tiempo de juego fue de ', total_time, ' segundos.')
    elif not is_ended:
        print(BOMB)
        print('¡Ops! ¡Pisaste una mina!')
        print('Tu tiempo de juego fue de ', total_time, ' segundos.')
    else:
        print('¡Gracias por jugar!. Te esperamos nuevamente. \n')
        print('Tu tiempo de juego fue de ', total_time, ' segundos.')

    nan = input('Presione ENTER para volver al menú principal \n')

    menu()


#Initialize the game
menu()

