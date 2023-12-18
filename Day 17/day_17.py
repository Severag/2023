import heapq
import numpy as np

def check(myanswer, answer):
    if not np.array_equal(myanswer, answer):
        print(f"\n\t{'ERROR':{'*'}^50}\n"
              f"\tCorrect answer: \t{answer}\n"
              f"\tReturned answer:\t{myanswer}")
    else:
        print(f"\tCheck passed!   \t{myanswer}")



def read_file(filename):
    with open( filename, 'r') as f:
        data = np.array([[int(val) for val in line.strip()] for line in f])
    
    return data



def solve(data):
    return part1(data), part2(data)



def part1(data):
    end_point = (len(data) - 1, len(data[-1]) - 1)
    return Astar(data, (0,0), end_point, get_moves)



def Astar(data, start, end, move_func):
    #        (heuristic, g score, point, last_dir, count)
    state = (0 + heuristic(start, end), 0, start, None, 0)
    
    open_list = [state]
    closed_set = set()
    
    while open_list:
        state = heapq.heappop(open_list)
        _, g_score, point, last_dir, count = state
        
        if np.array_equal(point, end):  # we've reached the end
            break
        elif (point, last_dir) in closed_set:
            continue
        
        closed_set.add((point, last_dir))
        
        for cand, its_dir, its_count, delta_g in move_func(data, point, last_dir, count):
            cand_g = g_score + delta_g  # heat loss
            cand_f = cand_g + heuristic(cand, end)
            
            new_state = (cand_f, cand_g, cand, its_dir, its_count)
            if (cand, its_dir) not in closed_set:
                heapq.heappush(open_list, new_state)
    
    return g_score



def heuristic(point, end_point):
    # Manhattan distance
    return abs(point[0] - end_point[0]) + abs(point[1] - end_point[1])



dirs = [[( 1,  0), (-1,  0)],
        [(-1,  0), ( 1,  0)],
        [( 0,  1), ( 0, -1)],
        [( 0, -1), ( 0,  1)]]
def get_moves(board, point, last_dir, count):
    outputs = []
    
    for this_dir, opposite in dirs:
        g_score = 0
        # can't go in reverse direction, assume previous function call handled
        # going in the same direction multiple times
        if last_dir != opposite and last_dir != this_dir:
            for idx in range(1, 4):
                new_point = (point[0] + this_dir[0] * idx, 
                             point[1] + this_dir[1] * idx)
                
                # if we're in bounds
                if 0 <= new_point[0] < len(board) and 0 <= new_point[1] < len(board[0]):
                    g_score += board[new_point]
                    outputs.append([new_point, this_dir, idx, g_score])
    
    return outputs



def part2(data):
    end_point = (len(data) - 1, len(data[-1]) - 1)
    return Astar(data, (0,0), end_point, get_moves_part2)



def get_moves_part2(board, point, last_dir, count):
    outputs = []
    
    for this_dir, opposite in dirs:
        g_score = 0
        # can't go in reverse direction, assume previous function call handled
        # going in the same direction multiple times
        if last_dir != opposite and last_dir != this_dir:
            for idx in range(1, 11):  # can only move [4,10] blocks
                new_point = (point[0] + this_dir[0] * idx, 
                             point[1] + this_dir[1] * idx)
                
                # if we're in bounds
                if 0 <= new_point[0] < len(board) and 0 <= new_point[1] < len(board[0]):
                    g_score += board[new_point]
                    
                    # if we've moved far enough
                    if idx >= 4:
                        outputs.append([new_point, this_dir, idx, g_score])
    
    return outputs
            


puzzles = [['test_case.txt',    [102, 94]],
            ['puzzle_input.txt', []]]

for filename, answers in puzzles:
    data = read_file(filename)
    results = solve(data)
    print(f"\n\n{filename}")
    if 'test' in filename:
        [check(res, ans) for res, ans in zip(results, answers) if ans is not None]
    else:
        print(f"\t{results}")