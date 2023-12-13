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
    parser = lambda x,y: tuple([x + 'x', tuple(int(val) for val in y.split(','))])
    with open( filename, 'r') as f:
        data = [parser(*line.strip().split(' ')) for line in f]
    
    return data



def solve(data):
    
    answer1 = [part1(line, 0) for line in data]
    
    answer2 = part2(data)
    
    return [sum(answer1), answer2]



def part1(state, combo):
    report, lengths = state
    
    # end conditions
    test = memoizator.get(state, None)
    if test is not None:
        return test
    elif len(lengths) == 0 and '#' not in report:
        return 1  # successful match
    elif len(lengths) == 0 or len(report) == 0:
        return 0  # left some broken springs on the table or ran out of report too early
    
    L = lengths[0]
    # look ahead for some combination of # or ? that is <L> long and has 
    # a ., ?, or x after it. x being something I added to the end of each report
    regex = r'(?=([\#\?]{%d}[\.\?x]))' % (L,)
    
    answers = []
    # for all the places the first segments could start
    for match in re.finditer(regex, report):
        if not '#' in report[:match.start()]:  # if we're not leaving a broken spring behind
            idx = match.start() + L + 1  # start of match + match length + buffer
            new_state = (report[idx:].lstrip('.'), lengths[1:])
            ans = memoizator.get(new_state, part1(new_state, combo))
            answers.append(ans)
    
    memoizator[state] = sum(answers)
    
    return memoizator[state]



def part2(data):
    answers = []
    for report, lengths in data:
        r5 = '?'.join([report[:-1]] * 5) + 'x'  # [:-1] to remove 'x' I added
        L5 = lengths * 5
        answers.append(part1((r5, L5), 0))
    
    return sum(answers)



memoizator = dict()  # (report, lengths): combinations that fit

puzzles = [['test_case.txt',    [21, 525152]],
            ['puzzle_input.txt', []]]

for filename, answers in puzzles:
    data = read_file(filename)
    results = solve(data)
    print(f"\n\n{filename}")
    if 'test' in filename:
        [check(res, ans) for res, ans in zip(results, answers) if ans is not None]
    else:
        print(f"\t{results}")