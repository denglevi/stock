# -*- coding: utf-8 -*-
import scrapy


class BankofpaSpider(scrapy.Spider):
    name = "bankOfPA"
    allowed_domains = ["hexun.com"]
    start_urls = ['http://hexun.com/']

    def parse(self, response):
        pass
