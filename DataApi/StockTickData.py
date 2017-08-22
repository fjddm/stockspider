from .ApiBase import CApiBase
import pandas as pd
import time

class CTickDataBase(CApiBase):
    ltype_ = ['R', '5R']
    lColName_ = ['amount', 'avgPrice', 'date', 'netChangeRatio', 'preClose', 'price', 'time', 'volume']
    dColMap_ = []
    def getTickData(self, *args, **kwargs):
        """
        获取Tick数据
        Parameters
        ------
          code_:string
                      股票代码 e.g. 600848
          dtype_：string
                      数据类型，R=1日实时 5R=5日实时 默认R
          retryCount_ : int, 默认 3
                     如遇网络等问题重复执行的次数
          pause_ : int, 默认 0
                    重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
        return
        -------
          DataFrame
              属性:日期. 时间, 价格, 成交量, 均价, 换手率, 昨收, 成交金额
        """
        try:
            df_ = self.checkAndRequest(*args, **kwargs)
            return df_
        except Exception as e:
            print(e)

class CBaiduTickData(CTickDataBase):
    urlFormat_ = 'https://gupiao.baidu.com/api/stocks/%s?from=pc&os_ver=1&cuid=xxx&vv=100&format=json&stock_code=%s&timestamp=%d'
    domains_ = {'R': 'stocktimeline',  '5R': 'stocktimelinefive', }
    def getUrl(self, code_, symbol_, type_, *args, **kwargs):
        return self.urlFormat_ % (self.domains_[type_], symbol_, int(time.time() * 1000))
    def parse(self, response_):
        if response_['errorNo'] != 0:
            raise Exception('ErrorNo:%d ErrorMsg:%s'%(response_['errorNo'],response_['errorMsg']))
        return pd.DataFrame(response_['timeLine'])