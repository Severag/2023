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
        data = [line.strip() for line in f]
    
    return data



def solve(data, is_part1=True):
    # get anything that isn't a number or a period  -or-  get each asterisk
    regex = r"[^0-9\.]"  if is_part1 else r"\*"
    
    found = set()
    for idx,line in enumerate(data):
        for match in re.finditer(regex, line):
            col = match.start()
            this_match = set()
            
            for r_idx in range(idx-1, idx+2, 1):
                for c_idx in range(col-1, col+2, 1):
                    if data[r_idx][c_idx].isdigit():
                        # store the number and its associated indices to the set 
                        # to remove duplicates
                        this_match.add(get_number(data[r_idx], c_idx) + (idx,))
        
            if is_part1:
                found |= this_match  # merge this_match with found
            elif len(this_match) == 2:  # if this is part 2 and we have a gear
                ratio = np.prod([int(item[0]) for item in this_match])
                found.add((ratio, idx))  # just keep the ratio and index
    
    return sum([int(item[0]) for item in found])



def get_number(line, pos):
    for start in range(pos, -1, -1):
        if not line[start].isdigit():
            start += 1
            break
    
    for end in range(pos, len(line), 1):
        if not line[end].isdigit():
            break
    else:  # if we reached the end of the line without breaking
        end += 1  # move end up to include the last digit of the line
    
    return line[start:end], start, end



test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 4361)
print(solve(puzz_input))  # it's 531932

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False), 467835 )
print(solve(puzz_input, False))