import itertools
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
    return part1(data), part2(data)



def part1(data, state1=((0,0), True, True)):
    # state is ((row, col), moving along the row, moving down or right)
    energized = np.full_like(data, 0, dtype=int)
    
    open_list = [state1]
    closed_set = set()
    
    while open_list:
        state = open_list.pop()
        
        if state in closed_set:
            continue
        closed_set.add(state)
        
        (row, col), along_row, right_or_down = state
        
        delta = 1 if right_or_down else -1  # increasing or decreasing index
        if along_row:
            inds = np.s_[row, col::delta]
            ignore_split = '-'
        else:
            inds = np.s_[row::delta, col]
            ignore_split = '|'
        
        travel_space = data[inds]
        next_interact = np.where((travel_space != '.') & (travel_space != ignore_split))[0]
        
        if len(next_interact) > 0:  # if np.where found something to interact with
            idx = next_interact[0]
            # mark the travel spaces as energized
            energized[inds][:idx+1] = 1  # + 1 to include the object itself
            # get new points after the interaction
            row += 0           if along_row else idx  * delta
            col += idx * delta if along_row else 0
            open_list += post_interaction(data, row, col, along_row, right_or_down)
        else:   # light goes to end of board and stops bouncing around
            energized[inds] = 1
    
    return energized[energized > 0].size



splitters = {'|':[[-1, 0, False, False],
                  [ 1, 0, False,  True]],
             '-':[[ 0,-1,  True, False],
                  [ 0, 1,  True,  True]]}
def post_interaction(board, row, col, along_row, right_or_down):
    obj = board[row, col]
    
    if obj in splitters:  # split into beams going up and down or left and right
        output = []
        for r_offset, c_offset, now_row, now_r_or_d in splitters[obj]:
            output.append( ((row + r_offset, col + c_offset), now_row, now_r_or_d) )
    else:
        is_back = obj == '\\'
        delta = 1 if is_back == right_or_down else -1
        new_row = row + delta if along_row else row
        new_col =    col      if along_row else col + delta
        output = [((new_row, new_col), not along_row, is_back == right_or_down)]
    
    return [out for out in output if 0 <= out[0][0] < len(data) and 
                                     0 <= out[0][1] < len(data[0])]



def part2(data):
    energy_levels = []
    r_max = len(data) - 1
    c_max = len(data[0]) - 1
    
    for r_idx in range(r_max):
        energy_levels.append(part1(data, ((r_idx, 0), True, True)))
        energy_levels.append(part1(data, ((r_idx, c_max), True, False)))
    for c_idx in range(c_max):
        energy_levels.append(part1(data, ((0, c_idx), False, True)))
        energy_levels.append(part1(data, ((r_max, c_idx), False, False)))
    
    return max(energy_levels)
            



puzzles = [['test_case.txt',    [46, 51]],
            ['puzzle_input.txt', []]]

for filename, answers in puzzles:
    data = read_file(filename)
    results = solve(data)
    print(f"\n\n{filename}")
    if 'test' in filename:
        [check(res, ans) for res, ans in zip(results, answers) if ans is not None]
    else:
        print(f"\t{results}")