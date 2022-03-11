import scrapy
from datetime import datetime


class ForexSpider(scrapy.Spider):
    name = 'forex'
    allowed_domains = ['money.rediff.com']

    def start_requests(self):
        start_urls = ['https://money.rediff.com/tools/forex']

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        currencies = response.xpath(
            "/html/body/div[2]/div[5]/div[2]/div[2]/table/tbody/tr")

        for currency in currencies:
            cur_name = currency.xpath(".//td[1]/text()").get()
            cur_code = cur_name.split(
                ' ')[-1].replace('(', '').replace(')', '')
            cur_rate = float(currency.xpath(
                ".//td[@class='numericalColumn']/text()").get())

            yield {
                'cur_name': cur_name,
                'cur_code': cur_code,
                'cur_rate': cur_rate
            }
