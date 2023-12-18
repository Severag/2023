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
    # return one capital letter, a number with however many digits, an alphanumeric
    # string of however many digits bracketed by parentheses
    regex = r'([A-Z]{1}) ([\d]+) \(#([\w]+)\)'
    
    dirs = {'R':np.array([ 0,  1]),
            'D':np.array([ 1,  0]),
            'L':np.array([ 0, -1]),
            'U':np.array([-1,  0])}
    dirs.update({str(key):val for key,val in zip(range(4),dirs.values())})
    
    hex_converter = lambda x: [dirs[x[-1]], int(x[:-1], 16)]
    parser = lambda x,y,z: [dirs[x], int(y), hex_converter(z)]
    
    with open( filename, 'r') as f:
        data = [parser(*re.findall(regex, line)[0]) for line in f]
    
    return data



def solve(data):
    return part1(data), part2(data)



def part1(data):
    # get all the points that make up the outline
    start = (0, 0)
    outline = [start]
    
    for idx, (this_dir, count, _) in enumerate(data):        
        for _ in range(count):
            outline.append(tuple(outline[-1] + this_dir))
    
    # create a board large enough to fit all the points
    out_arr = np.array(outline)
    mins = np.min(out_arr, axis=0)
    maxs = np.max(out_arr, axis=0) + 1 - mins + 2
    # '+ 1' to get desired array size, '- mins' to account for the path straying
    # into the negatives, '+ 2' to create border around outline
    out_arr += 1 - mins  # map points onto new locations in board
    board = np.zeros(maxs)
    board[tuple(out_arr.T)] = 1  # mark the location of the outline
    
    # find the exterior space
    open_list = [(0, 0)]
    
    while open_list:
        point = open_list.pop()
        
        if board[point] != 0:  # we've visited this point already, or it's in the outline
            continue        
        board[point] = -1  # mark this location as outside
        
        # only keep adjacent points if they haven't been visited and aren't in the outline
        # aka, board[cand] == 0
        open_list += [cand for cand in get_adj(board, point) if board[cand] == 0]
    
    # find interior space
    board[board == 0] = 1  # only points within outline are left as zeros
    board[board < 0] = 0  # mark outside as 0, inside as 1        
    
    return int(np.sum(board))



def get_adj(board, point):
    x, y = point
    cands = []
    for dx, dy in zip([1, -1, 0, 0], [0, 0, 1, -1]):
        new_x = x + dx
        new_y = y + dy
        if 0 <= new_x < len(board) and 0 <= new_y < len(board[new_x]):
            cands.append((new_x, new_y))
    
    return cands



def part2(data):
    # Shoelace formula
    # length + 1 because the starting point will also be the ending point
    corners = np.zeros([len(data) + 1, 2], dtype=np.longlong)
    perimeter = 0  # how many points are in the outline
    
    # use the hexidecimal-derived points
    for idx, (_, _, (this_dir, count)) in enumerate(data, start=1):
        corners[idx] = corners[idx-1] + this_dir * count
        
        perimeter += np.abs(np.sum(corners[idx] - corners[idx-1]))
    
    shoe1 = np.sum(corners[:-1, 0] * corners[1:, 1])  # x_i * y_(i+1)
    shoe2 = np.sum(corners[:-1, 1] * corners[1:, 0])  # y_i * x_(i+1)    
    area = 0.5 * np.abs(shoe1 - shoe2)
    
    # Pick's theorem
    # Area = # of interior points + (# of exterior points) / 2 - 1
    # A = i + b/2 - 1
    # so we want i + b, and we know A (area) and b (perimeter)
    # A + b/2 = i + b - 1
    # A + b/2 + 1 = i + b
    
    return area + perimeter / 2 + 1
            


puzzles = [['test_case.txt',    [62, 952_408_144_115]],
            ['puzzle_input.txt', []]]

for filename, answers in puzzles:
    data = read_file(filename)
    results = solve(data)
    print(f"\n\n{filename}")
    if 'test' in filename:
        [check(res, ans) for res, ans in zip(results, answers) if ans is not None]
    else:
        print(f"\t{results}")