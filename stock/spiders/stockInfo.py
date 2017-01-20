# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import re
import execjs
import os
import time


class StockinfoSpider(scrapy.Spider):
    name = "stockInfo"
    allowed_domains = ["hexun.com"]
    start_urls = ['http://stockdata.stock.hexun.com/gszl/data/jsondata/jbgk.ashx?count=20&titType=null&page=1&callback=hxbase_json15']
    num = 1
    itemTitle = {
        'district':u'所属地域',
        'Institutional':u'注册资本(万元)',
        'deviation':u'所属行业',
        'Pricelimit':u'总股本(亿股)',
        'Cprice':u'收盘价',
        'maincost':u'所属概念',
        'shareholders':u'流通市值(亿元)',
        'Iratio':u'市盈率',
        'lootchips':u'流通股本(亿股)',
        'Stockname':u'名称',
        'time':u'时间'
    }
    def parse(self, response):
        res = response.body_as_unicode()
        if res == 'hxbase_json15({sum:0,list:[]})':
            print(u'数据获取完成!')
            return

        data = re.findall(r"list:\[.*\]", res, re.M)

        data = data[0].replace('list:', '').replace('', '')
        self.num = self.num + 1
        stocks = execjs.eval(data)
        for stock in stocks:
            kv = {}
            code = '000000'
            for item in stock:
                if item == 'Stockname':
                    code = re.findall(r"\d+", stock[item])
                    code = code[0]
                v = Selector(text=stock[item]).xpath('//a/text()').extract()
                if not v:
                    v = stock[item]
                else:
                    v = v[0]

                kv[item] = v
            kv['time'] = time.time()
            print(code)
            self.createInfoFile(code,kv)

        url = 'http://stockdata.stock.hexun.com/gszl/data/jsondata/jbgk.ashx?count=20&titType=null&page=%d&callback=hxbase_json15'%self.num
        response.urljoin(url)
        yield scrapy.Request(url, callback=self.parse)

    def createInfoFile(self, code, info):

        basePath = 'E:\Project\stock/data/'
        # basePath = '/usr/local/stock/data/'
        if not os.path.exists(basePath):
            os.mkdir(basePath)

        stockPath = basePath + str(code)
        if not os.path.exists(stockPath):
            os.mkdir(stockPath)

        infoFilePath = stockPath + '/' + 'info.txt'
        if os.path.exists(infoFilePath):
            os.remove(infoFilePath)
        with open(infoFilePath, 'a') as fp:
            for item in info:
                kvStr = "%s-%s\n"%(item,info[item])
                fp.write(kvStr)
            fp.close()
