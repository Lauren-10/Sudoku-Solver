import csv
import numpy as np
with open("training_data/train_sudoku1.csv", 'r') as f:
    zero_counts = np.zeros(81)
    for line in csv.reader(f):
        zero_counts[line[0].count('0')] += 1

for i in range(len(zero_counts)):
    if zero_counts[i] != 0:
        print(i, zero_counts[i])

print(zero_counts[44] + zero_counts[45] +zero_counts[46] + zero_counts[47])
print(zero_counts[48] + zero_counts[49] +zero_counts[50] + zero_counts[51] + zero_counts[52])
