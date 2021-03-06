import scrapy
from datetime import datetime


class CommoditySpider(scrapy.Spider):
    name = 'commodity'
    allowed_domains = ['moneycontrol.com']

    def start_requests(self):
        start_urls = ['https://www.moneycontrol.com/commodity/']

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        mcx_commodities = response.xpath(
            "//ul/li[@id='comm_tab1']//table[@class='mctable1']/tbody/tr")

        for mcx_commodity in mcx_commodities:
            commodity = mcx_commodity.xpath(".//td/a/text()").extract_first()

            date = mcx_commodity.xpath(
                ".//td/a/div[@class='date']/text()").extract_first()
            date = datetime.strptime(date, '%d %b %Y').strftime('%Y-%m-%d')

            price = float(mcx_commodity.xpath(
                ".//td[2]/text()").extract_first().replace(',', ''))
            change = float(mcx_commodity.xpath(
                ".//td[3]/text()").extract_first().replace(',', ''))
            pc_change = float(mcx_commodity.xpath(
                ".//td[4]/text()").extract_first().replace(',', ''))

            yield {
                "commodity": commodity,
                "type": "MCX",
                "date": date,
                "price": price,
                "change": change,
                "pc_change": pc_change
            }

        ncdex_commodities = response.xpath(
            "//ul/li[@id='comm_tab2']//table[@class='mctable1']/tbody/tr")

        for ncdex_commodity in ncdex_commodities:
            commodity = ncdex_commodity.xpath(".//td/a/text()").extract_first()
            date = ncdex_commodity.xpath(
                ".//td/a/div[@class='date']/text()").extract_first()
            date = datetime.strptime(date, '%d %b %Y').strftime('%Y-%m-%d')

            price = float(ncdex_commodity.xpath(
                ".//td[2]/text()").extract_first().replace(',', ''))
            change = float(ncdex_commodity.xpath(
                ".//td[3]/text()").extract_first().replace(',', ''))
            pc_change = float(ncdex_commodity.xpath(
                ".//td[4]/text()").extract_first().replace(',', ''))

            yield {
                "commodity": commodity,
                "type": "NCDEX",
                "date": date,
                "price": price,
                "change": change,
                "pc_change": pc_change
            }
