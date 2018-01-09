# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from food_menu.items import FoodMenuItem

class MenuSpider(scrapy.Spider):
    name = 'menu'
    allowed_domains = ['quananngon.com.vn']
    start_urls = ['http://quananngon.com.vn/san-pham.html']
    domain = 'http://quananngon.com.vn'

    def parse(self, response):
        for i in range(15):
            link_page = self.start_urls[0] + '?page=' + str(i + 1)
            yield Request(link_page, callback=self.parse_url)

    def parse_url(self, response):
        sel = Selector(response)
        links = sel.xpath('//*[@id="main-content"]/div[1]/div/div/div/div/div[3]/div/div[1]/div/div/div/div/div[2]/h3/a/@href').extract()
        images = sel.xpath('//*[@id="main-content"]/div[1]/div/div/div/div/div[3]/div/div[1]/div/div/div/div/div[1]/a/img/@src').extract()
        if links:
            for i in range(len(links)):
                product_link = self.domain + links[i]
                yield Request(product_link, callback=self.parse_product, meta={'image': images[i]})

    def parse_product(self, response):
        sel = Selector(response)
        item = FoodMenuItem()
        item['title'] = sel.xpath('//*[@id="main-content"]/div[1]/div/div/div/div/div[2]/div/div/div/section/div/div/div/div/div/div[2]/div[1]/h1/text()').extract()[0]
        item['image'] = response.meta['image']
        item['link'] = response.url
        item['price'] = sel.xpath('//*[@id="main-content"]/div[1]/div/div/div/div/div[2]/div/div/div/section/div/div/div/div/div/div[2]/div[2]/div/p/span[2]/text()').extract()[0].replace('  ','')
        yield item
