from lib2to3.pytree import convert
from stockfish import Stockfish
import subprocess

import ChessEngine

stockfish = Stockfish(path=subprocess.getoutput('which stockfish'), depth=12, parameters={'Threads':4})


def find_position(sf_move_log):
    stockfish.set_position(sf_move_log)
    best_move = stockfish.get_best_move()

    return best_move

'''
Convert best_move for give to the game
'''
def convert_best_move(best_move):

    move_converted = []

    convert = {
        'a': 0,
        'b': 1,
        'c': 2,
        'd': 3,
        'e': 4,
        'f': 5,
        'g': 6,
        'h': 7,
        '1': 7,
        '2': 6,
        '3': 5,
        '4': 4,
        '5': 3,
        '6': 2,
        '7': 1,
        '8': 0,
        }

    promotion = ''

    if len(best_move) == 5:
        promotion = best_move[-1]
        best_move = best_move[:-1]

    for p in best_move:
        for i in p:
            move_converted.append(convert[i])

    start_square = tuple(move_converted[:2])[::-1]
    end_square = tuple(move_converted[2:])[::-1]

    return start_square, end_square, promotion
