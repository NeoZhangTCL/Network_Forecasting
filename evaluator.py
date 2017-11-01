def getMPE(actualData, forecastData):
    if len(actualData) != len(forecastData):
        raise Exception("the observe list and forecast list must has same length")
    size = len(actualData)
    percentageErrorSum = 0
    for i in range(size):
        if actualData[i] == 0:
            size = size - 1
        else:
            percentageErrorSum = percentageErrorSum + (actualData[i] - forecastData[i]) / actualData[i]
    return percentageErrorSum / size
