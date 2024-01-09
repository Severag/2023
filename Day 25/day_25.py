import itertools, re
import numpy as np

def check(myanswer, answer):
    if not np.array_equal(myanswer, answer):
        print(f"\n\t{'ERROR':{'*'}^50}\n"
              f"\tCorrect answer: \t{answer}\n"
              f"\tReturned answer:\t{myanswer}")
    else:
        print(f"\tCheck passed!   \t{myanswer}")



def read_file(filename):
    regex = '\w{3}'  # three character word
    with open( filename, 'r') as f:
        data = [re.findall(regex, line) for line in f]
    
    data_dict = dict()
    for key,*vals in data:
        data_dict[key] = data_dict.get(key, []) + vals
        
        # make the reverse connection
        for it in vals:
            data_dict[it] = data_dict.get(it, []) + [key]
    
    return data_dict



def solve(data):
    return part1(data), part2(data)



def part1(data):
    import networkx as nx
    
    my_graph = nx.Graph(data)
    
    # find the nodes on either side of the critical edges
    top,bottom = set(), set()
    for n1, n2 in nx.minimum_edge_cut(my_graph):
        top.add(n1)
        bottom.add(n2)
    
    # get the size of the two subgraphs
    top_nodes = flood(data, list(top)[0], bottom)
    bottom_nodes = flood(data, list(bottom)[0], top)
    
    return len(top_nodes) * len(bottom_nodes)



def flood(data, start, avoid):    
    open_list = [start]
    closed_set = set()
    
    while open_list:
        node = open_list.pop()
        
        # already visited or forbidden
        if node in closed_set or node in avoid:
            continue
        
        closed_set.add(node)
        
        for cand in data[node]:
            if not (cand in closed_set or cand in avoid):
                open_list.append(cand)
    
    return closed_set



def part2(data):
    return



puzzles = [['test_case.txt',    [54, None]],
           ['puzzle_input.txt', []]]

for filename, answers in puzzles:
    data = read_file(filename)
    results = solve(data)
    print(f"\n\n{filename}")
    if 'test' in filename:
        [check(res, ans) for res, ans in zip(results, answers) if ans is not None]
    else:
        print(f"\t{results}")