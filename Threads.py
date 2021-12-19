from multiprocessing import Process, Queue, cpu_count
import ChessAI

class Threads:
    def __init__(self):
        # Get number of CPU threads
        self.cpu = cpu_count()
        # Make process
        self.process = []
        self.return_queue = Queue()

        for process in range(self.cpu):
            move_finder_process = None
            self.process.append(move_finder_process)

    def start(self, gs, valid_moves):
        # Split valid_moves

        valid_moves_split_lenght = len(valid_moves) / self.cpu

        valid_moves_list = []
        for i in range(self.cpu):
            valid_moves_list.append([])

        j = 0

        for i, move in enumerate(valid_moves):
            valid_moves_list[j].append(move)
            j += 1
            if j >= self.cpu:
                j = 0        

        # Init process
        for i, process in enumerate(self.process):
            process = Process(target=ChessAI.find_best_move, args=(gs, valid_moves_list[i], self.return_queue, i))
            self.process[i] = process
        # Start process
        for process in self.process:
            process.start()

    def kill(self):
        # Stop process
        for process in self.process:
            process.kill()

    def terminate(self):
        # Terminate process
        for process in self.process:
            process.terminate()
    
    def is_alive(self):
        # Process alive or not ?
        count_alive = 0
        for process in self.process:
            if process.is_alive(): count_alive += 1

        if count_alive != 0:
            return True
        else:
            return False
    
    def best_move(self):
        
        scores = []

        for move in self.process:
            scores.append(self.return_queue.get())

        best_score = 0
        i_best_score = 0 
        for i, score in enumerate(scores):
            score = score[1]
            if score > best_score:
                best_score = score
                i_best_score = i 

        best_move = scores[i_best_score][0]

        print(best_move)
        return best_move