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
        data = [np.array(list(f".{line.strip()}.")) for line in f]
    
    # f-string and this line create an "empty" border around the main part of the board
    data = [np.full_like(data[0], '.')] + data + [np.full_like(data[0], '.')]
    
    return np.array(data)



def solve(data, is_part1=True):
    
    answer1, loop_points = part1(data)
    answer2 = part2(data, loop_points)
    
    return answer1, answer2



def part1(data):
    start = tuple(np.argwhere(data == 'S')[0])
    
    open_list = [(0, start)]
    dists = {start:0}
    closed_set = set()
    
    while open_list:
        cur_dist, cur_node = heapq.heappop(open_list)
        
        # if we haven't already visited this node
        if cur_node not in closed_set:
            closed_set.add(cur_node)
            
            for adj in get_adjacent(data, cur_node):
                if adj not in closed_set:
                    heapq.heappush(open_list, (cur_dist + 1, adj))
                
                dists[adj] = min(dists.get(adj, np.inf), cur_dist + 1)
        
    return max(dists.values()), closed_set
    


def get_adjacent(graph, point, on_loop=True):
    if on_loop:
        label = graph[point]
        
        if label != 'S':
            return [tuple(point + offset) for offset in translator[label]]
        else:
            valid = []
            for offset in translator[label]:
                cand = tuple(point + offset)
                # if cand is a pipe and it has a leg that points back at point
                if (graph[cand] != '.' and 
                     np.all(-offset == translator[graph[cand]], axis=1).any()):
                    valid.append(cand)
            return valid
    else:
        # get all 8 adjacents
        adjacents = [(point[0] + r, point[1] + c) for r in [-1,0,1] for c in [-1,0,1] if not r == c == 0]
        # weed out any that go outside the limits of the array
        adjacents = [val for val in adjacents if 0 <= val[0] < graph.shape[0] and 
                     0 <= val[1] < graph.shape[1]]
        return adjacents



def part2(data, loop_points):
    new_board = upscale_board(data, loop_points)
    open_set = {(0,0)}
    closed_set = set()
    
    while open_set:
        cur_node = open_set.pop()
        
        # if we haven't already visited this node
        if cur_node not in closed_set:
            closed_set.add(cur_node)
            new_board[cur_node] = 'O'
            
            for adj in get_adjacent(new_board, cur_node, False):
                # spot isn't in the loop and hasn't been visited before
                if new_board[adj] == 'x' and adj not in closed_set:  
                    open_set.add(adj)
    
    new_board[1::2] = 'N'  # mark the spaces created for new_board 'N' for new
    new_board[:, 1::2] = 'N'
    
    # now, only the inside spaces should still be unmodified, aka 'x's
    return new_board[new_board == 'x'].size



def upscale_board(old_board, loop_points):
    def convert_loc(point):
        return (point[0]*2, point[1]*2)
    
    new_board = np.full(convert_loc(old_board.shape), 'x')
    
    for node in loop_points:
        new_loc = convert_loc(node)
        new_board[new_loc] = data[node]
        
        if data[node] != 'S':
            # extend its arms out to cover new gaps
            for offset in translator[data[node]]:
                new_board[tuple(new_loc + offset)] = '|' if offset[1] == 0 else '-'
    
    return new_board



# converts letters to relative directions
translator = {'|':np.array([[-1, 0],[ 1, 0]]),
              '-':np.array([[ 0,-1],[ 0, 1]]),
              'L':np.array([[-1, 0],[ 0, 1]]),
              'J':np.array([[-1, 0],[ 0,-1]]),
              '7':np.array([[ 1, 0],[ 0,-1]]),
              'F':np.array([[ 1, 0],[ 0, 1]]),
              '.':np.array([]),
              'S':np.array([[-1, 0],[ 1, 0],[ 0,-1],[ 0, 1]])}

puzzles = [['test_case.txt',    [8,        1]],
           ['test_case2.txt',   [None,    10]],
           ['test_case3.txt',   [None,     8]],
           ['puzzle_input.txt', [None, None]]]


for filename, answers in puzzles:
    data = read_file(filename)
    results = solve(data)
    print(f"\n\n{filename}")  #:{'-'}^50
    if 'test' in filename:
        [check(res, ans) for res, ans in zip(results, answers) if ans is not None]
    else:
        print(f"\t{results}")