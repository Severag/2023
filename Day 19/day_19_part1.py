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
    comp_dict = {'<':lambda x,y: x < y,
                 '>':lambda x,y: x > y}
    cond_parser = lambda x1,x2,x3,x4: [x1, comp_dict[x2], int(x3), x4]
    regex_p = '(\w)([<>])(\d+):(\w+)'  # one letter, < or >, however many digits,
    # a colon (don't return), however many letters
    regex_i = '(\w)=(\d+)'  # one letter, = (don't return), however many digits
    
    def process_parser(line):
        name, steps = line.strip().split('{')
        cond_strs = steps.split(',')
        conditions = [cond_parser(*re.findall(regex_p, string)[0]) for string in cond_strs[:-1]]
        default = cond_strs[-1].strip('}')
        
        def process(item, procs):
            for attribute, comp_func, val, next_step in conditions:
                if comp_func(item[attribute], val):
                    return procs[next_step](item, procs)
            
            # if we didn't meet any of the conditions, do default
            return procs[default](item, procs)
        
        return {name:process}
    
    def item_parser(line):
        item = {key:int(val) for key,val in re.findall(regex_i, line)}
        
        return item
    
    procs = {}
    items = []
    with open( filename, 'r') as f:
        # data = [parser(*re.findall(regex, line)[0]) for line in f]
        in_procs = True
        for line in f:
            if len(line) == 1:
                in_procs = False
            elif in_procs:
                procs.update(process_parser(line))
            else:
                items.append(item_parser(line))
    
    # accepts and rejects return themselves
    procs.update({'A':lambda *x: 'A', 
                  'R':lambda *x: 'R'})
    
    return procs, items



def solve(data):
    return part1(data), part2(data)



def part1(data):
    procs, items = data
    
    outputs = [''] * len(items)
    sums = [0] * len(items)
    for idx,it in enumerate(items):
        outputs[idx] = procs['in'](it, procs)
        
        if outputs[idx] == 'A':
            sums[idx] = sum(it.values())
    
    return sum(sums)



def part2(data):
    return
            


puzzles = [['test_case.txt',    [19_114, None]],
            ['puzzle_input.txt', []]]

for filename, answers in puzzles:
    data = read_file(filename)
    results = solve(data)
    print(f"\n\n{filename}")
    if 'test' in filename:
        [check(res, ans) for res, ans in zip(results, answers) if ans is not None]
    else:
        print(f"\t{results}")