# coding:utf-8
import os
import MySQLdb
import numpy as np
import matplotlib.pyplot as plt
import sys


class readCSVData:
    conn = None
    cursor = None

    def __init__(self):
        self.conn = MySQLdb.connect(user="root", passwd="", host="127.0.0.1", db="stock2")
        self.conn.set_character_set('utf8')
        self.cursor = self.conn.cursor()

    def createTable(self, name):
        sql = "create table %s (id int(4) primary key auto_increment,openPrice varchar(80),highPrice varchar(80),lowPrice varchar(80),closePrice varchar(80),volume varchar(80),cDate varchar(80));" % name

        # sql = "CREATE TABLE stock2.table_name(sss VARCHAR(90),column_2 INT,column_3 INT,column_4 INT,column_5 INT);"

        return self.cursor.execute(sql)

    def importData(self, dataPath,dataFile=''):
        files = os.listdir(dataPath)
        self.cursor.execute('show tables;')
        tables = self.cursor.fetchall()
        tables = np.asarray(tables).ravel()
        for file in files:
            fileName = file.lower().replace('.csv', '')
            if dataFile != '':
                if dataFile != fileName:
                    continue
            if fileName in tables:
                self.cursor.execute('drop table %s' % fileName)
            res = self.createTable(fileName)
            if res != 0:
                print("创建数据表%s失败", fileName)
                continue
            fp = open(os.path.join(dataPath, file), 'r', encoding='utf-8')
            lines = fp.readlines()
            data = lines[1:]
            for x in data:
                x = x.strip().split(',')
                sql = "insert into %s (cDate,openPrice,highPrice,lowPrice,closePrice,volume) values ('%s','%s','%s','%s','%s','%s');" % (
                    fileName,
                    x[1].replace('/', '-').replace('"', ''), x[2].replace('"', ''), x[3].replace('"', ''),
                    x[4].replace('"', ''), x[5].replace('"', ''), x[6].replace('"', ''))
                print(sql)
                self.cursor.execute(sql)
            fp.close()

        self.cursor.close()
        self.conn.commit()
        self.conn.close()

    def getMeanPrice(self, name, days):

        sql = 'select closePrice from %s order by id desc limit 100' % name
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        x1 = int(100 / days)
        y1 = days
        priceArr = np.asarray(res).reshape((x1, y1))
        meanPrice = []

        for x in priceArr:
            y = []
            for xx in x:
                y.append(float(xx))
            meanPrice.append(np.mean(y))

        sql = 'select closePrice from %s order by id desc limit %d' % (name, x1)
        self.cursor.execute(sql)
        price = self.cursor.fetchall()
        return meanPrice, np.asarray(price).ravel()

    def showPriceInfo(self, name, days):
        meanPrice, price = readCSVData.getMeanPrice(name, days)
        print(meanPrice)
        print(price)

        fg = plt.figure()
        ax = fg.add_subplot(111)

        ax.plot(meanPrice[::-1])
        ax.plot(price[::-1])

        ax.legend((u'meanPrice', u'price'), loc='best')
        plt.show()

    def getLowHighPrice(self, name, days):

        sql = 'select closePrice from %s order by id desc limit 100' % name
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        x1 = int(len(res) / days)
        y1 = days
        priceArr = np.asarray(res[0:x1 * days]).reshape((x1, y1))
        highPrice = []
        lowPrice = []
        meanPrice = []
        price = np.asarray(res[0:x1])
        for x in priceArr:
            y = []
            for xx in x:
                y.append(float(xx))
            highPrice.append(np.max(y))
            lowPrice.append(np.min(y))
            meanPrice.append(np.mean(y))

        return highPrice, lowPrice, price, meanPrice


if __name__ == '__main__':

    argv = sys.argv
    if len(argv) < 2:
        print('缺少参数!')
        exit()

    if argv[1] == 'readCSV':
        dataPath = argv[2]
        readCSVData = readCSVData()

        if len(argv) > 3:
            readCSVData.importData(dataPath,dataFile=argv[3])
        else:
            readCSVData.importData(dataPath)

    if argv[1] == 'importData':
        readCSVData = readCSVData()
        if len(argv) < 4:
            print('缺少参数!')

        code = argv[2]
        days = int(argv[3])
        readCSVData.showPriceInfo(code, days)

    if argv[1] == 'highlow':
        readCSVData = readCSVData()
        if len(argv) < 4:
            print('缺少参数!')
            exit()

        code = argv[2]
        days = int(argv[3])
        highPrice, lowPrice, price, meanPrice = readCSVData.getLowHighPrice(code, days)

        print(highPrice)
        print(lowPrice)
        print(meanPrice)
        print(price)

        fg = plt.figure()
        ax = fg.add_subplot(111)

        ax.plot(highPrice[::-1])
        ax.plot(lowPrice[::-1])
        ax.plot(meanPrice[::-1])
        ax.plot(price[::-1])

        ax.legend((u'highPrice', u'lowPrice', u'meanPrice', u'price'), loc='best')
        plt.title(code)
        plt.show()
