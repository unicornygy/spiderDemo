# -*- coding: utf-8 -*-
import csv

import scrapy
from scrapy import Request


class DemoSpider(scrapy.Spider):
    name = 'demo'
    start_urls = ['https://www.douban.com/doulist/1264675//']

    def parse(self, response):
        informations = response.xpath(
            '//div[@class="title"]/a[@target="_blank"]/text()|//div[@class="abstract"]/text()').extract()
        csvFile = open("books.csv", 'a', encoding="utf-8")
        fileHeader = ["bookName", "author", "publishHouse", "publishDate"]
        dict_writer = csv.DictWriter(csvFile, fileHeader)
        dict_information = {}
        count = 0
        for information in informations:
            information = information.strip()
            if count == 0:
                dict_information['bookName'] = information
                count += 1
            else:
                if "作者" in information:
                    dict_information['author'] = information[3:]
                elif "出版社" in information:
                    dict_information['publishHouse'] = information[4:]
                elif "出版年" in information:
                    dict_information['publishDate'] = information[4:]
                    dict_writer.writerow(dict_information)
                    dict_information.clear()
                    count = 0
        csvFile.close()
        if response.xpath('//span[@class="next"]/a/@href'):
            next_url = response.xpath('//span[@class="next"]/a/@href').extract()[0]
            print(next_url)
            yield Request(next_url, callback=self.parse)
