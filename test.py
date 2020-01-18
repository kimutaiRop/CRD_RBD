import pandas as pd
import crd_rbd

# example 1
# example of data in list
data_ = [
    [20, 16, 26, 26, 34, 28, 20, 18],
    [26, 22, 26, 24, 38, 30, 24, 29],
    [32, 28, 32, 24, 36, 48, 36, 24],
    [48, 42, 34, 36, 42, 54, 50, 45],
]

# give the data unique rows and column labeling and convert to dataframe
data_ = pd.DataFrame(data_, columns=['0', '1', '2', '3',
                                     '4', '5', '6', '7'],
                     index=['a', 'b', 'c', 'd'])

# example 2
# comment the line bellow for now
data_ = pd.read_csv('path to .csv file or .txt file')  # make sure your data is well labeled

# now feed the data into the program
m = crd_rbd.CrdRbd(data_)

m.crd()  # for a crd
m.rbd()  # for rbd
