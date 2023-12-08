import re, math
import numpy as np

def check(myanswer, answer):
    if not np.array_equal(myanswer, answer):
        print('\n' + 'ERROR'.center(50,'*'))
        print('Correct answer:')
        print(answer)
        print('Returned answer:')
    else:
        print('Check passed!')
    print(myanswer)



def read_file(filename):
    with open( filename, 'r') as f:
        instr = [1 if char == 'R' else 0 for char in next(f).strip()]
        _ = next(f)
        data = [re.findall('\w{3}', line) for line in f]
    
    graph = {key:values for key, *values in data}
    
    return instr, graph



def solve(data, is_part1=True):
    if not is_part1:
        return solve_part2(data)
    
    instr, graph = data
    
    cur_node = 'AAA'
    idx = 0
    
    while cur_node != 'ZZZ':
        side = instr[idx % len(instr)]
        cur_node = graph[cur_node][side]
        
        idx += 1
    
    return idx



def solve_part2(data):
    instr, graph = data
    
    # each starting node will have its own path through the graph
    cur_nodes = [key for key in graph.keys() if key.endswith('A')]
    steps = [[] for _ in cur_nodes]
    freqs = [False for _ in cur_nodes]
    idx = 0
    
    while True:
        # advance
        side = instr[idx % len(instr)]
        cur_nodes = [graph[node][side] for node in cur_nodes]
        idx += 1
        
        # keep track of how often each path arrives at a Z-ending node
        all_Zs = True  # are all them right now at Z-ending nodes?
        for n_idx,node in enumerate(cur_nodes):
            if node.endswith('Z'):
                steps[n_idx].append(idx)
                
                if len(steps[n_idx]) > 1 and not freqs[n_idx]:
                    freqs[n_idx] = steps[n_idx][-1] - steps[n_idx][-2]
            else:
                all_Zs = False
        
        # end conditions
        if all_Zs:  # all Z-enders right now
            return idx 
        elif False not in freqs:  # we know enough to predict when it'll happen
            lcm = 1  # least common multiple
            for val in freqs:
                lcm = math.lcm(lcm, val)
            return lcm



test_case = read_file('test_case.txt')
test_case2 = read_file('test_case2.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 2)
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case2, False),  6)
print(solve(puzz_input, False))  # 17_099_847_107_071