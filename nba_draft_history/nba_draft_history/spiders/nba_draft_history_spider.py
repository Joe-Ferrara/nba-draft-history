import scrapy

class NbaDraftHistorySpider(scrapy.Spider):
    name = "nba_draft_history"

    terr_years = ['1949',
                  '1950',
                  '1951',
                  '1952',
                  '1953',
                  '1955',
                  '1956',
                  '1958',
                  '1959',
                  '1962',
                  '1963',
                  '1964',
                  '1965']

    def start_requests(self):
        urls = []
        for i in range(73):
            year = 2019 - i
            url = 'https://www.basketball-reference.com/draft/NBA_'
            url += str(year)
            url += '.html'
            urls.append(url)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        year = response.css('title::text').getall()[0][0:4]
        if year in self.terr_years:
            round = '0'
        else:
            round = '1'
        step = 0
        for row in response.xpath('//*[@class="sortable stats_table"]//tbody//tr'):
            if row.xpath('td[2]//text()').extract_first() == None:
                if step == 0:
                    step += 1
                else:
                    step = 0
                    round = str(int(round) + 1)
                continue
            yield {
                'round': round,
                'year': year,
                'pick': row.xpath('td[1]//text()').extract_first(),
                'team': row.xpath('td[2]//text()').extract_first(),
                'name': row.xpath('td[3]//text()').extract_first(),
                'college': row.xpath('td[4]//text()').extract_first(),
                'years_played': row.xpath('td[5]//text()').extract_first(),
                'games_played': row.xpath('td[6]//text()').extract_first(),
                'minutes_played': row.xpath('td[7]//text()').extract_first(),
                'points_total': row.xpath('td[8]//text()').extract_first(),
                'rebounds_total': row.xpath('td[9]//text()').extract_first(),
                'assists_total': row.xpath('td[10]//text()').extract_first(),
                'field_goal_percent': row.xpath('td[11]//text()').extract_first(),
                'three_point_percent': row.xpath('td[12]//text()').extract_first(),
                'free_throw_percent': row.xpath('td[13]//text()').extract_first(),
                'min_per_game': row.xpath('td[14]//text()').extract_first(),
                'points_per_game': row.xpath('td[15]//text()').extract_first(),
                'rebounds_per_game': row.xpath('td[16]//text()').extract_first(),
                'assists_per_game': row.xpath('td[17]//text()').extract_first(),
                'win_shares': row.xpath('td[18]//text()').extract_first(),
                'win_shares_per_48': row.xpath('td[19]//text()').extract_first(),
                'box_score_plus_minus': row.xpath('td[20]//text()').extract_first(),
                'value_over_replacement': row.xpath('td[21]//text()').extract_first()
            }
