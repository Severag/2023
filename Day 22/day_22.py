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
    parser = lambda X: [[int(val) for val in part.split(',')] for part in X]
    
    with open( filename, 'r') as f:
        data = [parser(line.split('~')) for line in f]
    
    return np.array(data)



def solve(data):
    num_redundant, p2_data = part1(data)
    
    return num_redundant, part2(p2_data)



def part1(data):
    jenga, locs = let_fall(data)
    
    redundancies = set()
    requireds = set()
    node_dict = dict()
    
    for lbl, slice_tup in enumerate(locs, start=1):
        # how many blocks support this one
        supports = []
        z_start = slice_tup[2].start
        if z_start > 0:  # if we're not on the ground
            # labels of blocks below this one
            supports = get_blocks_at((*slice_tup[:2], z_start - 1), jenga)
            
            # multiple blocks support us
            if len(supports) > 1:
                redundancies.update(supports)
            else:  # we need the one block below us
                requireds.update(supports)
             
            node_dict[-lbl] = supports
        
        # how many blocks are we supporting
        z_end = slice_tup[2].stop 
        aboves = get_blocks_at((*slice_tup[:2], z_end), jenga)
        
        if len(aboves) < 1:  # we're not supporting anything
            redundancies.add(lbl)  # we're redundant
        
        node_dict[lbl] = [[z_start, z_end - 1], supports, aboves]
    
    # first term remove blocks that are redundant for some blocks but required for others
    return len(redundancies - requireds), (requireds, node_dict)



def get_blocks_at(slice_tup, arr):
    nums = np.unique(arr[slice_tup])  # block labels in region
    return nums[np.nonzero(nums)]  # get rid of empty space (0-valued)



def let_fall(data):
    # sort blocks by which are closest to the ground
    # np.min() gets the lowest spot of the ones vertically oriented
    order_inds = np.argsort(np.min(data[..., 2], axis=1))
    blocks = data[order_inds]
    
    min_dim = np.min(data, axis=(0,1))
    max_dim = np.max(data, axis=(0,1))
    shape = max_dim - min_dim + 1
    
    stack = np.zeros(shape)
    blocks -= min_dim
    block_locs = []
    
    for idx, blk in enumerate(blocks):
        min_coord = np.min(blk, axis=0)
        max_coord = np.max(blk, axis=0)
        x_coords, y_coords, z_coords = [slice(start,end+1) for start,end in zip(min_coord, max_coord)]
        
        # z levels with previous blocks that'll keep us from falling all the way
        is_blocks = np.any(stack[x_coords, y_coords, :] > 0, axis=(0,1))
        if True in is_blocks:  # if there are blocks in the way
            # pick the level just above where the last interference is
            new_z = np.where(is_blocks)[0][-1] + 1
        else:
            new_z = 0
        # new_z = np.where(np.all(stack[x_coords, y_coords, :] == 0, axis=(0,1)))[0][0] + 1
        new_z_coords = slice(new_z, max_coord[2] - min_coord[2] + new_z + 1)
        
        stack[x_coords, y_coords, new_z_coords] = idx + 1
        block_locs.append((x_coords, y_coords, new_z_coords))
    
    return stack, block_locs



def part2(data):
    requireds, node_dict = data
    chain_lens = []
        
    for start in requireds:
        open_list = [(0, start)]
        closed_set = set()
        
        while open_list:
            _, block = heapq.heappop(open_list)
            [z_start, z_end], supports, aboves = node_dict[block]
            
            # block is an unvisited node, 
            # AND (all its supports have been visited ('<=' here means "is subset of")
            #      OR it's the starting block)
            if block not in closed_set and (set(supports) <= closed_set or start == block):
                closed_set.add(block)
                [heapq.heappush(open_list, (z_end + 1, blk)) for blk in aboves]
        
        chain_lens.append(len(closed_set) - 1)  # subtract 1 for the starting block
    
    return sum(chain_lens)



puzzles = [['test_case.txt',    [5, 7]],
           ['puzzle_input.txt', []]]

for filename, answers in puzzles:
    data = read_file(filename)
    results = solve(data)
    print(f"\n\n{filename}")
    if 'test' in filename:
        [check(res, ans) for res, ans in zip(results, answers) if ans is not None]
    else:
        print(f"\t{results}")