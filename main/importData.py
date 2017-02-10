# -*- coding:utf-8 -*-
import os
import click
import chardet
import codecs
import time
from myDBConnector import MyDBConnector

class ImportDataToDB():
    myConn = None
    cursor = None
    conn = None
    dataDir = './../data/'

    def __init__(self):
        self.myConn = MyDBConnector()
        self.myConn.conn.set_character_set('utf8')
        self.conn = self.myConn.conn
        self.cursor = self.myConn.cursor

    def readInfoData(self):
        dirPath = './../data/'
        files = os.listdir(dirPath)
        for file in files:
            sql = "select * from stockinfo where code = '%s'" % file
            self.cursor.execute(sql)
            stock = self.cursor.fetchone()
            if not stock:
                self.insertStock(dirPath, file)
            else:
                self.updateStock(dirPath, file,stock)
        self.cursor.close()
        self.conn.commit()
        self.conn.close()

    def getLatestPrice(self,code):

        y = time.strftime('%Y')
        m = time.strftime('%m')
        d = time.strftime('%d')

        filePath = os.path.join(self.dataDir,code,y,m)
        fileList = os.listdir(filePath)
        filePath = os.path.join(filePath,fileList.pop())
        print(filePath)
        if not os.path.exists(filePath):
            return 0
        with open(filePath, "r") as fp:
            info = fp.readlines()
            x = info.pop()
            data = x.strip().split('-')

        print(data[2])
        return data[2]

    def insertStock(self, dirPath, file):
        filePath = dirPath + file + '/info.txt'
        if not os.path.exists(filePath):
            return
        with open(filePath, "r") as fp:
            data = fp.readlines()
        val = {}
        for x in data:
            x = x.strip()
            line = x.split('-')
            val[line[0]] = line[1]
        # val['Cprice']
        latestPrice = self.getLatestPrice(file)
        sql = 'insert into stockinfo(name,code,shareholder,institutional,deviation,district,linkUrl,' \
              'lootchips,iratia,maincost,priceLimit,updateTime,cprice) values ("%s","%s","%s","%s","%s","%s","%s","%s",' \
              '"%s","%s","%s","%s","%s");' % (val['Stockname'], file, val['shareholders'], val['Institutional'], \
                                              val['deviation'], val['district'], val['StockLink'], \
                                              val['lootchips'], val['Iratio'], val['maincost'], val['Pricelimit'], val['time'], latestPrice)
        return self.cursor.execute(sql)

    def updateStock(self, dirPath, file,stock):
        filePath = dirPath + file + '/info.txt'
        if not os.path.exists(filePath):
            return False
        with open(filePath, "r") as fp:
            data = fp.readlines()
        val = {}
        for x in data:
            x = x.strip()
            line = x.split('-')
            val[line[0]] = line[1]

        # if val['time'] == stock[12]:
        #     return False

        latestPrice = self.getLatestPrice(file)
        sql = 'update stockinfo set name="%s",code="%s",shareholder="%s",institutional="%s",deviation="%s",district="%s",linkUrl="%s",' \
              'lootchips="%s",iratia="%s",maincost="%s",priceLimit="%s",updateTime="%s",cprice="%s" where code="%s";' % (val['Stockname'], file, val['shareholders'], val['Institutional'], \
                                              val['deviation'], val['district'], val['StockLink'], \
                                              val['lootchips'], val['Iratio'], val['maincost'], val['Pricelimit'], val['time'], latestPrice,file)
        print(sql)
        return self.cursor.execute(sql)

    def readStockPriceInfo(self):
        self.cursor.execute("truncate table stocklist;")
        dirPath = '../data/'
        dirs = os.listdir(dirPath)
        for dirStockName in dirs:
            stockDirPath = os.path.join(dirPath,dirStockName)
            stockYearDirs = os.listdir(stockDirPath)
            for stockMonthDir in stockYearDirs:
                stockMonthDir = os.path.join(stockDirPath,stockMonthDir)
                if not os.path.isdir(stockMonthDir):
                    continue
                stockDayFiles = os.listdir(stockMonthDir)
                for stockDayFile in stockDayFiles:
                    filesPath = os.path.join(stockMonthDir,stockDayFile)
                    filesPath = os.listdir(filesPath)
                    for filePath in filesPath:
                        filePath = os.path.join(stockMonthDir,stockDayFile,filePath)
                        try:
                            with open(filePath,"r") as fp:
                                info = fp.readlines()
                                for x in info:
                                    data = x.strip().split('-')
                                    self.inserStockDayPrice(data)
                        except Exception as e:
                            print("except:%s\nfileName:%s"%(e,filePath))
        self.cursor.close()
        self.conn.commit()
        self.conn.close()
        print("数据导入完成!")

    def inserStockDayPrice(self,data):
        # print(data)
        if len(data) == 15:
            sql = 'insert into stocklist(name,code,latestPrice,rangeNum,lastPrice,openPrice,highPrice,' \
              'lowPrice,volume,volumeNum,updateTime,changeRate,amp) values ("%s","%s","%s","%s","%s","%s","%s","%s",' \
              '"%s","%s","%s","%s","%s");' % (data[1], data[0],data[2],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[14],data[11],data[12])
        else:
            sql = 'insert into stocklist(name,code,latestPrice,rangeNum,lastPrice,openPrice,highPrice,' \
              'lowPrice,volume,volumeNum,updateTime,changeRate,amp) values ("%s","%s","%s","%s","%s","%s","%s","%s",' \
              '"%s","%s","%s","%s","%s");' % (data[1], data[0],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[13],data[10],data[11])
        #print(sql)
        return self.cursor.execute(sql)

if __name__ == '__main__':
    importData = ImportDataToDB()
    importData.readInfoData()
    #importData.readStockPriceInfo()
