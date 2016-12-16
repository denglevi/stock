# -*- coding: utf-8 -*-
import scrapy
import re
import os
import time


class HexunSpider(scrapy.Spider):
    name = "hexun"
    allowed_domains = ["hexun.com"]
    start_urls = [
        'http://quote.tool.hexun.com/hqzx/quote.aspx?type=2&market=0&sorttype=3&updown=up&page=1&count=50']
    page = 1
    itemTitle = [u'代码', u'名称', u'最新价', u'涨跌幅', u'昨收', u'今开', u'最高', u'最低', u'成交量', u'成交额', u'换手', u'振幅', u'量比']

    def createDataFile(self, stockCode):
        y = time.strftime('%Y')
        m = time.strftime('%m')
        d = time.strftime('%d')

        dataPath = 'E:\Project\stock/data/'

        if not os.path.exists(dataPath):
            os.mkdir(dataPath)

        if not os.path.exists(dataPath + stockCode):
            os.mkdir(dataPath + stockCode)

        if not os.path.exists(dataPath + stockCode + '/' + y):
            os.mkdir(dataPath + stockCode + '/' + y)

        if not os.path.exists(dataPath + stockCode + '/' + y + '/' + m):
            os.mkdir(dataPath + stockCode + '/' + y + '/' + m)

        if not os.path.exists(dataPath + stockCode + '/' + y + '/' + m):
            os.mkdir(dataPath + stockCode + '/' + y + '/' + m)

        return dataPath + stockCode + '/' + y + '/' + m + '/' + d + '.txt'

    def parse(self, response):
        data = response.body_as_unicode()

        if not data:
            print(u'数据获取完成!')
            return
        else:
            data = re.findall(r"\[.*\]", data, re.M)
            for x in data:
                x = x.replace("[", "").replace("]", "").replace('\'', '')
                stock = x.split(',')
                stockCode = stock[0]
                fileName = self.createDataFile(stockCode)
                with open(fileName, 'a') as fp:
                    print('-'.join(stock) + '-' + str(time.time()))
                    fp.write('-'.join(stock) + '-' + str(time.time()) + "\n")
                fp.close()
        self.page = self.page + 1
        url = 'http://quote.tool.hexun.com/hqzx/quote.aspx?type=2&market=0&sorttype=3&updown=up&page=%d&count=50' % self.page
        url = response.urljoin(url)
        yield scrapy.Request(url, callback=self.parse)
