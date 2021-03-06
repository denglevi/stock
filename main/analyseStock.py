import MySQLdb
#import matplotlib.pyplot as plt
import time
#from matplotlib.font_manager import *
import numpy as np
import os


class AnalyseStock:
    conn = None
    cursor = None

    def __init__(self):
        self.conn = MySQLdb.connect(user="root", passwd="123456", host="127.0.0.1", db="stock")
        self.conn.set_character_set('utf8')
        self.cursor = self.conn.cursor()

    def getStockData(self, sql, num=1):
        self.cursor.execute(sql)

        data = self.cursor.fetchall()
        if not data:
            return None
        x = []
        y = []
        d = []
        lastData = None
        currentData = None
        for z in data:

            if not lastData:
                lastData = z
                continue

            # 如果上一个日期和当前日期不一样的即存储lastData数据
            currentData = z

            lastDateStr = time.strftime('%Y%m%d', time.localtime(round(float(lastData[1]))))
            currentDateStr = time.strftime('%Y%m%d', time.localtime(round(float(currentData[1]))))

            if lastDateStr != currentDateStr:
                x.append(float(lastData[0]) / num)
                y.append(lastDateStr)
                d.append((lastData, z[0]))
            lastData = currentData
        if not currentData:
            currentData = lastData
            currentDateStr = time.strftime('%Y%m%d', time.localtime(round(float(currentData[1]))))
        x.append(float(currentData[0]) / num)
        y.append(currentDateStr)
        d.append((currentData, z[0]))
        return [x, y, d]

    # 计算均线
    def priceMean(self, data, daySize):

        x = int(len(data) / daySize)
        y = daySize
        l = len(data) - (x * daySize)

        priceArr = np.asarray(data[l:]).reshape((x, y))
        meanData = []
        for price in priceArr:
            meanData.append(np.mean(price))
        return meanData

    # 判断是否长期处于低价位
    def isLowestPrice(self, data):
        lowPrice = np.min(data)
        meanPrice = np.mean(data)

        if data[-1] < lowPrice and data[-1] < meanPrice:
            return data[-1]
        else:
            return None

    # 获取所有股票的最后10天的收盘价
    def getLastTenDayPrice(self):
        stockPath = './../data/'
        stockFiles = os.listdir(stockPath)
        data = {}
        for stockFile in stockFiles:
            sql = "select latestPrice,updateTime from stocklist where code = '%s'" % stockFile
            #print(sql)
            dataPrice = self.getStockData(sql, 1)
            if not dataPrice:
                continue
            data[stockFile] = dataPrice[0]

        return data


if __name__ == "__main__":
    #font = FontProperties(fname=os.path.expandvars(r"%windir%\fonts\simsun.ttc"), size=14)

    analyseStock = AnalyseStock()

    allPrice = analyseStock.getLastTenDayPrice()

    # print(allPrice)
    codesUp = {}
    codesDown = {}
    lowestPrice = {}
    for code in allPrice:
        price = allPrice[code]
        meanPrice = analyseStock.priceMean(price, 5)
        res = analyseStock.isLowestPrice(price)
        if analyseStock.isLowestPrice(price):
            lowestPrice[code] = res

        #print(code)
        #print(price)
        #print(meanPrice)
        if not price or not meanPrice:
            continue

        if len(price) < 2 or len(meanPrice) < 2:
            continue

        val4 = price[-2]
        val5 = meanPrice[-2]

        val1 = price[-1]
        val2 = meanPrice[-1]

        val6 = val5 - val4
        if val6 > 0 and val1 == val2 and val1 >= val5:
            codesUp[val6] = (code,val1)

        if val6 < 0 and val1 == val2 and val1 <= val5:
            codesDown[val6] = (code,val1)

    keysUp = codesUp.keys()
    keysDown = codesDown.keys()
    filePath = './../analyseResultData/' + time.strftime('%Y-%m-%d') + '.txt'

    fp = open(filePath, 'a')
    fp.write("====================%s====================\n" % time.strftime("%Y-%m-%d %H:%M:%S"))
    for key in sorted(keysUp, reverse=True):
        fp.write('up-' + str(key) + '-' + str(codesUp[key][0]) +  '-'+str(codesUp[key][1]) +"\n")

    for key in sorted(keysDown):
        fp.write('down-' + str(key) + '-' + str(codesDown[key][0]) +  '-'+str(codesDown[key][1]) +"\n")

    for key in lowestPrice:
        fp.write('lowestPrice-' + str(key) + '-' + str(lowestPrice[key]) + "\n")

    fp.close()
    #print(codesUp)
    #print(codesDown)
    #print(lowestPrice)
    print("创建文件成功!")
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.plot(x3)
    # ax.plot(meanPrice2)
    # ax.plot(meanPrice4)
    # ax.legend((u'收盘价', u'最高价'), loc='best', prop=font)
    # ax.legend((u'最高价', u'交易量', u'收盘价', u'开盘价', u'换手率'), loc='best', prop=font)
    # plt.title(u'趋势图', fontproperties=font)
    # plt.show()
