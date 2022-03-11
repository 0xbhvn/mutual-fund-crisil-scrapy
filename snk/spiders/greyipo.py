import scrapy


class GreyipoSpider(scrapy.Spider):
    name = 'greyipo'
    allowed_domains = ['ipowatch.com']

    def start_requests(self):
        start_urls = [
            'https://www.ipowatch.in/p/ipo-grey-market-premium-latest-ipo-grey.html']

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        ipos_gmp = response.xpath(
            "//div[@id='post-toc']/div/div/table[1]/tbody/tr")
        ipos_kostak_sauda = response.xpath(
            "//div[@id='post-toc']/div/div/table[2]/tbody/tr")
        all_prices = zip(ipos_gmp, ipos_kostak_sauda)

        for i, (gmp, ks) in enumerate(zip(ipos_gmp, ipos_kostak_sauda)):
            try:
                ipo_name = gmp.xpath(".//td[1]/a/text()").extract_first()
                gmp_price = gmp.xpath(".//td[2]/b/span/text()").extract_first()
                if gmp_price[0] == '-':
                    gmp_price = gmp_price[0] + gmp_price[2:]
                else:
                    gmp_price = gmp_price[1:]

                if gmp_price == '-':
                    gmp_price = 0
                else:
                    gmp_price = int(gmp_price)

                kostak_price = ks.xpath(".//td[2]/b/text()").extract_first()
                if kostak_price[0] == '-':
                    kostak_price = kostak_price[0] + kostak_price[2:]
                else:
                    kostak_price = kostak_price[1:]

                if kostak_price == '-':
                    kostak_price = 0
                else:
                    kostak_price = int(kostak_price)

                sauda_price = ks.xpath(".//td[3]/b/text()").extract_first()
                if sauda_price[0] == '-':
                    sauda_price = sauda_price[0] + sauda_price[2:]
                else:
                    sauda_price = sauda_price[1:]

                if sauda_price == '-':
                    sauda_price = 0
                else:
                    sauda_price = int(sauda_price)

                yield {
                    'ipo_name': ipo_name,
                    'gmp_price': gmp_price,
                    'kostak_price': kostak_price,
                    'sauda_price': sauda_price
                }
            except Exception as e:
                print(e)
