import json
import pandas as pd
import time
from abc import ABCMeta, abstractmethod
try:
    from urllib.request import urlopen,Request
except ImportError:
    from urllib2 import urlopen, Request
from pandas.io.json import json_normalize

class CApiBase(object):
    __metaclass__ = ABCMeta
    dColMap_ = {}
    lColName_ = []
    ltype_ = []

    @staticmethod
    def codeToSymbol(code_):
        if len(code_) != 6:
            return ''
        else:
            return "sh%s"%code_ if code_[:1] in ['5','6','9'] else "sz%s"%code_

    @staticmethod
    def openRequest(url_,  callBack_, retryCount_ = 3, timeout_ = 10, pause_ = 0.001, *args, **kwargs):
        if callBack_ == None:
            raise Exception("OpenResult Error: callBack is None")

        ex_ = None
        for _ in range(retryCount_):
            try:
                request_ = Request(url_)
                lines_ = urlopen(request_, timeout=timeout_).read()
                if len(lines_) < 15:  # no data
                    time.sleep(pause_)
                    continue
                response_ = json.loads(lines_.decode('utf-8'))
                return callBack_(response_)
            except Exception as e:
                ex_ = e
                time.sleep(pause_)
        raise ex_

    def checkAndRequest(self, code_, type_, *args, **kwargs):
        if type_.upper() not in self.ltype_:
            raise Exception('dtype error %s' % repr(type_.upper()) + ' not in %s' % repr(self.ltype_))
        symbol_ = self.codeToSymbol(code_)
        if symbol_ == '':
            raise Exception('code %s error, symbol is null' % code_)
        url_ = self.getUrl(code_, symbol_, type_, *args, **kwargs)
        df_ = self.openRequest(url_ = url_, callBack_ = self.parse, *args, **kwargs)
        if not isinstance(df_, pd.DataFrame):
            raise Exception("Result Data Type Error: data type is %s, not %s"%(type(df_), type(pd.DataFrame())))
        if len(self.dColMap_) != 0:
            df_.rename(columns = self.dColMap_, inplace = True)
        if len(self.lColName_) != 0:
            df_.drop(df_.columns.difference(self.lColName_), axis = 1, inplace = True)
        return df_

    @abstractmethod
    def getUrl(self, code_, symbol_, dtype_, *args, **kwargs):
        pass

    @abstractmethod
    def parse(self, response_):
        pass