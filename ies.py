from ts import *

def simpleExponentialSmoothing(observedData, alpha):
    predictedData = observedData[:]
    for i in range(1, len(observedData)):
        predictedData[i] = (1 - alpha) * predictedData[i-1] + alpha * observedData[i-1]
    return (1 - alpha) * predictedData[-1] + alpha * observedData[-1]

def intervalExponentialSmoothing(ts, alpha):

    indexs = ts.getIndexList()
    res = []

    length = len(ts.getDataList())
    pivot = int(length / 3)
    for i in range(length-pivot-1, length-1):
        timestamp = indexs[i]
        hr = timestamp.hour
        tstmp = ts.filterTime(end=timestamp)
        tstmp = tstmp.getIntervalListByHour(hr)
        obData = tstmp.getDataList()
        res.append(simpleExponentialSmoothing(obData, alpha))

    ts.addCol(res, 'ies')

    return ts


def main():
    ts = TimeSeriesData.readTsFile("internet-traffic-data-20041119-20050127.csv")
    ts = intervalExponentialSmoothing(ts, 1)
    ts.plot()


if __name__ == '__main__':
    main()