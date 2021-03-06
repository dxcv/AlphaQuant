__author__ = 'wangjp'

import numpy as np
import pandas as pd
from DataReaderModule.Constants import ALIAS_FIELDS

class Calculator:
    """
        基础计算函数 ：
        1 所有输入数据为 以股票代码、日期 为multiindex 的 pd.DataFrame
        2 返回值应为 形状完全相同的 以股票代码、日期 为multiindex 的 pd.DataFrame
        3.对于数据中的缺失值，基本的处理思想是尽量保持原有数据提供的信息，如 计算五日均值
          数据有缺失 [1,2,nan,nan,3] 则使用其中有的三天数据进行计算
    """


    def __init__(self):
        pass

    @staticmethod
    def _transData(x, retDf=False):
        if retDf:
            return x.to_frame() if isinstance(x, pd.Series) else x
        else:
            return x[x.columns[0]] if isinstance(x,pd.DataFrame) else x

    @classmethod
    def cmpMin(cls, x, y, retDf=False):
        idx = x.le(other=y)
        minVal = x * idx + y * (~idx)
        return Calculator._transData(x=minVal, retDf=retDf)

    @classmethod
    def cmpMax(cls, x, y, retDf=False):
        idx = x.ge(other=y)
        maxVal = x * idx + y * (~idx)
        return Calculator._transData(x=maxVal, retDf=retDf)

    @classmethod
    def Delay(cls, x, num, by=ALIAS_FIELDS.STKCD, fillNan=None, retDf=False):
        x = Calculator._transData(x=x, retDf=retDf)
        ret = x.groupby(level=[by],sort=False,as_index=~retDf,group_keys=False).shift(periods=num)
        if fillNan is not None:
            ret[ret.isnull()] = fillNan
        return ret

    @classmethod
    def Diff(cls, x, num, by=ALIAS_FIELDS.STKCD, fillNan=None, retDf=False):
        x = Calculator._transData(x=x, retDf=retDf)
        ret = x - Calculator.Delay(x=x, num=num, by=by, fillNan=fillNan, retDf=retDf)
        return ret


    @classmethod
    def Max(cls, x, num, by=ALIAS_FIELDS.STKCD, minobs=0, retDf=False):
        x = Calculator._transData(x=x, retDf=retDf)
        ret = x.groupby(level=[by],sort=False,as_index=~retDf,group_keys=False).rolling(window=num, min_periods=minobs).max()
        return ret


    @classmethod
    def Min(cls, x, num, by=ALIAS_FIELDS.STKCD, minobs=0, retDf=False):
        x = Calculator._transData(x=x, retDf=retDf)
        ret = x.groupby(level=[by],sort=False,as_index=~retDf,group_keys=False).rolling(window=num, min_periods=minobs).min()
        return ret

    @classmethod
    def Countif(cls, condition, num, by=ALIAS_FIELDS.STKCD, minobs=0, retDf=False):
        condition = Calculator._transData(x=condition, retDf=retDf)
        condition[condition.isnull()] = 0
        ret = Calculator.Sum(x=condition, num=num, by=by, minobs=minobs, retDf=retDf)
        return ret

    @classmethod
    def Sumif(cls, x, condition, num, by=ALIAS_FIELDS.STKCD, minobs=0, retDf=False):
        x = Calculator._transData(x=x, retDf=retDf)
        condition = Calculator._transData(x=condition, retDf=retDf)
        if retDf:
            condition.columns = x.columns
        ret = (x*condition).groupby(level=[by],sort=False,as_index=~retDf,group_keys=False).rolling(window=num, min_periods=minobs).sum()
        return ret

    @classmethod
    def Mean(cls, x, num, by=ALIAS_FIELDS.STKCD, minobs=0, retDf=False):
        """
        窗口期内的 NaN 数量满足 minNum 将被忽略
        :param x:
        :param num:
        :param by:
        :return:
        """
        x = Calculator._transData(x=x, retDf=retDf)
        ret = x.groupby(level=[by],sort=False,as_index=~retDf,group_keys=False).rolling(window=num, min_periods=minobs).mean()
        return ret

    @classmethod
    def Sum(cls, x, num, by=ALIAS_FIELDS.STKCD, minobs=0, retDf=False):
        avg = Calculator.Mean(x=x, num=num, by=by, minobs=minobs, retDf=retDf)
        ret = avg*num
        return ret

    @classmethod
    def Var(cls, x, num, by=ALIAS_FIELDS.STKCD, ddof=1, minobs=0, retDf=False):
        x = Calculator._transData(x=x, retDf=retDf)
        ret = x.groupby(level=[by],sort=False,as_index=~retDf,group_keys=False).rolling(window=num, min_periods=minobs).var(ddof=ddof)
        return ret

    @classmethod
    def Std(cls, x, num, by=ALIAS_FIELDS.STKCD, ddof=1, minobs=0, retDf=False):
        x = Calculator._transData(x=x, retDf=retDf)
        ret = x.groupby(level=[by],sort=False,as_index=~retDf,group_keys=False).rolling(window=num, min_periods=minobs).std(ddof=ddof)
        return ret

    @classmethod
    def Sma(cls, x, n, m, by=ALIAS_FIELDS.STKCD, retDf=False):
        # Xt = At*m/n + Xt-1*(n-m)/n  ie . alpha = m/n com = n/m - 1
        assert n>m
        def ewm(val):
            return val.ewm(com=com).mean()
        com = n/m - 1
        x = Calculator._transData(x=x, retDf=retDf)
        ret = x.groupby(level=[by],sort=False,as_index=~retDf,group_keys=False).apply(ewm)
        return ret

    @classmethod
    def Wma(cls, x, num, pct=0.9, by=ALIAS_FIELDS.STKCD, retDf=False):
        # 计算A前 n期样本加权平均值权重为 0.9i， (i 表示样本距离当前时点的间隔)
        # if all nan, then 0/0 makes nan
        x = Calculator._transData(x=x, retDf=retDf)
        cpx = x.copy(deep=True)
        isNa = x.isnull()
        noNa = ~isNa
        cpx[isNa] = 0
        adjfct = 0
        ret = 0
        totWeight = (1 - pct**num)/(1-pct)
        for dumi in range(num):
            weight = pct**dumi
            ret += weight*Calculator.Delay(x=cpx, num=dumi, by=by, fillNan=0, retDf=retDf)
            adjfct += weight*Calculator.Delay(x=noNa, num=dumi, by=by, fillNan=0, retDf=retDf)
        ret = totWeight/adjfct*ret
        return ret

    @classmethod
    def Decaylinear(cls, x, d, by=ALIAS_FIELDS.STKCD, retDf=False):
        # 对 A 序列计算移动平均加权，其中权重对应 d,d-1,…,1/ sum(1-d)（权重和为 1）
        # if all nan, then 0/0 makes nan
        x = Calculator._transData(x=x, retDf=retDf)
        cpx = x.copy(deep=True)
        isNa = x.isnull()
        noNa = ~isNa
        cpx[isNa] = 0
        adjfct = 0
        ret = 0
        for dumi in range(d, 0, -1):
            ret += dumi*Calculator.Delay(x=cpx, num=d-dumi, by=by, fillNan=0, retDf=retDf)
            adjfct += dumi*Calculator.Delay(x=noNa, num=d-dumi, by=by, fillNan=0, retDf=retDf)
        ret = ret/adjfct
        return ret

    @classmethod
    def TsToMin(cls, x, num, by=ALIAS_FIELDS.STKCD, minobs=0, retDf=False):
        # NaN 处理：
        # 若前窗口期包含NaN 则NaN 会占有一天的位置 ex [1, nan, 3] 在3位置对应的TsToMin(num=3) 为 3 即1 对应的位置，而不是2
        def findMin(val):
            pos = np.nanargmin(val)
            return val.shape[0] - pos
        x = Calculator._transData(x=x, retDf=retDf)
        ret = x.groupby(level=[by],sort=False,as_index=~retDf,group_keys=False).rolling(window=num, min_periods=minobs).apply(findMin, raw=True)
        return ret

    @classmethod
    def TsToMax(cls, x, num, by=ALIAS_FIELDS.STKCD, minobs=0, retDf=False):
        def findMax(val):
            pos = np.nanargmax(val)
            return val.shape[0] - pos
        x = Calculator._transData(x=x, retDf=retDf)
        ret = x.groupby(level=[by],sort=False,as_index=~retDf,group_keys=False).rolling(window=num, min_periods=minobs).apply(findMax, raw=True)
        return ret

    @classmethod
    def Rank(cls, x, by=ALIAS_FIELDS.DATE, retDf=False):
        # 注 不应再时间序列排序中使用该函数，应用于截面排序
        # method : {‘average’, ‘min’, ‘max’, ‘first’, ‘dense’}
        # na_option : {‘keep’, ‘top’, ‘bottom’}
        x = Calculator._transData(x=x, retDf=retDf)
        ret = x.groupby(level=[by],sort=False,as_index=~retDf,group_keys=False).rank(method='average', na_option='bottom', pct=False, ascending=True)
        return ret

    @classmethod
    def TsRank(cls, x, by=ALIAS_FIELDS.STKCD, retDf=False):
        # 用于时间序列排序， i.e 当前排名为 在所有过去数值中的 排名
        pass

    @classmethod
    def FindRank(cls, x, num, by=ALIAS_FIELDS.STKCD, minobs=0, retDf=False):
        # x 的末位值在过去 n 天的顺序排位 最小值排名为1
        # nan 值将被 忽略 ex [1,nan ,3] 的FindRank 值为 2
        def findLess(val):
            return sum(val<=val[-1])
        x = Calculator._transData(x=x, retDf=retDf)
        ret = x.groupby(level=[by],sort=False,as_index=~retDf,group_keys=False).rolling(window=num, min_periods=minobs).apply(findLess, raw=True)
        return ret

    @classmethod
    def Corr(cls, x, y, num, by=ALIAS_FIELDS.STKCD, minobs=2, retDf=False):
        x = Calculator._transData(x=x, retDf=retDf)
        y = Calculator._transData(x=y, retDf=retDf)
        nanPos = x.isnull().values + y.isnull().values  # x 和 y 需要全部有值才有意义
        cpX = x.copy(deep=True)
        cpY = y.copy(deep=True)
        cpX[nanPos] = np.nan
        cpY[nanPos] = np.nan
        cpX.columns = ['corr']
        cpY.columns = ['corr']
        ret = (Calculator.Mean(cpX*cpY,num,by,minobs,retDf) - Calculator.Mean(cpX,num,by,minobs,retDf)*Calculator.Mean(cpY,num,by,minobs,retDf)) / \
              (Calculator.Std(cpX, num, by, ddof=0, minobs=minobs,retDf=retDf)*Calculator.Std(cpY, num, by, ddof=0, minobs=minobs,retDf=retDf))
        return ret

    @classmethod
    def AlphaBetaSigma(cls, x, y, num, by=ALIAS_FIELDS.STKCD, calcAlpha=False, calcSigma=False, minobs=2, retDf=False):
        x = Calculator._transData(x=x, retDf=retDf)
        y = Calculator._transData(x=y, retDf=retDf)
        nanPos = x.isnull().values + y.isnull().values  # x 和 y 需要全部有值才有意义
        cpX = x.copy(deep=True)
        cpY = y.copy(deep=True)
        cpX[nanPos] = np.nan
        cpY[nanPos] = np.nan
        cpX.columns = ['val']
        cpY.columns = ['val']
        beta = (Calculator.Mean(cpX*cpY, num, by, minobs,retDf) - Calculator.Mean(cpX,num,by,minobs,retDf)*Calculator.Mean(cpY,num,by,minobs,retDf)) / \
               Calculator.Var(cpX, num, by, ddof=0, minobs=minobs,retDf=retDf)
        if calcAlpha or calcSigma:  # 需要计算 alpha
            meanX = Calculator.Mean(x=cpX, num=num, by=by, minobs=minobs, retDf=retDf)
            meanY = Calculator.Mean(x=cpY, num=num, by=by, minobs=minobs, retDf=retDf)
            alpha = meanY - meanX * beta
            if calcSigma:   # 需要 计算残差平方和/ valid data num
                ssX = Calculator.Mean(x=cpX ** 2, num=num, by=by, minobs=minobs, retDf=retDf)
                ssY = Calculator.Mean(x=cpY ** 2, num=num, by=by, minobs=minobs, retDf=retDf)
                sXY = Calculator.Mean(x=cpX*cpY, num=num, by=by, minobs=minobs, retDf=retDf)
                sigma = ssY + ssX*beta**2 + alpha**2 - 2*beta*sXY - 2*alpha*meanY + 2*alpha*beta*meanX
                if retDf:
                    beta.columns = ['beta']
                    alpha.columns = ['alpha']
                    sigma.columns = ['sigma']
                return alpha, beta, sigma
            else:
                if retDf:
                    beta.columns = ['beta']
                    alpha.columns = ['alpha']
                return alpha,beta
        else:
            if retDf:
                beta.columns = ['beta']
            return beta

    @classmethod
    def RegBeta(cls,x, y, num, by=ALIAS_FIELDS.STKCD, retDf=False):
        ret = Calculator.AlphaBetaSigma(x=x, y=y, num=num, by=by, retDf=retDf)
        return ret

    @classmethod
    def RegAlpha(cls,x, y, num, by=ALIAS_FIELDS.STKCD, retDf=False):
        alpha, beta = Calculator.AlphaBetaSigma(x=x, y=y, num=num, by=by, calcAlpha=True, retDf=retDf)
        return alpha

    @classmethod
    def RegResi(cls,x, y, num, by=ALIAS_FIELDS.STKCD, retDf=False):
        alpha, beta, sigma = Calculator.AlphaBetaSigma(x=x, y=y, num=num, by=by, calcAlpha=True, calcSigma=True, retDf=retDf)
        return sigma





if __name__=='__main__':
    t= Calculator()

    num = 4
    a = range(num)
    b = range(num)

    idx = pd.MultiIndex.from_product([a,b], names=['a', 'b'])

    # rawdata = np.random.rand(12,2)
    rawdata = np.transpose(np.array([range(num*num)])).astype(np.float32)
    rawdata[2:3,:] = np.nan

    data = pd.DataFrame(rawdata,columns=['c1'],index=idx)

    print(data)

    print(t.FindRank(x=data,num=3,by='a'))
    # print(t.TsToMax(x=data, num=3, by='a'))
