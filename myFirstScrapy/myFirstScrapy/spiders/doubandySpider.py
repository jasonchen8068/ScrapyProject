# -*- conding:utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from myFirstScrapy.items import MyfirstscrapyItem
import time


class dbdySpider(scrapy.Spider):
    #spider name
    name = 'movie'
    #fan pa cuo shi
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'}
    url = 'https://movie.douban.com/top250'

    def start_requests(self):
        yield Request(self.url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        item = MyfirstscrapyItem()
        selector = Selector(response)
        movies = selector.xpath('//div[@class="info"]')
        for movie in movies:
            name = movie.xpath('div[@class="hd"]/a/span/text()').extract()
            message = movie.xpath('div[@class="bd"]/p/text()').extract()
            star = movie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()
            number = movie.xpath('div[@class="bd"]/div[@class="star"]/span/text()').extract()
            quote = movie.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            if quote:
                quote = quote[0]
            else:
                quote = ''
            item['title'] = ''.join(name)
            item['movieInfo'] = ';'.join(message).replace(' ', '').replace('\n', '')
            item['star'] = star[0]
            item['number'] = number[1]
            item['quote'] = quote
            yield item
        nextpage = selector.xpath('//span[@class="next"]/link/@href').extract()

        time.sleep(3)

        if nextpage:
            nextpage = nextpage[0]

            yield Request(self.url + str(nextpage), headers=self.headers, callback=self.parse)