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
        data = [line.strip().split(',') for line in f][0]
    return data



def solve(data):
    return part1(data), part2(data)



def part1(data):
    hashes = [my_hash(step) for step in data]    
   
    return sum(hashes)



def my_hash(string):
    val = 0
    for char in string:
        val += ord(char)
        val *= 17
        val %= 256
   
    return val



def part2(data):
    # dictionaries will keep entries in fifo order like a list and also allow us
    # to lookup which lenses are in a box and modify/delete them
    boxes = [dict() for _ in range(256)]
   
    # put lenses in boxes
    for step in data:
        # regex = (from 1 to however many letters)(a minus or equal sign)(from 0 to however many numbers)
        [[label, op, numstr]] = re.findall('([\w]+)([-=])([\d]*)', step)
        box_id = my_hash(label)
       
        if op == '=':
            foc_len = int(numstr)
            boxes[box_id][label] = foc_len  # update (or add) lens with new focal length
        else:  # op == '-'
            boxes[box_id].pop(label, None)  # remove lens with label if it's there
   
    # calculate focusing power
    total = 0
    for box_id, box in enumerate(boxes):
        for slot, foc_len in enumerate(box.values()):
            total += (box_id + 1) * (slot + 1) * foc_len
   
    return total



puzzles = [['test_case.txt',    [1320, 145]],
            ['puzzle_input.txt', []]]

for filename, answers in puzzles:
    data = read_file(filename)
    results = solve(data)
    print(f"\n\n{filename}")
    if 'test' in filename:
        [check(res, ans) for res, ans in zip(results, answers) if ans is not None]
    else:
        print(f"\t{results}")