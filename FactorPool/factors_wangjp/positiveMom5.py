__author__ = 'wangjp'

import time

import numpy as np
import pandas as pd
from FactorModule.FactorBase import FactorBase
from CalculatorModule.Calculator import Calculator
from DataReaderModule.Constants import ALIAS_FIELDS as t

class Factor(FactorBase):

    def __init__(self):
        super(Factor,self).__init__(basePath=r'D:\AlphaQuant\FactorModule')
        self.factorName = __name__.split('.')[-1]
        self.needFields = [t.PCTCHG, t.TRDSTAT]  # ������Ҫ���ֶ�
        # put remote conn here if need extra data

    def factor_definition(self):
        s = time.time()
        needData = self.needData                                # ������������
        needData.loc[needData[t.TRDSTAT].isin([5,6]), t.PCTCHG] = np.nan        # ��ͣ�ƶ�Ӧ ��Ʊ������ ��Ϊ NaN
        factor = Calculator.Sumif(x=needData[t.PCTCHG], condition=needData[t.PCTCHG]>0 ,num=5)        # ����5�ն���
        factor.columns = [self.factorName]
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()



fct = Factor()
fct.run_factor()