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

    categories = [
        {'link': 'http://quananngon.com.vn/khai-vi-pc19368.html', 'category': 'khai vị'},
        {'link': 'http://quananngon.com.vn/mon-chinh-pc19369.html', 'category': 'món chính'},
        {'link': 'http://quananngon.com.vn/trang-mieng-pc19370.html', 'category': 'tráng miệng'}
    ]

    def parse(self, response):
        for i in range(len(self.categories)):
            link_page = self.categories[i]['link']
            request = Request(link_page, callback=self.parse_url, meta={'category': self.categories[i]['category']})
            yield request


    def parse_url(self, response):
        sel = Selector(response)
        category = response.meta['category']
        links = sel.xpath('//*[@id="main-content"]/div[1]/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div[1]/a/@href').extract()
        images = sel.xpath('//*[@id="main-content"]/div[1]/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div[1]/a/img/@src').extract()
        next = sel.xpath('//*[@id="yw0"]/li[@class="next"]/a/@href').extract()
        if next:
            request = Request(self.domain + next[0], callback=self.parse_url, meta={'category': category})
            yield request

        if links:
            for i in range(len(links)):
                product_link = self.domain + links[i]
                yield Request(product_link, callback=self.parse_product, meta={'category': category, 'image': images[i]})

    def parse_product(self, response):
        sel = Selector(response)
        category = response.meta['category']
        item = FoodMenuItem()
        item['category'] = category
        item['title'] = sel.xpath('//*[@id="main-content"]/div[1]/div/div/div/div/div[2]/div/div/div/section/div/div/div/div/div/div[2]/div[1]/h1/text()').extract()[0]
        item['image'] = response.meta['image']
        item['link'] = response.url
        item['price'] = sel.xpath('//*[@id="main-content"]/div[1]/div/div/div/div/div[2]/div/div/div/section/div/div/div/div/div/div[2]/div[2]/div/p/span[2]/text()').extract()[0].replace('  ','').replace('.','').replace('đ','')
        yield item
