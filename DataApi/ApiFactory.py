from .StockHistData import CBaiduHistData
from .StockTickData import CBaiduTickData
from .ApiInterface import CApiInterface

class CApiFactory(object):
    RetObjDict_ = {
        'baidu':lambda : CApiInterface(histDataObj_ = CBaiduHistData(),tickDataObj_ = CBaiduTickData()),
    }
    @staticmethod
    def getObj(key):
        return CApiFactory.RetObjDict_[key]()