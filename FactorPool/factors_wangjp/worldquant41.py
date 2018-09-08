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
        self.needFields = [t.HIGH, t.LOW, t.CLOSE, t.AMOUNT, t.VOLUME, t.TRDSTAT]  # ������Ҫ���ֶ�


    def factor_definition(self):
        s = time.time()
        needData = self.needData                                # ������������
        needData.loc[needData[t.TRDSTAT].isin([5,6]), t.VOLUME] = np.nan        # ��ͣ�ƶ�Ӧ ��Ʊ������ ��Ϊ NaN
        vwap = needData[t.AMOUNT]/needData[t.VOLUME]
        hml = (needData[t.HIGH]+needData[t.LOW]+needData[t.CLOSE])/3
        factor = -hml/vwap
        factor = factor.to_frame()
        factor.columns = [self.factorName]                          # ���Ӽ�����Ӧ��ֻ��һ�У� ����˴����� �������Ӷ���
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()



fct = Factor()
fct.run_factor()