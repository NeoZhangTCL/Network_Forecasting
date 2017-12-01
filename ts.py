import pandas as pd
import matplotlib.pyplot as plt

class TimeSeriesData:

    def __init__(self, ts):
        self.ts = ts

    @classmethod
    def readTsFile(cls, fileName):
        headers = ['DateTime', 'ObservedValue']
        ts = pd.read_csv(fileName, sep=',', header=None, names=headers)
        ts['DateTime'] = pd.to_datetime(ts['DateTime'], format='%Y-%m-%d %H:%M:%S')
        ts.index = ts['DateTime']
        del ts['DateTime']
        return TimeSeriesData(ts)

    def __repr__(self):
        return self.ts.__repr__()

    def addCol(self, dataList, colName):
        se = pd.Series(dataList)
        self.ts[colName] = se

    def plot(self):
        self.ts.plot()
        plt.show()

    def getIntervalLength(self):
        indexs = self.ts.index.tolist()
        interval = None
        if len(indexs) > 1:
            interval = indexs[1] - indexs[0]
        return interval

    def getStartInterval(self):
        return self.ts.index[0]

    def getEndInterval(self):
        return self.ts.index[-1]

    def filterTime(self, start=None, end=None):
        if start == None:
            start = str(self.getStartInterval())
        if end == None:
            end = str(self.getEndInterval())
        return TimeSeriesData(self.ts.ix[start:end])

    def changeInterval(self, interval=None):
        ts = self.ts
        if interval == 'day':
            ts = ts.resample('D').sum()
        elif interval == 'week':
            ts = ts.resample('W').sum()
        return TimeSeriesData(ts)

    def getDataList(self, valueName = 'ObservedValue'):
        return list(self.ts[valueName])

# ts = TimeSeriesData.readTsFile("internet-traffic-data-20041119-20050127.csv")
# ts = ts.filterTime('2004-11-25', '2004-12-05')
# print(ts.getStartInterval())
# ts = ts.changeInterval('week')
# print(ts)
# print(ts.getDataList())
# print(ts.plot())