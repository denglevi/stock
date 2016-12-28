# -*- coding:utf-8 -*-
import MySQLdb
import os


class ImportDataToDB:
    conn = None
    cursor = None

    def __init__(self):
        self.conn = MySQLdb.connect(user="root", passwd="", host="127.0.0.1", db="stock2")
        self.conn.set_character_set('utf8')
        self.cursor = self.conn.cursor()

    def readInfoData(self):
        dirPath = './../data/'
        files = os.listdir(dirPath)
        for file in files:
            sql = "select * from stockInfo where code = '%s'" % file
            self.cursor.execute(sql)
            stock = self.cursor.fetchone()
            if not stock:
                self.insertStock(dirPath, file)
            else:
                self.updateStock(dirPath, file,stock)
        self.cursor.close()
        self.conn.commit()
        self.conn.close()

    def insertStock(self, dirPath, file):
        filePath = dirPath + file + '/info.txt'
        if not os.path.exists(filePath):
            return
        with open(filePath, "r") as fp:
            data = fp.readlines()
        val = []
        for x in data:
            x = x.strip()
            line = x.split('-')
            val.append(line[1])

        sql = 'insert into stockInfo(name,code,shareholder,institutional,deviation,district,linkUrl,' \
              'lootchips,iratia,maincost,priceLimit,updateTime,cprice) values ("%s","%s","%s","%s","%s","%s","%s","%s",' \
              '"%s","%s","%s","%s","%s");' % (val[1], file, val[0], val[2], \
                                              val[4], val[6], val[7], \
                                              val[10], val[12], val[13], val[15], val[17], val[8])
        return self.cursor.execute(sql)

    def updateStock(self, dirPath, file,stock):
        filePath = dirPath + file + '/info.txt'
        if not os.path.exists(filePath):
            return False
        with open(filePath, "r") as fp:
            data = fp.readlines()
        val = []
        for x in data:
            x = x.strip()
            line = x.split('-')
            val.append(line[1])

        if(val[17] == stock[12]):
            return False


        sql = 'update stockInfo set name="%s",code="%s",shareholder="%s",institutional="%s",deviation="%s",district="%s",linkUrl="%s",' \
              'lootchips="%s",iratia="%s",maincost="%s",priceLimit="%s",updateTime="%s",cprice="%s" where code="%s";' % (val[1], file, val[0], val[2], \
               val[4], val[6], val[7], \
               val[10], val[12], val[13], val[15], val[17], val[8],file)
        return self.cursor.execute(sql)

    def readStockPriceInfo(self):
        self.cursor.execute("truncate table stocklist;")
        dirPath = './../data/'
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
                        with open(filePath,"r") as fp:
                            info = fp.readlines()
                            for x in info:
                                data = x.strip().split('-')
                                self.inserStockDayPrice(data)
        self.cursor.close()
        self.conn.commit()
        self.conn.close()
        print("数据导入完成!")

    def inserStockDayPrice(self,data):
        # print(data)
        if len(data) == 15:
            sql = 'insert into stockList(name,code,latestPrice,rangeNum,lastPrice,openPrice,highPrice,' \
              'lowPrice,volume,volumeNum,updateTime,changeRate,amp) values ("%s","%s","%s","%s","%s","%s","%s","%s",' \
              '"%s","%s","%s","%s","%s");' % (data[1], data[0],data[2],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[14],data[11],data[12])
        else:
            sql = 'insert into stockList(name,code,latestPrice,rangeNum,lastPrice,openPrice,highPrice,' \
              'lowPrice,volume,volumeNum,updateTime,changeRate,amp) values ("%s","%s","%s","%s","%s","%s","%s","%s",' \
              '"%s","%s","%s","%s","%s");' % (data[1], data[0],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[13],data[10],data[11])
        print(sql)
        return self.cursor.execute(sql)
if __name__ == '__main__':
    importData = ImportDataToDB()
    # importData.readInfoData()
    importData.readStockPriceInfo()
