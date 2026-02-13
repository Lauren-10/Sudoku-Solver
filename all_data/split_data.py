import csv
#Split testing and training data
with open('test_sudoku.csv', 'w', newline='') as test_file:
    with open('train_sudoku.csv', 'w', newline='') as train_file:
        with open('sudoku.csv', 'r') as data_file:
            test = csv.writer(test_file)
            train = csv.writer(train_file)
            count = 0 
            for line in csv.reader(data_file):
                if count < 800000:
                    train.writerow(line)
                    count += 1
                else:
                    test.writerow(line)

#Split training data into two files so github is happy
with open("train_sudoku.csv", "r") as infile:
    with open("train_sudoku1.csv", "w", newline='') as f1:
        with open("train_sudoku2.csv", "w", newline='') as f2:
            t1 = csv.writer(f1)
            t2 = csv.writer(f2)
            count = 0
            for line in csv.reader(infile):
                if count < 400000:
                    t1.writerow(line)
                    count += 1
                else:
                    t2.writerow(line)