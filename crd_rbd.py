import numpy as np
import pandas as pd


class CrdRbd:
    def __init__(self, data):
        self.SST = None,
        self.MSST = None,
        self.SSt = None
        self.MSSt = None
        self.MSSE = None
        self.MSSe = None
        self.n = None
        self.N = None
        self.k = None
        self.b = None
        self.data = data
        print("""    
            T SQR = TOTAL SQUARED,
            T MEAN = TOTAL MEAN
            G = GRAND TOTAL
            """)

    def data_manipulation(self, in_data, prob):
        if prob == 'crd':
            rep = 'T'
        else:
            rep = 'B'
        sum_of_Yi = pd.DataFrame(np.sum(in_data).T, columns=[rep])
        mean_of_Yi = pd.DataFrame(np.mean(in_data).T, columns=['mean'])
        sqr_of_Yi = pd.DataFrame(np.square(np.sum(in_data)).T, columns=['{}^2'.format(rep)])
        t_sqr_of_Yi = np.sum(np.square(np.sum(in_data)))
        total = np.sum(np.sum(in_data))
        total_mean = total / in_data.size
        total_squared = np.sum(np.sum(np.square(in_data)))
        total_sqr = total ** 2
        print("N :  {}".format(in_data.size))
        print("G :  {}".format(total))
        print("G^2 : {}".format(total_sqr))
        print("T SQR : {}".format(total_squared))
        print("T MEAN : {}".format(total_mean))

        new_table = sum_of_Yi.join(mean_of_Yi).join(sqr_of_Yi)
        print("\n")
        print(new_table.T)
        val = {
            'G': total,
            'N': in_data.size,
            'total_squared': total_squared,
            'sqr_of_Yi': sqr_of_Yi,
            't_sqr_of_Yi': t_sqr_of_Yi,
            'G^2': total_sqr,

        }
        return val

    def anova(self, test, sse, sst_, df):
        if len(test) == 1:
            SSt = test[0]
            t_D_F = df[0]
            E_D_F = df[1]
            T_D_F = df[2]
        elif len(test) == 2:
            SSt = test[0]
            SSb = test[1]
            t_D_F = df[0]
            b_D_F = df[1]
            E_D_F = df[2]
            T_D_F = df[3]
        pre_table = [[SSt,
                      t_D_F,
                      SSt / t_D_F,
                      (SSt / t_D_F) / (sse / E_D_F),
                      ],
                     [sst_,
                      T_D_F,
                      sst_ / T_D_F,
                      '-'
                      ]
                     ]
        if len(test) == 1:
            pre_table.insert(1, [sse,
                                 E_D_F,
                                 sse / E_D_F,
                                 '-'
                                 ])
        if len(test) > 1:
            index = ['treatment', 'block', 'error', 'total']
        else:
            index = ['treatment', 'error', 'total']
        if len(test) > 1:
            pre_table.insert(1, [SSb,
                                 b_D_F,
                                 SSb / b_D_F,

                                 (SSb / b_D_F) / (sse / E_D_F),
                                 ])
            pre_table.insert(2, [sse,
                                 E_D_F,
                                 sse / E_D_F,
                                 '-'
                                 ])
        table = pd.DataFrame(np.array(
            pre_table
        ), index=index, columns=['SS', 'DF', 'MSS', 'Variance ration (F)'])
        print("\n")
        print(table)

    def crd(self):
        print("----treatments-----")
        print("k : {} ".format(self.data.shape[0]))
        n = self.data.shape[1]
        var = self.data.T
        calc = self.data_manipulation(var, 'crd')
        SST = calc['total_squared'] - calc['G^2'] / calc['N']
        T_D_F = calc['N'] - 1
        sum_ys = np.sum(calc['t_sqr_of_Yi'])
        SSt = sum_ys / n - calc['G^2'] / calc['N']
        t_D_F = self.data.shape[0] - 1
        SSe = calc['total_squared'] - sum_ys / n
        E_D_F = self.data.shape[0] * (n - 1)
        print("\n")
        print('--- ANOVA TABLE ---')
        self.anova([SSt], SSe, SST, [t_D_F, E_D_F, T_D_F])

    def rbd(self):
        print("\n-----with blocks------")
        print("b : {} ".format(self.data.shape[1]))
        b = self.data.shape[1]
        k = self.data.shape[0]
        var = self.data.T
        calc = self.data_manipulation(var, 'crd')
        sum_ys = np.sum(calc['t_sqr_of_Yi'])
        SSt = sum_ys / b - calc['G^2'] / (b * k)
        t_D_F = k - 1
        calc = self.data_manipulation(self.data, 'rbd')
        SST = calc['total_squared'] - calc['G^2'] / (b * k)
        T_D_F = b * k - 1
        sum_ys = np.sum(calc['t_sqr_of_Yi'])
        SSb = sum_ys / k - calc['G^2'] / (b * k)
        b_D_F = b - 1
        SSe = SST - (SSt + SSb)
        E_D_F = (b - 1) * (k - 1)
        print("\n")
        print('--- ANOVA TABLE ---')
        self.anova([SSt, SSb], SSe, SST, [t_D_F, b_D_F, E_D_F, T_D_F])

