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
    
    return np.array(data)



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
    ps, vs = data[:, 0], data[:, 1]
    
    def error(new_line):
        p_, v_ = new_line[:3], new_line[3:]
        As = np.sum((vs - v_)**2, axis=1, keepdims=True)
        Bs = np.sum(2 * (ps - p_) * (vs - v_), axis=1, keepdims=True)
        Ts = -Bs / 2 / As
        
        return np.sum(np.abs(ps - p_ + (vs - v_) * Ts))
    
    def constraints(new_line):
        p_, v_ = new_line[:3], new_line[3:]
        As = np.sum((vs - v_)**2, axis=1, keepdims=True)
        Bs = np.sum(2 * (ps - p_) * (vs - v_), axis=1, keepdims=True)
        return np.min(-Bs / 2 / As)
    
    cons = {'type': 'ineq',
            'fun' : constraints}
    from scipy.optimize import minimize
    
    res_1 = minimize(error, [0,0,0,  2,2,2], constraints=cons)
    
    return np.sum(np.round(res_1.x[:3]))



def closest_approach(line1, line2):
    p1,v1 = line1
    p2,v2 = line2
    
    A = np.dot(v1 - v2, v1 - v2)
    B = 2 * np.dot(p1 - p2, v1 - v2)
    
    return - B / 2 / A



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