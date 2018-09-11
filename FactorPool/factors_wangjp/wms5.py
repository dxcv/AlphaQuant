__author__ = 'wangjp'

import time

import numpy as np
import pandas as pd
from FactorModule.FactorBase import FactorBase
from CalculatorModule.Calculator import Calculator
from DataReaderModule.Constants import ALIAS_FIELDS as t

class Factor(FactorBase):

    def __init__(self):
        super(Factor,self).__init__()
        self.factorName = __name__.split('.')[-1]
        self.needFields = [t.HIGH, t.LOW, t.CLOSE, t.ADJFCT, t.TRDSTAT]  # ������Ҫ���ֶ�


    def factor_definition(self):
        s = time.time()
        needData = self.needData                                # ������������
        needData.loc[needData[t.TRDSTAT].isin([5,6]), t.ADJFCT] = np.nan        # ��ͣ�ƶ�Ӧ ��Ʊ������ ��Ϊ NaN

        num = 5
        rHigh = Calculator.Max(x=needData[t.HIGH]*needData[t.ADJFCT], num=num)
        rLow = Calculator.Max(x=needData[t.LOW]*needData[t.ADJFCT], num=num)
        rChg = Calculator.Sum(x = Calculator.Diff(x=needData[t.CLOSE], num=1), num=num)
        factor = -rChg/(rHigh - rLow)
        factor = factor.to_frame()
        factor.columns=[self.factorName]                         # ���Ӽ�����Ӧ��ֻ��һ�У� ����˴����� �������Ӷ���
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()



fct = Factor()
fct.run_factor()