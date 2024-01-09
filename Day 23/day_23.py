import heapq, collections, itertools
import numpy as np

def check(myanswer, answer):
    if not np.array_equal(myanswer, answer):
        print(f"\n\t{'ERROR':{'*'}^50}\n"
              f"\tCorrect answer: \t{answer}\n"
              f"\tReturned answer:\t{myanswer}")
    else:
        print(f"\tCheck passed!   \t{myanswer}")



def read_file(filename):
    translator = {'#':-1,
                  '.': 0,
                  '^': 1,
                  '>': 2,
                  'v': 3,
                  '<': 4}
    with open( filename, 'r') as f:
        data = [[translator[char] for char in line.strip()] for line in f]
    
    return np.array(data)



def solve(data):
    return part1(data), part2(data)



def part1(data):
    # get start and end locations
    start = (0, np.where(data[0] == 0)[0][0])
    end = (len(data) - 1, np.where(data[-1] == 0)[0][0])
    
    node_map = reduce(data, start, end)
    
    # initialize search
    open_list = [(0, start, None, 0)]  # dist^-1 from start, loc, old_loc, true dist
    # used the inverse total path length as a heuristic to get a good starting
    # set of values that'll make it easier to trim underperforming paths
    closed_dict = dict()
    
    while open_list:
        inv_dist, point, old_point, actual_dist = open_list.pop()
        
        # we've been here before
        if point in closed_dict:
            if closed_dict[point] >= actual_dist:  # prev way was longer (aka 'better')
                continue  # skip this path
        
        closed_dict[point] = actual_dist
        
        # go to next nodes
        for cand, d_dist in node_map[point].items():
            path_len = actual_dist + d_dist
            heapq.heappush(open_list, (path_len**-1, cand, point, path_len))
    
    return closed_dict[end]



def reduce(data, start, end):
    '''
    reduce <data> from a map of the terrain into a node-based graphical 
    representation of it
    '''
    # get intersections
    nodes = [start, end]    
    
    for r_idx,row in enumerate(data):
        for c_idx,val in enumerate(row):
            point = (r_idx, c_idx)
            
            # if it's an open spot at the intersection of two or more lines
            if val >= 0 and len(get_adj(data, point)) > 2:
                nodes.append(point)
    
    # find distances between nodes
    dists = dict()
    for inter in nodes:
        this_node = dict()
        for adj in get_adj(data, inter):
            this_node.update(trace_path(data, inter, adj))
        
        dists[inter] = this_node
    
    return dists        
            


def get_adj(board, point, prev=None):
    directions = {1:(-1, 0),
                  2:( 0, 1),
                  3:( 1, 0),
                  4:( 0,-1)}
    
    adjacents = []
    for dr, dc in zip([1,-1,0,0],[0,0,1,-1]):
        cand = (point[0] + dr, point[1] + dc)
        
        if 0 <= cand[0] < len(board) and 0 <= cand[1] < len(board[cand[0]]) and cand != prev:
            if board[cand] >= 0:  # cand is an open spot
                
                # if we're not in prev mode OR current point is flat OR we're moving down the slope
                if prev is None or board[point] == 0 or (dr, dc) == directions[board[point]]:
                    adjacents.append(cand)
    
    return adjacents



def trace_path(board, old_point, point):
    '''
    follow along a single path until it branches
    return the branch point and the distance from the start as a dictionary
    '''
    dist = 1
    
    # loop until the next intersection
    while True:
        next_steps = get_adj(board, point, prev=old_point)
        
        if point[0] == len(board) - 1:  # we reached the end
            break
        elif len(next_steps) == 0:  # found a dead end
            return dict()  # return nothing
        if len(next_steps) > 1:  # found an intersection
            break
        
        # setup next loop
        old_point = point
        point = next_steps[0]
        dist += 1
    
    # return point of new intersection and the distance from starting intersection
    return {point:dist}



def part2(data):
    no_slopes = np.array(data)
    no_slopes[no_slopes>0] = 0  # make all slopes flat ground
    
    return undirected_graph(no_slopes)



def undirected_graph(data):
    '''
    variation on Part1() to deal with the possibility of looping within a path
    '''
    # get start and end locations
    start = (0, np.where(data[0] == 0)[0][0])
    end = (len(data) - 1, np.where(data[-1] == 0)[0][0])
    
    node_map = reduce(data, start, end)
    
    # initialize search
    open_list = [(0, start, dict())]  # true dist, loc, old_locations
    end_dist = 0
    end_paths = []
    
    while open_list:
        actual_dist, point, path = open_list.pop()
        
        # if this path has been here before
        if point in path:
            continue  # can't revist a node more than once
        
        path = path | {point:actual_dist}
    
        # if this is at the end
        if point == end:
            end_paths.append(path)
            end_dist = max(end_dist, actual_dist)
            continue
        
        # go to next nodes
        for cand, d_dist in node_map[point].items():
            if cand not in path:
                path_len = actual_dist + d_dist
                open_list.append((path_len, cand, path))
    
    return end_dist



puzzles = [['test_case.txt',    [94, 154]],
           ['puzzle_input.txt', []]]

for filename, answers in puzzles:
    data = read_file(filename)
    results = solve(data)
    print(f"\n\n{filename}")
    if 'test' in filename:
        [check(res, ans) for res, ans in zip(results, answers) if ans is not None]
    else:
        print(f"\t{results}")