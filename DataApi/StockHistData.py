from .ApiBase import CApiBase
import pandas as pd
import time
import datetime

class CHistDataBase(CApiBase):
    ltype_ = ['D', 'W', 'M']
    lColName_ = ['amount','close','date','high','low','netChangeRatio','open', 'preClose','volume']
    dColMap_ = []
    def getHistData(self, *args, **kwargs):
        try:
            df_ = self.checkAndRequest(*args, **kwargs)
            return df_
        except Exception as e:
            print(e)

class CBaiduHistData(CHistDataBase):
    urlFormat_ = 'https://gupiao.baidu.com/api/stocks/%s?from=pc&os_ver=1&cuid=xxx&vv=100&format=json&stock_code=%s&step=3&start=%s&count=%d&fq_type=%s&timestamp=%d'
    domains_ = {'D': 'stockdaybar', 'W': 'stockweekbar', 'M': 'stockmonthbar',}
    def getUrl(self, code_, symbol_, type_, fqType_ = 'no', start_ = '', end_ = '', *args, **kwargs):
        count_ = 640
        lastdate_ = end_
        if start_ == '':
            count_ = 10000
        elif lastdate_ != '':
            d1 = datetime.datetime.strptime(start_, '%Y%m%d')
            d2 = datetime.datetime.strptime(lastdate_, '%Y%m%d')
            count_ = (d2-d1).days
            if count_ > 10000:
                count_ = 10000
        return self.urlFormat_ % (self.domains_[type_], symbol_, lastdate_, count_, fqType_, int(time.time() * 1000))

    def parse(self, response_):
        print(response_)
        if response_['errorNo'] != 0:
            raise Exception('ErrorNo:%d ErrorMsg:%s'%(response_['errorNo'],response_['errorMsg']))
        jslist_ = []
        for item_ in response_['mashData']:
            item_['kline']['date'] = item_['date']
            jslist_.append(item_['kline'])
        return pd.DataFrame(jslist_)