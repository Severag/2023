import heapq, collections, math, re
import numpy as np
from functools import cache

def check(myanswer, answer):
    if not np.array_equal(myanswer, answer):
        print(f"\n\t{'ERROR':{'*'}^50}\n"
              f"\tCorrect answer: \t{answer}\n"
              f"\tReturned answer:\t{myanswer}")
    else:
        print(f"\tCheck passed!   \t{myanswer}")



def read_file(filename):
    conversion = {'#':-2,
                  '.':-1,
                  'S': 0}
    
    with open( filename, 'r') as f:
        data = [[conversion[char] for char in line.strip()] for line in f]
    
    return np.array(data)



def solve(data):
    return part1(data), part2(data)



def part1(data):
    limit = 6 if len(data) < 16 else 64
    start = tuple(np.squeeze(np.where(data == 0)))
    
    return find_spots(data, limit, start)



def find_spots(data, limit, start, return_board=False):
    board = np.array(data)
    # time, point
    open_list = [(0, start)]
    
    while open_list:
        state = heapq.heappop(open_list)
        time, point = state
        
        # end condition #1
        if board[point] > 0:
            continue  # skip it if it's already been visited
        
        board[point] = time
        
        # end condition #2
        if time == limit:  # time's up!
            continue  # don't calculate any more moves
        
        for new_point in get_adj(data, point):
            cand = (time + 1, new_point)
            heapq.heappush(open_list, cand)
    
    # reachable spots are those whose distance from start matches the even/odd
    # of the limit, excluding rocks and places we didn't visit
    spots = np.count_nonzero((board % 2 == limit % 2) & (board >= 0))
    
    if return_board:
        return spots, board
    else:
        return spots



def get_adj(board, point):
    adjacents = []
    for dr, dc in zip([1,-1,0,0],[0,0,1,-1]):
        cand = (point[0] + dr, point[1] + dc)
        if 0 <= cand[0] < len(board) and 0 <= cand[1] < len(board[cand[0]]):
            if board[cand] == -1:  # cand is an unvisited open spot
                adjacents.append(cand)
    
    return adjacents



def part2(data):
    length = len(data)
    
    if length < 100:
        return None  # skip test case
    
    goal = 26501365  # desired number of steps
    offset = goal % length
    test_limits = [offset, 
                   offset + length, 
                   offset + length * 2]
    spots = [0] * len(test_limits)
    
    limit = test_limits[-1]  # max board size needed
    # needs to be odd and symmetric (aka [x,x])
    num_tiles = round(limit / length) * 2 + 1
    board = np.tile(data, (num_tiles, num_tiles))
    
    start_inds = np.array(np.where(board == 0))  # since we tiled, there are multiple matches
    # so get which of the points in start_inds are closest to the center
    idx = np.argmin(np.sum(np.abs(start_inds - len(board) // 2), axis=0))
    start = tuple(start_inds[:, idx])
    board[start_inds] = -1  # the other points aren't special anymore
    board[start] = 0
    
    # board, now with distances from the start
    spots[-1], board = find_spots(board, limit, start, True)
    for idx, limit in enumerate(test_limits):
        spots[idx] = np.count_nonzero((board % 2 == limit % 2) & (board >= 0) & (board <= limit))
    
    from numpy.polynomial import Polynomial
    extrap = Polynomial.fit(test_limits, spots, 2, window=[offset, goal])
    return int(extrap(goal))



puzzles = [['test_case.txt',    [16, None]],
           ['puzzle_input.txt', []]]

for filename, answers in puzzles:
    data = read_file(filename)
    results = solve(data)
    print(f"\n\n{filename}")
    if 'test' in filename:
        [check(res, ans) for res, ans in zip(results, answers) if ans is not None]
    else:
        print(f"\t{results}")