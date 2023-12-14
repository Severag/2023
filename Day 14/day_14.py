import re
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
        data = np.array([np.array(list(line.strip())) for line in f])
    
    return data



def solve(data):
    answer1 = part1(data)
    answer2 = part2(data)
    
    return [answer1, answer2]



def part1(data):
    new_board = roll(data)
    
    return find_load(new_board)



def roll(board):
    new_board = np.full_like(board, '.')
    new_board[board == '#'] = '#'
    
    for idx,col in enumerate(board.T):
        # get places the rocks roll between (beginning, square rocks, end)
        stops = np.insert([-1, col.size], 1, np.where(col == '#')[0]) + 1
        
        # consolidate the rocks at the next lowest stopping point
        for start,end in zip(stops[:-1], stops[1:]):
            rock_num = np.count_nonzero(col[start:end] == 'O')
            new_board[start:start+rock_num, idx] = 'O'
    
    return new_board



def find_load(board):
    row_count = np.count_nonzero(board == 'O', axis=1)
    dists = np.arange(len(board), 0, -1)
    load = np.sum(row_count * dists)
    
    return load



def part2(data):
    # board as string: list of which cycles they appeared
    prev_states = {str(data):[0]}
    time = 1_000_000_000
    
    # for each cycle
    for idx in range(1, time):
        # roll the rocks north, west, south, and east
        for _ in range(4):
            data = roll(data)  # roll
            data = np.rot90(data, axes=(1,0))  # align board with new direction
        
        # see if we can extrapolate out to the state at cycle = <time>
        key = np.array2string(data, 500, threshold=10000)
        # 500 keeps each row on 1 line, threshold prevents replacing rows with '...'
        if key in prev_states:  # if we've been here before
            # check if we can repeat from here to exactly 1 billion    
            freq = idx - prev_states[key][-1]
            if (time - idx) % freq == 0:  
                # then this will also be the state at 1 billion
                return find_load(data)
        # else:
        prev_states[key] = prev_states.get(key, []) + [idx]



puzzles = [['test_case.txt',    [136, 64]],
            ['puzzle_input.txt', []]]

for filename, answers in puzzles:
    data = read_file(filename)
    results = solve(data)
    print(f"\n\n{filename}")
    if 'test' in filename:
        [check(res, ans) for res, ans in zip(results, answers) if ans is not None]
    else:
        print(f"\t{results}")