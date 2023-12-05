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
    break_line = lambda x: x.split(':')[1].split('|')
    get_nums = lambda x: [int(val) for val in re.findall('\d+', x)]
    
    with open( filename, 'r') as f:
        data = [[get_nums(half) for half in break_line(line)] for line in f]
    
    return data



def solve(data, is_part1=True):
    card_matches = np.zeros(len(data), dtype=int)
    
    for idx, [winners, mynums] in enumerate(data):
        card_matches[idx] = len([num for num in mynums if num in winners])
    
    if is_part1:
        return np.sum(2**card_matches // 2)
    else:
        counts = np.ones_like(card_matches)
    
        for idx, res in enumerate(card_matches):  
            counts[idx+1:idx+1+res] += counts[idx]
            # res is the # of matching numbers for this card
            # the next <res> cards get a new virtual card for every instance
            # (real and virtual) of the current card
        
        return counts.sum()



test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 13)
print(solve(puzz_input))  # it's 531932

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False), 30 )
print(solve(puzz_input, False))