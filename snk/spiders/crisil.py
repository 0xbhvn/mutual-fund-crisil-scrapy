import scrapy


class CrisilSpider(scrapy.Spider):
    name = 'crisil'
    allowed_domains = ['moneycontrol.com']

    def start_requests(self):
        start_urls = ['https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/index-fundsetfs.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/multi-cap-fund.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/large-cap-fund.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/large-and-mid-cap-fund.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/mid-cap-fund.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/small-cap-fund.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/elss.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/sectoralthematic.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/value-fund.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/focused-fund.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/dividend-yield-fund.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/contra-fund.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/aggressive-hybrid-fund.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/arbitrage-fund.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/dynamic-asset-allocation-or-balanced-advantage.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/equity-savings.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/fixed-maturity-plans-hybrid.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/conservative-hybrid-fund.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/multi-asset-allocation.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/capital-protection-funds.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/low-duration-fund.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/short-duration-fund.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/ultra-short-duration-fund.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/money-market-fund.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/floater-fund.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/corporate-bond-fund.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/credit-risk-fund.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/fixed-maturity-plans-debt.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/medium-duration-fund.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/dynamic-bond-fund.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/medium-to-long-duration-fund.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/gilt-fund.html',
                      'https://www.moneycontrol.com/mutual-funds/performance-tracker/returns/long-duration-fund.html']

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        funds = response.xpath(
            "/html/body/section[2]/div/div/div[2]/div/div[4]/div/table/tbody/tr")

        for fund in funds:
            fund_name = fund.xpath(".//td[1]/a/text()").get()
            crisil_rank = fund.xpath(".//td[4]/span/text()").get()

            if fund.xpath(".//td[4]/span/text()").get() == '-':
                crisil_rank = 0
            else:
                crisil_rank = int(fund.xpath(".//td[4]/span/text()").get())

            level_1_category = fund.xpath(
                "/html/body/section[1]/div/div/div[1]/div[1]/div/div/div[1]/h4/div[1]/div/ul/li[@class='tabactive active']/a/text()").get()
            level_2_category = fund.xpath(".//td[3]/text()").get()
            level_3_category = fund.xpath(".//td[2]/text()").get()

            yield {
                'fund_name': fund_name,
                'crisil_rank': crisil_rank,
                'level_1_category': level_1_category,
                'level_2_category': level_2_category,
                'level_3_category': level_3_category,
            }
