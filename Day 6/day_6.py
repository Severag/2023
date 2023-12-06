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
        data = [re.findall('\d+', line) for line in f]
        
    return data



def solve(data, is_part1=True):   
    '''
        <race time>     = <hold time> + <travel time>
        <race distance> = <hold time> * <travel time>
        
        system of equations give a quadratic formula for either variable
    '''
    if is_part1:
        rules = [[int(val) for val in line] for line in data]
    else:
        rules = [[int(''.join(line))] for line in data]
    
    ways = []  # ways to win
    
    for time, dist in zip(*rules):
        sq_root = np.sqrt(time**2 - 4 * -1 * -dist)
        # first integer above this root beats the record
        x1 = int((-time + sq_root ) / -2 + 1)  
        # first integer below this root beats the record
        x2 = int((-time - sq_root ) / -2 - 1e-9)
        ways.append(x2 - x1 + 1)  # the count of integer ways to beat the record
    
    return np.prod(ways)



test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 288)
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False),  71503)
print(solve(puzz_input, False))  