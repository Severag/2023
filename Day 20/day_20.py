import collections, math, re
import numpy as np
from functools import cache

def check(myanswer, answer):
    if not np.array_equal(myanswer, answer):
        print(f"\n\t{'ERROR':{'*'}^50}\n"
              f"\tCorrect answer: \t{answer}\n"
              f"\tReturned answer:\t{myanswer}")
    else:
        print(f"\tCheck passed!   \t{myanswer}")



def read_file(filename):
    nodes_dict = {}
    names_set = set()
    with open( filename, 'r') as f:
        for idx,line in enumerate(f):
            names = re.findall('(\w+)', line)
            nodes_dict[names[0]] = {'type':line[0],
                                   'n_idx':idx,
                                    'ins' :[],
                                    'outs':names[1:]}
            names_set.update(names)
    
    for lost_name in (names_set - set(nodes_dict.keys())):
        nodes_dict[lost_name] = {'type':'o',
                                'n_idx':idx+1,
                                 'ins' :[],
                                 'outs':[]}
    
    for name,node in nodes_dict.items():
        for output_node in node['outs']:            
            nodes_dict[output_node]['ins'].append(node['n_idx'])
    
    return nodes_dict



def solve(data):
    return part1(data), part2(data)



def part1(data):    
    to_tuple = lambda arr: tuple(map(tuple, arr))
    
    counts = np.array([0,0], dtype=np.longlong)
    state = np.full([len(data)]*2, False, dtype=bool)
    state_tup = to_tuple(state)
    
    for idx in range(1000):
        new_counts, state = send_pulse(state_tup)
        state_tup = to_tuple(state)
        counts += new_counts
        
    return np.prod(counts)



@cache
def send_pulse(state_tup):
    # items in deque are: [receiving node name, sending node name, signal level]
    open_list = collections.deque([['broadcaster', '', False]])
    pulse_count = {True:0,  # High
                   False:1}  # Low, from starting button pulse
    # nodes read from this array from columns and write downstream in rows (&)
    # or they store their state on the diagonal (%)
    state = np.asarray(state_tup, dtype=bool)
    track = 'rt_sl_fv_gk'
    
    while open_list:
        node_name, sent_name, signal = open_list.popleft()
        this_node = data[node_name]
        node_type = this_node['type']
        idx = this_node['n_idx']
                    
        if node_type == 'b':  # broadcaster
            new_sig = signal  # just repeat the incoming signal
        elif node_type == '%':  # flip-flop
            if not signal:  # if it's a low signal
                new_sig = not(state[idx, idx])
                state[idx, idx] = new_sig
            else:  # ignore high signals
                continue
        elif node_type == '&':  # conjunction
            # update memory
            o_idx = data[sent_name]['n_idx']
            state[o_idx, idx] = signal
            # send appropriate output given new input
            new_sig = False in state[this_node['ins'], idx]
            
            if not new_sig and node_name in track:  # for Part 2
                state[idx, idx] = True
        elif node_type == 'o':  # dummy nodes like 'output' and 'rx'
            continue
        
        for next_name in this_node['outs']:
            open_list.append([next_name, node_name, new_sig])
        
            pulse_count[new_sig] += 1
    
    return np.array([pulse_count[False], pulse_count[True]]), state



def part2(data):
    '''
        a few lines in send_pulse will indicate in the state variable when
        certain conjunctions flip. this function will record at what index that 
        happens, and the least common multiple of all those frequencies is the 
        index when they all flip together and activate rx
    '''
    # ignore test cases
    if len(data) < 10:
        return None
    
    to_tuple = lambda arr: tuple(map(tuple, arr))
    
    state = np.full([len(data)]*2, False, dtype=bool)
    state_tup = to_tuple(state)
    idx = 0
    
    # indices of the gatekeeping nodes
    track = [data[string]['n_idx'] for string in 'rt_sl_fv_gk'.split('_')]
    # how many cycles it takes them to come online
    track_freq = np.zeros(len(track), dtype=int)
    trues = 0  # how many frequencies have we found
    
    while True:
        _, state = send_pulse(state_tup)
        state_tup = to_tuple(state)
        
        idx += 1
        
        # have we found another frequency
        if sum(state[track, track]) > trues:
            # which one is it?
            mask = (track_freq == 0) & state[track, track]
            track_freq[mask] = idx  # add it to the collection
            trues += 1  # set a higher back to find the next one
        
        if trues >= 4:
            return math.lcm(*track_freq)



puzzles = [['test_case.txt',    [32_000_000, None]],
           ['test_case2.txt',   [11_687_500, None]],
           ['puzzle_input.txt', []]]

for filename, answers in puzzles:
    data = read_file(filename)
    results = solve(data)
    print(f"\n\n{filename}")
    if 'test' in filename:
        [check(res, ans) for res, ans in zip(results, answers) if ans is not None]
    else:
        print(f"\t{results}")