import pandas as pd
import crd_rbd

data_ = [
    [20, 16, 26, 26, 34, 28, 20, 18],
    [26, 22, 26, 24, 38, 30, 24, 29],
    [32, 28, 32, 24, 36, 48, 36, 24],
    [48, 42, 34, 36, 42, 54, 50, 45],
]

data_ = pd.DataFrame(data_, columns=['0', '1', '2', '3',
                                     '4', '5', '6', '7'],
                     index=['a', 'b', 'c', 'd'])

m = crd_rbd.CrdRbd(data_)
m.crd()
