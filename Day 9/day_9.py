import itertools
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
        data = [np.array([int(val) for val in line.strip().split(' ')]) for line in f]
    
    return data



def solve(data, is_part1=True):
    marginal_nums = []
    line_idx = -1 if is_part1 else 0
    
    for line in data:
        next_row = line[1:] - line[:-1]  # differences between the previous rows' entries
        # switches sign after each next() call
        mult = itertools.cycle([1]) if is_part1 else itertools.cycle([1,-1])
        # after calculating each row, just keep the relevant end
        ends = [next(mult) * line[line_idx], next(mult) * next_row[line_idx]]
        
        while not np.all(next_row == 0):
            next_row = next_row[1:] - next_row[:-1]
            ends.append(next(mult) * next_row[line_idx])
        
        marginal_nums.append(sum(ends))
    
    return sum(marginal_nums)



test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 114)
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False),  2)
print(solve(puzz_input, False))