import csv
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