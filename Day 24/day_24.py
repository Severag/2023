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
    regex = '-?\d+'  # negative sign, if it's there, and any length number
    converter = lambda X: [int(val) for val in re.findall(regex, X)]
    parser = lambda X: [converter(part) for part in X]
    with open( filename, 'r') as f:
        data = [parser(line.split('@')) for line in f]
    
    return np.array(data, dtype=np.longlong)



def solve(data):
    return part1(data), part2(data)



def part1(data):
    # x,y bounding box values
    low,high = (7, 27) if len(data) < 10 else (2e14, 4e14)
    
    mb_form = [get_m_b(p, v) for p,v in data]
    count = 0
    tracker = []
    
    for idx1, idx2 in list(itertools.combinations(range(len(data)), 2)):
        line1, line2 = mb_form[idx1], mb_form[idx2]
        x,y = get_intersection(*line1, *line2)
        time = min(get_time(x, *data[idx1]), get_time(x, *data[idx2]))
        
        # intersection is in the future and we're in the region we care about
        if (time >= 0 and low <= x <= high and low <= y <= high):
             count += 1
             tracker.append([x, y, time])
        else:
             tracker.append(None)
    
    return count



def get_m_b(p, v):
    m = v[1] / v[0]
    b = -m * p[0] + p[1]  # from point-slope form of f(x) = mx + b
    return m,b



def get_intersection(m1, b1, m2, b2):
    # find where  y1 = y2
    # aka m1*x1 + b1 = m2*x2 + b2, solve for x 
    x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1
    return x,y



def get_time(x, p, v):
    return (x - p[0]) / v[0]



def part2(data):
    # --0-- #
    # switch to a hail #0-centric reference frame
    new_ref = data - data[0]  
    # hail #0 is now stationary at the origin
    
    # --1-- #
    # find plane containing the origin and hail #1's line
    normal = np.cross(new_ref[1,0], new_ref[1,1])
    normal = normal / np.sqrt(np.dot(normal, normal * 1.0))  # make it a unit vector
    # if hail #1 is defined by p0 + v*t, then the above is a short form of
    # cross(p0 - origin, p1 - p0) where p1 is p0 + v*1
    # rock's trajectory has to be in this plane
    
    # --2-- #
    # find when & where hail #2 intersects this plane
    p0, v = new_ref[2]
    time2 = - np.dot(normal, p0) / np.dot(normal, v)
    # at <time2>, (p0 + v*time2) * normal is 0, solve for time2
    point2 = p0 + v * time2
    
    # --3-- #
    # find when & where hail #3 intersects this plane
    p0, v = new_ref[3]
    time3 = - np.dot(normal, p0) / np.dot(normal, v)
    # at <time3>, (p0 + v*time3) * normal is 0, solve for time3
    point3 = p0 + v * time3
    
    # --4-- #
    # get rock's line
    v_rock = (point2 - point3) / (time2 - time3)
    # distance traveled from hail #2 to hail #3, divived by the time it took
    p_rock = point2 - time2 * v_rock
    # point where rock hits hail #2 minus the distance it covered to get there
    p_rock_true = p_rock + data[0, 0]  # convet back into stationary reference frame
    
    return int(p_rock_true.round().sum())



puzzles = [['test_case.txt',    [2, 47]],
           ['puzzle_input.txt', []]]

for filename, answers in puzzles:
    data = read_file(filename)
    results = solve(data)
    print(f"\n\n{filename}")
    if 'test' in filename:
        [check(res, ans) for res, ans in zip(results, answers) if ans is not None]
    else:
        print(f"\t{results}")