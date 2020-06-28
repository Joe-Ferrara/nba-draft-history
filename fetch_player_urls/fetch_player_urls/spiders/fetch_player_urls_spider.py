import scrapy

class FetchPlayerUrlsSpider(scrapy.Spider):
    name = "fetch_player_urls"

    def start_requests(self):
        urls = []
        for i in range(1967, 2020):
            url = 'https://www.basketball-reference.com/draft/NBA_'
            url += str(i)
            url += '.html'
            urls.append(url)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for row in response.xpath('//*[@class="sortable stats_table"]//tbody//tr'):
            # if name is None, one of non-player rows
            if row.xpath('td[3]//text()').extract_first() == None:
                continue
            # if years is None, then did not play any years
            if row.xpath('td[5]//text()').extract_first() == None:
                continue
            yield {
                'name': row.xpath('td[3]//text()').extract_first(),
                'url': row.xpath('td[3]//a/@href').extract_first()
            }
