__author__ = 'wangjp'


rootPath = r'D:\AlphaQuant'

class DatabaseNames:
    MysqlDaily = 'testdb' #''stocks_data_daily'

class ALIAS_TABLES:         # �������
    TRDDATES = 'trade_dates'
    STKBASIC = 'stocks_info'
    DAILYCNT = 'daily_stocks_count'
    XFILTER = 'FEATURES_FILTER'
    YFILTER = 'RESPONSE_FILTER'
    RESPONSE = 'RESPONSE'
    TRAEDINFO = 'ASHAREEODPRICES'
    DERIVINFO = 'ASHAREEODDERIVATIVEINDICATOR'

class ALIAS_FIELDS:         # ���������ֶα��
    DATE = 'TRADE_DT'
    STKCD = 'S_INFO_WINDCODE'
    STKCNT = 'DAILY_COUNT'

    OPEN = 'S_DQ_OPEN'
    HIGH = 'S_DQ_HIGH'
    LOW = 'S_DQ_LOW'
    CLOSE = 'S_DQ_CLOSE'
    VOLUME = 'S_DQ_VOLUME'
    AMOUNT = 'S_DQ_AMOUNT'
    PCTCHG = 'S_DQ_PCTCHANGE'
    TRDSTAT = 'S_DQ_TRADESTATUS'
    ADJFCT = 'S_DQ_ADJFACTOR'
    STSTAT = 'TYPE_ST'

class ALIAS_RESPONSE:
    OC1 = 'OCDay1'
    CC1 = 'CCDay1'
    OC10 = 'OCDay10'
    OCG1 = 'OCDay1Gap1'
    CCG1 = 'CCDay1Gap1'
    OCG2 = 'OCDay1Gap2'
    CCG2 = 'CCDay1Gap2'
    OCG3 = 'OCDay1Gap3'
    CCG3 = 'CCDay1Gap3'
    OCG4 = 'OCDay1Gap4'
    CCG4 = 'CCDay1Gap4'

class ALIAS_STATUS:        # ״̬�ֶα��
    NOTRD = 'NOTRADE'
    PNOTRD = 'PRENOTRADE'
    ISST = 'ISST'
    LMUP = 'LIMITUP'
    LMDW = 'LIMITDOWN'
    INSFAMT = 'INSFAMT'
    INSFTRD = 'INSFTRADE'
    INSFLST = 'INSFLIST'
    INSFRSM = 'INSFRESUM'

class ALIAS_INDICATORS:
    BETA = 'beta'
    IC = 'IC'
    RKIC = 'rankIC'
    GPIC = 'groupIC'
    TBDF = 'tbdf'


NO_QUICK = ['ASHAREEODPRICES', 'FEATURES_FILTER', 'RESPONSE_FILTER', 'RESPONSE']

