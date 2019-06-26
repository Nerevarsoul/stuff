"""
0,1,2,3,4,5,6,7,8,9,10,22,11,20..There is nothing special between numbers 0 and 10.
For all other numbers, the next element in the series is the lowest number that doesn't contain
any digits of the previous one, and is not already in the series.

You will be given an index number and your task will be return the element at that position.
"""
import time


def get_element(index: int) -> int:
    seq = []
    missed = set()
    for _ in range(index):
        if not seq:
            seq.append(0)
            continue

        if missed:
            i = min(missed)
        else:
            i = 1
        while True:
            if i not in seq and not any([sym in str(seq[-1]) for sym in str(i)]):
                seq.append(i)
                if i in missed:
                    missed.remove(i)
                # print(seq)
                break
            else:
                if i not in seq:
                    missed.add(i)
                i += 1
    return seq[-1]


if __name__ == '__main__':
    start = time.time()
    print(get_element(2000))
    print(time.time() - start)
