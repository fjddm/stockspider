class CApiInterface(object):
    def __init__(self, histDataObj_ = None, tickDataObj_ = None):
        self.histDataObj_ = histDataObj_
        self.tickDataObj_ = tickDataObj_
    def getHistData(self, *args, **kwargs):
        return self.histDataObj_.getHistData(*args, **kwargs)
    def getTickData(self, *args, **kwargs):
        return self.tickDataObj_.getTickData(*args, **kwargs)