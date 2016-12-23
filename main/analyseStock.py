import MySQLdb
import matplotlib.pyplot as plt
import time
from matplotlib.font_manager import *


class AnalyseStock:
    conn = None
    cursor = None

    def __init__(self):
        self.conn = MySQLdb.connect(user="root", passwd="", host="127.0.0.1", db="stock2")
        self.conn.set_character_set('utf8')
        self.cursor = self.conn.cursor()

    def getStockData(self, sql, num):
        self.cursor.execute(sql)

        data = self.cursor.fetchall()
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

            lastDateStr = time.strftime('%Y%m%d',time.localtime(round(float(lastData[1]))))
            currentDateStr = time.strftime('%Y%m%d',time.localtime(round(float(currentData[1]))))

            if lastDateStr != currentDateStr:
                x.append(float(lastData[0]) / num)
                y.append(lastDateStr)
                d.append((lastData, z[0]))
            lastData = currentData

        x.append(float(currentData[0]) / num)
        y.append(currentDateStr)
        d.append((currentData, z[0]))
        print(y)
        return (x, y, d)


if __name__ == "__main__":
    font = FontProperties(fname=os.path.expandvars(r"%windir%\fonts\simsun.ttc"), size=14)
    sql = "select highPrice,updateTime from stocklist where code = '600545'"
    analyseStock = AnalyseStock()
    x1, y1, d1 = analyseStock.getStockData(sql, 1)

    sql = "select volume,updateTime from stocklist where code = '600545'"
    x2, y2, d2 = analyseStock.getStockData(sql, 100000)

    sql = "select lastPrice,updateTime from stocklist where code = '600545'"
    x3, y3, d3 = analyseStock.getStockData(sql, 1)

    sql = "select openPrice,updateTime from stocklist where code = '600545'"
    x4, y4, d4 = analyseStock.getStockData(sql, 1)

    sql = "select changeRate,updateTime from stocklist where code = '600545'"
    x5, y5, d5 = analyseStock.getStockData(sql, 1)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x1)
    ax.plot(x2)
    ax.plot(x3)
    ax.plot(x4)
    ax.plot(x5)
    ax.legend((u'最高价', u'交易量', u'收盘价', u'开盘价', u'换手率'), loc='best', prop=font)
    plt.title(u'趋势图', fontproperties=font)
    plt.show()
