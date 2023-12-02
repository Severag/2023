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
        data = f.readlines()
    
    return data



def solve(data, is_part1=True):
    import re
    regex = r'\d' if is_part1 else f"(?=({'|'.join(numbers)}))"
           
    nums = []
    for line in data:
        results = re.findall(regex, line)
        nums.append(10 * subs[results[0]] + subs[results[-1]])
   
    return sum(nums)



numbers = ['zero','one','two','three', 'four','five','six', 'seven','eight','nine']
numbers += [str(val) for val in range(10)]
subs = {n:(idx % 10) for idx,n in enumerate(numbers)}



test_case = read_file('test_case.txt')
test_case2 = read_file('test_case2.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 142 )
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case2, False), 281 )
print(solve(puzz_input, False))