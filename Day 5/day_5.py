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
    
    groups = []
    this_group = []
    for line in data:
        if len(line) > 0:
            this_group.append([int(val) for val in line])
        elif len(this_group) > 0:
            groups.append(np.array(this_group).squeeze())
            this_group = []
    groups.append(np.array(this_group))
    
    return groups



def solve(data, is_part1=True):    
    if is_part1:
        funcs = [None]
        for group in data[1:]:
            funcs.append(create_conv_func(group, funcs[-1]))
        funcs = funcs[1:]
    
        end_states = [funcs[-1](val) for val in data[0]]    
    
        return min(end_states)
    else:
        return solve2(data)




def create_conv_func(group_arr, prior=None):
    start = group_arr[:, 1]
    end = start + group_arr[:, 2]
    new_start = group_arr[:, 0]
    
    def conv(val):
        val = val if prior is None else prior(val)
        
        [where] = np.where((start <= val) & (val < end))
        
        if len(where) > 0:  # if we found a conversion mapping
            idx = where[0]
            return val - start[idx] + new_start[idx]
        else:
            return val  # no mapping, just returns itself
    
    return conv



def solve2(data):  
    funcs = [None]
    for group in data[-1:0:-1]:
        funcs.append(create_conv_func(group[:, (1,0,2)], funcs[-1]))
    funcs = funcs[1:]
    
    loc_to_seed = funcs[-1]
    
    starts = data[0][::2]
    ends = starts + data[0][1::2]
    
    for idx in range(max(ends)):
        num = loc_to_seed(idx)
        
        if ((num >= starts) & (num < ends)).any():
            break
    
    return idx    



test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 35)
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False), 46 )
print(solve(puzz_input, False))  # 1240036 too high