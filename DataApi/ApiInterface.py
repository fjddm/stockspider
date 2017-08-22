class CApiInterface(object):
    def __init__(self, histDataObj_ = None, tickDataObj_ = None):
        self.histDataObj_ = histDataObj_
        self.tickDataObj_ = tickDataObj_
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
        return self.histDataObj_.getHistData(code_ = code_, start_ = start_, end_ = end_, type_ = type_, fqType_ = fqType_, retryCount_ = retryCount_, pause_ = pause_)

    def getTickData(self, code_, type_ = 'R', retryCount_ = 3, pause_ = 0.001):
        """
        获取Tick数据
        Parameters
        ------
          code_:string
                      股票代码 e.g. 600848
          type_：string
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
        return self.tickDataObj_.getTickData(code_ = code_, type_ = type_, retryCount_ = retryCount_, pause_ = pause_)