import pandas as pd

class TimeSeriesData:

    def __init__(self, ts):
        self.ts = ts

    @classmethod
    def readTsFile(cls, fileName):
        headers = ['DateTime', 'Value']
        ts = pd.read_csv(fileName, sep=',', header=None, names=headers)
        ts['DateTime'] = pd.to_datetime(ts['DateTime'], format='%Y-%m-%d %H:%M:%S')
        ts.index = ts['DateTime']
        return TimeSeriesData(ts)

    def __repr__(self):
        return self.ts.__repr__()

    def getInterval(self):
        interval = self.ts['DateTime'][1] - self.ts['DateTime'][0]
        return interval

    def getStartInterval(self):
        return list(self.ts['DateTime'])[0]

    def getEndInterval(self):
        return list(self.ts['DateTime'])[-1]

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

    def getDataList(self):
        return list(self.ts['Value'])

# ts = TimeSeriesData.readTsFile("internet-traffic-data-20041119-20050127.csv")
# ts = ts.filterTime('2004-11-25', '2004-12-05')
# print(ts)
# ts = ts.changeInterval('week')
# print(ts)
# print(ts.getDataList())