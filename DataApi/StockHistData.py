from .ApiBase import CApiBase
import pandas as pd
import time
import datetime

class CHistDataBase(CApiBase):
    ltype_ = ['D', 'W', 'M']
    lColName_ = ['amount','close','date','high','low','netChangeRatio','open', 'preClose','volume']
    dColMap_ = []
    def getHistData(self, code_, start_ = '', end_ = '', type_ = 'D', fqType_ = 'no', retryCount_ = 3, pause_ = 0.001):
        """
                获取个股历史交易记录
                Parameters
                ------
                  code_:string
                              股票代码 e.g. 600848
                  start_:string
                              开始日期 format：YYYYMMDD 为空时取到API所提供的最早日期数据
                  end_:string
                              结束日期 format：YYYYMMDD 为空时取到最近一个交易日数据
                  ktype_：string
                              数据类型，D=日 k线 W=周 M=月，默认为D
                  retryCount_: int, 默认 3
                             如遇网络等问题重复执行的次数
                  pause_ : int, 默认 0
                            重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
                return
                -------
                  DataFrame
                      属性:日期 ，开盘价， 最高价， 收盘价， 最低价， 成交量， 昨日收盘，换手率
        """
        try:
            df_ = self.checkAndRequest(code_, start_ = start_, end_ = end_, type_ = type_, fqType_ = fqType_, retryCount_ = retryCount_, pause_ = pause_)
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