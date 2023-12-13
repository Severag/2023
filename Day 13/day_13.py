import re
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
        data = [line.strip().replace('#', '1').replace('.', '0') for line in f]
    
    patterns = []
    start = 0
    for idx,line in enumerate(data):
        if len(line) == 0:
            patterns.append(data[start:idx])
            start = idx + 1
        else:
            data[idx] = np.array([int(val) for val in line])
    patterns.append(data[start:])
    
    return [np.array(patt) for patt in patterns]



def solve(data):
    answer1 = part1(data)
    
    answer2 = part1(data, True)
    
    return [answer1, answer2]



def part1(data, allow_smudge=False):
    horiz, vert = [], []
    for pattern in data:
        h = check_rows(pattern, allow_smudge)  # horizontal reflection
        if h is None:
            v = check_rows(pattern.T, allow_smudge)  # vertical reflection
            if v is not None:
                vert.append(v)
        else:
            horiz.append(h)
    
    return sum(vert) + 100 * sum(horiz)



def check_rows(pattern, allow_smudge=False):
    for idx, row in enumerate(pattern[:-1]):
        # if this row matches the one after it
        diff = np.sum((row - pattern[idx+1])**2)
        
        if diff == 0:  # exact match
            # allow check_reflections to use smudge if check_rows can
            # since exact match means we didn't need to use it
            if check_reflection(pattern, idx, allow_smudge):
                return idx + 1  # + 1 because the answer is about count, not index
        elif allow_smudge and diff == 1:  # we have a smudge
            # check_reflections can't use a smudge, since we already one
            if check_reflection(pattern, idx, False):
                return idx + 1
        
    return None



def check_reflection(pattern, idx, allow_smudge=False):
    used_smudge = False
    # determine how many rows have to be equals
    bound = min(idx, len(pattern) - idx - 2)
    # march back through pattern, check each row matches its 
    # corresponding one about row = idx
    for offset in range(1, bound + 1):
        # if any don't match, it's a dud
        diff = np.sum((pattern[idx - offset] - pattern[idx + offset + 1])**2)
        if (allow_smudge and diff > 1) or (not allow_smudge and diff > 0):
            break
        elif diff == 1:  # if we used a smudge to get by
            used_smudge = True
    else:
        # either we're not using smudges, or we are and we actually used it
        return not allow_smudge or used_smudge    
    return False # it doesn't work out



def part2(data):
    return



puzzles = [['test_case.txt',    [405, 400]],
            ['puzzle_input.txt', []]]

for filename, answers in puzzles:
    data = read_file(filename)
    results = solve(data)
    print(f"\n\n{filename}")
    if 'test' in filename:
        [check(res, ans) for res, ans in zip(results, answers) if ans is not None]
    else:
        print(f"\t{results}")