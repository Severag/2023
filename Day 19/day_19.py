import math, re
import numpy as np

def check(myanswer, answer):
    if not np.array_equal(myanswer, answer):
        print(f"\n\t{'ERROR':{'*'}^50}\n"
              f"\tCorrect answer: \t{answer}\n"
              f"\tReturned answer:\t{myanswer}")
    else:
        print(f"\tCheck passed!   \t{myanswer}")



def read_file(filename):
    cond_parser = lambda x1,x2,x3,x4: [x1, x2 == '<', int(x3), x4]
    regex_p = '(\w)([<>])(\d+):(\w+)'  # one letter, < or >, however many digits,
    # a colon (don't return), however many letters
    regex_i = '(\w)=(\d+)'  # one letter, = (don't return), however many digits
    
    def process_parser(line):
        name, steps = line.strip().split('{')
        cond_strs = steps.split(',')
        conditions = [cond_parser(*re.findall(regex_p, string)[0]) for string in cond_strs[:-1]]
        default = cond_strs[-1].strip('}')
        
        return {name:[conditions, default]}
    
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
    
    starting = xmas_range()
    valid_ranges = search('in', starting, procs)
    
    return valid_ranges, items



class xmas_range():
    def __init__(self, init_values=None):
        if init_values is None:
            self.attributes = {key:range(1, 4001) for key in 'xmas'}
        else:
            self.attributes = {key:range(val[0], val[-1] + 1)
                               for key,val in init_values.items() }
    
    
    def __str__(self):
        return '\n'.join([f'{key}:{self.attributes[key]}' for key in 'xmas'])
    
    
    def __repr__(self):
        return self.__str__()
    
    
    def adjust_limit(self, key, val, is_less_than):
        span = self.attributes[key]
        if is_less_than:
            if val in span:  # make val new max value
                self.attributes[key] = range(span[0], val)
                return True
            elif val > span[-1]:  # we're already less than value
                # don't change anything
                return True
            else:  # we have to be greater than val to get here, so this isn't valid
                return False
        else:
            val += 1  # range is inclusive on the lower end, so to exclude val
            # we must start with one above it
            if val in span:  # make val new min value
                self.attributes[key] = range(val, span[-1] + 1)
                return True
            elif val < span[0]:  # we're already greater than value
                # don't change anything
                return True
            else:  # we have to be less than val to get here, so this isn't valid
                return False
    
    
    def in_limits(self, item):
        for key,val in item.items():
            if val not in self.attributes[key]:
                return False
        
        return True
    
    
    def value(self):
        return math.prod([len(val) for val in self.attributes.values()])
    
    
    def copy(self):
        return xmas_range(self.attributes)



def search(p_name, xmas, procs):
    # end conditions
    if p_name == 'A':  # accepted
        return [xmas]
    elif p_name == 'R':  # rejected
        return []
    
    conditions, default = procs[p_name]
    
    outcomes = []
    curr_xmas = xmas
    for attribute, is_less_than, val, next_step in conditions:
        # meets the condition
        meets = curr_xmas.copy()
        is_valid = meets.adjust_limit(attribute, val, is_less_than)
        if is_valid:  # we can make that change
            outcomes += search(next_step, meets, procs)
        
        # doesn't meet the condition and continues the loop
        val += -1 if is_less_than else 1  # not(>) is >= and not(<) is <=
        # so we need to move val so its original value gets included in the range
        is_valid = curr_xmas.adjust_limit(attribute, val, not is_less_than)
        if not is_valid:
            print(curr_xmas, val)
            raise ValueError
    
    outcomes += search(default, curr_xmas, procs)
    
    return outcomes



def solve(data):
    return part1(data), part2(data)



def part1(data):
    valid_ranges, items = data
    
    total = 0
    for it in items:
        for rng in valid_ranges:
            if rng.in_limits(it):  # found what range item fits into
                total += sum(it.values())
                break
        # if we get through the whole loop w/out finding a match, the part is rejected
    
    return total



def part2(data):
    valid_ranges, _ = data
    
    return sum([xmas.value() for xmas in valid_ranges])



puzzles = [['test_case.txt',    [19114, 167_409_079_868_000]],
            ['puzzle_input.txt', []]]

for filename, answers in puzzles:
    data = read_file(filename)
    results = solve(data)
    print(f"\n\n{filename}")
    if 'test' in filename:
        [check(res, ans) for res, ans in zip(results, answers) if ans is not None]
    else:
        print(f"\t{results}")