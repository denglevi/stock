# -*- coding: utf-8 -*-
import scrapy
import sys
import os
import time

sys.path.append("./../../main/")
from main.myDBConnector import MyDBConnector


# 银行股轮动策略
# 始终持有沪深银行指数成分股中市净率最低的股份制银行，每周检查一次，如果发现有新的股份制银行市净率低于原有的股票，则予以换仓。

class BankofpaSpider(scrapy.Spider):
    name = "bankOfPA"
    allowed_domains = ["hexun.com"]
    start_urls = ['http://stockdata.stock.hexun.com/000001.shtml']
    myConn = None
    stockList = None
    stockIndex = 0
    outStr = []

    def __init__(self):
        self.myConn = MyDBConnector()
        sql = "select * from stockinfo where deviation LIKE '%银行%'"
        self.stockList = self.myConn.getData(sql)

    def parse(self, response):
        stockInfo = response.xpath('//td[@class="tb2_new"]/text()').extract()
        # stockCurrentPrice = response.xpath('//span[@id="q_current"]/text()').extract()
        # print(stockInfo)
        try:
            self.outStr.append((False,self.stockList[self.stockIndex][1],stockInfo[3],float(self.stockList[self.stockIndex][13]) / float(stockInfo[3])))
            # self.outStr[self.stockList[self.stockIndex][1]] = {'rate':stockInfo[3],'pa': float(self.stockList[self.stockIndex][13]) / float(stockInfo[3]), 'error': False}
            # self.outStr.append({'name': self.stockList[self.stockIndex][1], 'rate': stockInfo[3],'pa': float(self.stockList[self.stockIndex][13]) / float(stockInfo[3]), 'error': False})
            # outStr = {'name': self.stockList[self.stockIndex][1], 'rate': stockInfo[3],'pa': float(self.stockList[self.stockIndex][13]) / float(stockInfo[3]), 'error': False}
        except Exception as e:
            # self.outStr[self.stockList[self.stockIndex][1]] = {'except': e, 'error': True}
            # self.outStr.append({'name': self.stockList[self.stockIndex][1], 'exception': e, 'error': True})
            outStr = {'name': self.stockList[self.stockIndex][1], 'exception': e, 'error': True}
            # self.writeData(outStr)
        self.stockIndex = self.stockIndex + 1
        if self.stockIndex == len(self.stockList):
            print("数据获取完成!")
            return
        url = self.stockList[self.stockIndex][7]
        url = response.urljoin(url)
        yield scrapy.Request(url, callback=self.parse)
        pass

    def writeData(self,stock):
        policyDataDir = './policyData/'
        if not os.path.exists(policyDataDir):
            os.mkdir(policyDataDir)
        y = time.strftime('%Y')
        m = time.strftime('%m')
        d = time.strftime('%d')

        with open(policyDataDir + y + m + d + '.txt', "a") as fp:
            # for stock in outStr:
            if not stock[0]:
                outStr = "名称：%s,每股净资产:%s,市净率:%2f\n" % (stock[1], stock[2], stock[3])
                fp.write(outStr)
            else:
                outStr = "名称：%s,异常:%s\n" % (stock[1], stock[2])
                fp.write(outStr)

        fp.close()
    def __del__(self):
        # print(2222)
        # print(self.outStr.items(), key=lambda d: d[1]))
        self.outStr = sorted(self.outStr,key=lambda outStr: outStr[3])
        for stock in self.outStr:
            print(stock)
            self.writeData(stock)