QuickTableFieldsDict = {
    'FEATURES_FILTER': ['NOTRADE', 'PRENOTRADE', 'ISST', 'LIMITUP', 'LIMITDOWN', 'INSFAMT', 'INSFTRADE', 'INSFLIST',
                        'INSFRESUM', 'FilterX'],
    'RESPONSE_FILTER': ['OCRet', 'CORet', 'CCRet', 'NOTRADE', 'ISST', 'COLIMITUP', 'COLIMITDOWN', 'CCLIMITUP',
                        'CCLIMITDOWN'],
    'RESPONSE': ['OCDay1', 'CCDay1', 'OCDay10', 'OCDay1Gap1', 'CCDay1Gap1', 'OCDay1Gap2', 'CCDay1Gap2', 'OCDay1Gap3',
                 'CCDay1Gap3', 'OCDay1Gap4', 'CCDay1Gap4'],
    'ASHAREEODPRICES': ['S_DQ_OPEN', 'S_DQ_HIGH', 'S_DQ_LOW', 'S_DQ_CLOSE', 'S_DQ_VOLUME', 'S_DQ_AMOUNT',
                        'S_DQ_PCTCHANGE', 'S_DQ_TRADESTATUS', 'S_DQ_ADJFACTOR'],
    'ASHAREST': ['TYPE_ST'],
    'ASHAREFLOATHOLDER': ['TOT_HOLDERS', 'PERS_HOLDERS', 'INST_HOLDERS', 'TOT_QUANTITY', 'PERS_QUANTITY',
                          'INST_QUANTITY'],
    'ASHARECAPITALIZATION': ['TOT_SHR', 'FLOAT_SHR', 'FLOAT_A_SHR', 'S_SHARE_TOTALA'],
    'ASHAREEODDERIVATIVEINDICATOR': [
                                     'S_VAL_MV',  # ��������ֵ
                                     'S_DQ_MV',  # ������ͨ��ֵ
                                     # 'S_PQ_HIGH_52W_',               # 52����߼�
                                     # 'S_PQ_LOW_52W_',                # 52����ͼ�
                                     'S_VAL_PE',  # ��ӯ��(PE)
                                     'S_VAL_PB_NEW',  # �о���(PB)
                                     'S_VAL_PE_TTM',  # ��ӯ��(PE,TTM)
                                     'S_VAL_PCF_OCF',  # ������(PCF,��Ӫ�ֽ���)
                                     'S_VAL_PCF_OCFTTM',  # ������(PCF,��Ӫ�ֽ���TTM)
                                     'S_VAL_PCF_NCF',  # ������(PCF,�ֽ�����)
                                     'S_VAL_PCF_NCFTTM',  # ������(PCF,�ֽ�����TTM)
                                     'S_VAL_PS',  # ������(PS)
                                     'S_VAL_PS_TTM',  # ������(PS,TTM)
                                     'S_DQ_TURN',  # ������
                                     'S_DQ_FREETURNOVER',  # ������(��׼.������ͨ�ɱ�)
                                     'TOT_SHR_TODAY',  # �����ܹɱ�
                                     'FLOAT_A_SHR_TODAY',  # ������ͨ�ɱ�
                                     # 'S_DQ_CLOSE_TODAY',             # �������̼�
                                     'S_PRICE_DIV_DPS',  # �ɼ�/ÿ����Ϣ
                                     'S_PQ_ADJHIGH_52W',  # 52����߼�(��Ȩ)
                                     'S_PQ_ADJLOW_52W',  # 52����ͼ�(��Ȩ)
                                     'FREE_SHARES_TODAY',  # ����������ͨ�ɱ�
                                     'NET_PROFIT_PARENT_COMP_TTM',  # ����ĸ��˾������(TTM)
                                     'NET_PROFIT_PARENT_COMP_LYR',  # ����ĸ��˾������(LYR)
                                     'NET_ASSETS_TODAY',  # ���վ��ʲ�
                                     'NET_CASH_FLOWS_OPER_ACT_TTM',  # ��Ӫ��������ֽ���������(TTM)
                                     'NET_CASH_FLOWS_OPER_ACT_LYR',  # ��Ӫ��������ֽ���������(LYR)
                                     'OPER_REV_TTM',  # Ӫҵ����(TTM)
                                     'OPER_REV_LYR',  # Ӫҵ����(LYR)
                                     'NET_INCR_CASH_CASH_EQU_TTM',  # �ֽ��ֽ�ȼ��ﾻ���Ӷ�(TTM)
                                     'NET_INCR_CASH_CASH_EQU_LYR',  # �ֽ��ֽ�ȼ��ﾻ���Ӷ�(LYR)
                                     # 'UP_DOWN_LIMIT_STATUS',         # �ǵ�ͣ״̬
                                     # 'LOWEST_HIGHEST_STATUS',        # �����ͼ�״̬
                                     ],

}

CacheLevlels = {
    'LEVEL1' : ['ASHAREEODPRICES', 'FEATURES_FILTER', 'RESPONSE_FILTER', 'RESPONSE'],
    'LEVEL2' : ['ASHARECAPITALIZATION', 'ASHAREFLOATHOLDER']
}
