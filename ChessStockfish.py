from stockfish import Stockfish
import subprocess


def stockfish_init(level):
    path = subprocess.getoutput('which stockfish')
    threads = int(subprocess.getoutput('grep -c ^processor /proc/cpuinfo')) // 2

    stockfish = Stockfish(path=path, depth=18, parameters={'Threads': threads, 'Skill Level': level})

    return stockfish


def find_position(sf_move_log, stockfish):
    stockfish.set_position(sf_move_log)
    best_move = stockfish.get_best_move()

    return best_move

'''
Convert best_move for give to the game
'''
def convert_best_move(best_move, side):

    move_converted = []

    if side == '< white >':
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
    else:
        convert = {
            'a': 7,
            'b': 6,
            'c': 5,
            'd': 4,
            'e': 3,
            'f': 2,
            'g': 1,
            'h': 0,
            '1': 0,
            '2': 1,
            '3': 2,
            '4': 3,
            '5': 4,
            '6': 5,
            '7': 6,
            '8': 7,
        }

    promotion = ''

    if len(best_move) == 5:
        promotion = best_move[-1]
        best_move = best_move[:-1]

    for i in best_move:
        move_converted.append(convert[i])

    start_square = tuple(move_converted[:2])[::-1]
    end_square = tuple(move_converted[2:])[::-1]

    return start_square, end_square, promotion
