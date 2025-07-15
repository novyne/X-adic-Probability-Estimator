import argparse
import cProfile
import sys

from collections import deque

from typing import Iterator

####################################################################################################
# Globals and arguments
####################################################################################################

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--base", default=2, type=int, help="Number of possbilities from the sample")
parser.add_argument("-ms", "--maxsamples", default=5, type=int, help="Maximum number of samples required to be drawn")
args = parser.parse_args()

sys.setrecursionlimit(int(1e9))

P = eval(input("Probability to estimate >>\t"))

if P < 0 or P > 1:
    raise ValueError(f"Probability {P} must be between 0 and 1")

####################################################################################################
# Functions
####################################################################################################

# Precompute base powers for optimization
base_powers = [args.base ** i for i in range(args.maxsamples + 1)]

def binprob(branch: list[int]) -> float:
    p = 0
    base = args.base
    for b in branch:
        p = p * base + b
    return p / base_powers[len(branch)]

def valid_branches(valid: list[int] = []) -> Iterator[list[int]]:
    queue = deque()
    queue.append(valid)

    while queue:
        current = queue.popleft()
        depth = len(current)
        if depth == args.maxsamples:
            continue

        # Calculate binprob once for pruning
        prune_prob = binprob(current + [args.base - 1])

        for i in range(args.base):
            new_valid = current + [i]

            # Prune if any remaining samples do not surpass the required probability 
            # (known by changing the last sample to its maximum value)
            if i != args.base - 1 and prune_prob < 1 - P:
                continue
            
            if binprob(new_valid) >= 1 - P:
                yield new_valid
            else:
                queue.append(new_valid)

def real_probability() -> float:
    return ((args.base ** args.maxsamples) // (1 / P)) / (args.base ** args.maxsamples)

####################################################################################################
# Main
####################################################################################################

def main() -> None:

    valid = valid_branches()
    print("Any combination of sample results below is successful:")
    print(*sorted(valid, reverse=True), sep=", ")

    rP = real_probability()
    print(f"The exact probability being estimated is {rP}, with a {(P - rP) / P * 100:.2f}% margin of error.\nIncrease the number of samples to increase the accuracy.")

if __name__ == "__main__":
    main()
    # cProfile.run("print(len(list(valid_branches())))", sort="cumulative")