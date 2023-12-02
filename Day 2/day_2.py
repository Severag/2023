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
    regex = r'(\d+) (red|blue|green)'
    
    with open( filename, 'r') as f:
        data = [re.findall(regex, line) for line in f]
    
    return data



def solve(data, is_part1=True):
    if not is_part1:
        return solve_p2(data)
    
    # else
    limits = {'red':12, 'green':13, 'blue':14}
    
    good_games = []
    for idx, game in enumerate(data):
        for count, color in game:  # game is a list of ('number', 'color') tuples
            if int(count) > limits[color]:  # an illegal game
                break
        else:  # if we didn't break, then it was a good game!
            good_games.append(idx+1)
    
    return sum(good_games)



def solve_p2(data):
    powers = []
    for idx, game in enumerate(data):
        mins = {'red':0, 'green':0, 'blue':0}
        
        for count, color in game:  # game is a list of ('number', 'color') tuples
            mins[color] = max(mins[color], int(count))
        
        powers.append(np.prod(list(mins.values())))
    
    return sum(powers)



test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 8 )
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False), 2286 )
print(solve(puzz_input, False))