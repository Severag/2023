import heapq
import numpy as np
from collections import Counter

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
    parser = lambda x,y: (x,int(y))
    with open( filename, 'r') as f:
        data = [parser(*line.split(' ')) for line in f]
        
    return data



def solve(data, is_part1=True):
    hands_ranked = []
    
    # convert letters into appropriate numbers to make it easier to sort
    card_num = {str(idx):idx for idx in range(2, 10)}
    card_num.update({val:idx for val,idx in zip('TJQKA', range(10,15))})
    
    if not is_part1:  # downgrad J's rank for Part 2
        card_num['J'] = 1
    
    for hand,wager in data:
        h_type = get_type(hand, is_part1)
        h_list = tuple(card_num[char] for char in hand)
        # the heap will sort by type then by rank of cards in left-to-right order
        heapq.heappush(hands_ranked, (h_type, h_list, wager))
    
    total = 0
    for rank in range(1, len(hands_ranked) + 1):
        _, _, wager = heapq.heappop(hands_ranked)
        total += wager * rank
    
    return total



def get_type(hand, is_part1=True):
    counts = Counter(hand)
    
    # turn 'J's into the most common card value
    if not is_part1 and 'J' in hand:
        for card,count in counts.most_common(2):
            if card != 'J':
                counts = Counter(hand.replace('J', card))
                break
    
    if 5 in counts.values():
        return 5  # Five of a kind
    elif 4 in counts.values():
        return 4  # Four of a kind
    elif 3 in counts.values():
        if 2 in counts.values():
            return 3.5  # Full House
        else:
            return 3  # Three of a kind
    elif 2 in counts.values():
        if Counter(counts.values())[2] > 1:
            return 2.5  # Two pair
        else:
            return 2  # One pair
    else:
        return 0



test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 6440)
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False),  5905)
print(solve(puzz_input, False))  