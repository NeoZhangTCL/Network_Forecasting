from ts import *
from evaluator import *

def simpleExponentialSmoothing(observedData, alpha):
    predictedData = observedData[:]
    for i in range(1, len(observedData)):
        predictedData[i] = (1 - alpha) * predictedData[i-1] + alpha * observedData[i-1]
    return (1 - alpha) * predictedData[-1] + alpha * observedData[-1]

def hourlyES(ts, alpha, pivot):

    indexs = ts.getIndexList()
    res = []

    length = len(ts.getDataList())

    for i in range(pivot, length-1):
        timestamp = indexs[i]
        hr = timestamp.hour
        tstmp = ts.filterTime(end=timestamp)
        tstmp = tstmp.getIntervalListByHour(hr)
        obData = tstmp.getDataList()
        res.append(simpleExponentialSmoothing(obData, alpha))

    tsEndPart = ts.filterTime(start=indexs[pivot+1])
    evalData = tsEndPart.getDataList()

    print('MAPE is', getMAPE(evalData, res))

    return res


def dailyES(ts, alpha, pivot):

    ts = ts.setIntervalLength('day')
    indexs = ts.getIndexList()
    res = []

    length = len(ts.getDataList())

    for i in range(length-pivot-1, length-1):
        timestamp = indexs[i]
        hr = timestamp.hour
        tstmp = ts.filterTime(end=timestamp)
        tstmp = tstmp.getIntervalListByHour(hr)
        obData = tstmp.getDataList()
        res.append(simpleExponentialSmoothing(obData, alpha))

    tsEndPart = ts.filterTime(start=timestamp)
    evalData = tsEndPart.getDataList()

    print('MAPE is', evalData, res)

    return res

def hourlyMain():
    fileName = input('Please input the data file name:')
    ts = TimeSeriesData.readTsFile(fileName)
    length = float(len(ts.getDataList()))
    startPoint = input('Please give a number to start from ' + str(int(length * 2 / 3)) + ' to ' + str(int(length)))
    res = hourlyES(ts, 0.7, int(startPoint))
    colName = 'ies a=' + str(0.7)
    ts.addCol(res, colName)
    ts.plot()
    ts.export('ies.txt')

def main():
    hourlyMain()


if __name__ == '__main__':
    main()