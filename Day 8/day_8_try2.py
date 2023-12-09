import re
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
    if is_part1:
        end_cond = lambda x: x == 'ZZZ'
        return solve_part1(data, 'AAA', end_cond)
    else:
        As = [key for key in data[1].keys() if key.endswith('A')]
        end_cond = lambda x: x.endswith('Z')
        
        freqs = [solve_part1(data, start, end_cond) for start in As]
        
        return np.lcm.reduce(freqs, dtype=np.longlong)



def solve_part1(data, start, at_end_func):
    instr, graph = data
    
    cur_node = start
    idx = 0  # cur_node is position at the end of <idx> after it's been updated
    
    while not at_end_func(cur_node):
        side = instr[idx % len(instr)]
        cur_node = graph[cur_node][side]
        
        idx += 1
    
    return idx



test_case = read_file('test_case.txt')
test_case2 = read_file('test_case2.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 2)
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case2, False),  6)
print(solve(puzz_input, False))  # 17_099_847_107_071