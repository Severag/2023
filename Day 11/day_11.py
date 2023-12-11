import itertools
import numpy as np

def check(myanswer, answer):
    if not np.array_equal(myanswer, answer):
        print(f"\n\t{'ERROR':{'*'}^50}\n"
              f"\tCorrect answer: \t{answer}\n"
              f"\tReturned answer:\t{myanswer}")
    else:
        print(f"\tCheck passed!   \t{myanswer}")



def read_file(filename):
    parse = lambda x: np.array([1 if val == '.' else 0 for val in x])
    
    with open( filename, 'r') as f:
        star_map = np.array([parse(line.strip()) for line in f], dtype=np.longlong)
    
    total = len(star_map)  # find rows where there aren't stars to lower the sum
    r_mask = np.where(np.sum(star_map, axis=1) == total)  
    
    total = len(star_map[0])  # find columns where there aren't stars 
    c_mask = np.where(np.sum(star_map, axis=0) == total)
    
    star_map[r_mask] = -1  # set the value of rows without stars to -1. their 
    star_map[:, c_mask] = -1  # actual distances with expansion will be added later
    
    stars = list(zip(*np.where(star_map == 0)))  # record where the stars are
    star_map[star_map == 0] = 1  # stars are regular space, without expansion
    
    return star_map, stars



def solve(data):
    
    answer1 = part1(data)
    answer2 = part2(data)
    
    return [answer1] + answer2



def part1(data, empty=2):
    star_map, stars = data
    exp_joints = star_map < 0  # where the expansion joints are
    star_map[exp_joints] = empty
    # star map can now be used to calculate the actual distance between two points
    
    def mod_manhat_dist(s1, s2):  # sum along the route from star1 to star2
        # the expansion lines will have higher values representing the extra space
        # stay in star2's row but slide over to star1's column
        move_out = [s2[0], s2[1], s1[1], True]
        # stay in star1's column but move up from star2's row to star1's row
        move_up = [s1[1], s2[0], s1[0], False]
        
        total = 0
        for const, start, end, dont_flip in [move_up, move_out]:
            delta = 1 if end > start else -1
            total += star_map[const, start:end:delta].sum() if dont_flip else star_map[start:end:delta, const].sum()
        
        return total
    
    dists = [mod_manhat_dist(star_a, star_b) for star_a, star_b in itertools.combinations(stars, 2)]
    
    star_map[exp_joints] = -1  # reset to prior state
    
    return sum(dists)



def part2(data):
    return [part1(data, expansion) for expansion in [10, 100, 1_000_000]]



puzzles = [['test_case.txt',    [374,  1030, 8410, None]],
           ['puzzle_input.txt', []]]

for filename, answers in puzzles:
    data = read_file(filename)
    results = solve(data)
    print(f"\n\n{filename}")
    if 'test' in filename:
        [check(res, ans) for res, ans in zip(results, answers) if ans is not None]
    else:
        print(f"\t{results}")