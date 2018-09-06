def recursive_val_iter(isBadSide, accl, depth):
    num_states = len(isBadSide)
    expected_return = 0
    for state in range(num_states):
        if isBadSide[state] == 1:
            expected_return -= accl
        else:
            expected_return += state+1
    if expected_return < 0:
        return 0
    else:
        if depth >= 5:
            return (expected_return/num_states)
        expected_return = 0
        for state in range(num_states):
            if isBadSide[state] == 1:
                expected_return -= accl
            else:
                if accl == 0:
                    print(state)
                expected_return += state+1+recursive_val_iter(isBadSide,accl+state+1, depth+1)
        return (expected_return/num_states)


def main():
    isBadSide =  [0,0,0,0,0,0,1,0,1,0,0,1,0,1,0,0]
    print(recursive_val_iter(isBadSide,0,0))

if __name__ == '__main__':
    main()