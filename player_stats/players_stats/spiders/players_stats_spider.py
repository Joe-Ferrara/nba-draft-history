import scrapy

class PlayerStatsSpider(scrapy.Spider):
    name = "player_stats"

    def start_requests(self):
        f = open('player_urls.txt', 'r')
        urls = []
        line = f.readline()
        while line != '':
            url = 'https://www.basketball-reference.com' + line[:-1]
            urls.append(url)
            line = f.readline()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title = response.css('title::text').getall()[0]
        # get name from title
        ind = 0
        while title[ind] != '|':
            ind += 1
        name = title[:ind-7]
        for row in response.xpath('//*[@class="row_summable sortable stats_table"]//tbody//tr'):
            yield {
                'name': name,
                'season': row.xpath('th//text()').extract_first(),
                'age': row.xpath('td[1]//text()').extract_first(),
                'team': row.xpath('td[2]//text()').extract_first(),
                'league': row.xpath('td[3]//text()').extract_first(),
                'games_played': row.xpath('td[5]//text()').extract_first(),
                'games_started': row.xpath('td[6]//text()').extract_first(),
                'minutes_per_game': row.xpath('td[7]//text()').extract_first(),
                'field_goals_made_per_game': row.xpath('td[8]//text()').extract_first(),
                'field_goals_attempted_per_game': row.xpath('td[9]//text()').extract_first(),
                'field_goal_percent': row.xpath('td[10]//text()').extract_first(),
                'three_pointers_made_per_game': row.xpath('td[11]//text()').extract_first(),
                'three_pointers_attempted_per_game': row.xpath('td[12]//text()').extract_first(),
                'three_point_percent': row.xpath('td[13]//text()').extract_first(),
                'two_pointers_made_per_game': row.xpath('td[14]//text()').extract_first(),
                'two_pointers_attempted_per_game': row.xpath('td[15]//text()').extract_first(),
                'two_point_percent': row.xpath('td[16]//text()').extract_first(),
                'effective_field_goal_percent': row.xpath('td[17]//text()').extract_first(),
                'free_throws_made_per_game': row.xpath('td[18]//text()').extract_first(),
                'free_throws_attempted_per_game': row.xpath('td[19]//text()').extract_first(),
                'free_throw_percent': row.xpath('td[20]//text()').extract_first(),
                'offensive_rebounds_per_game': row.xpath('td[21]//text()').extract_first(),
                'defensive_rebounds_per_game': row.xpath('td[22]//text()').extract_first(),
                'total_rebounds_per_game': row.xpath('td[23]//text()').extract_first(),
                'assists_per_game': row.xpath('td[24]//text()').extract_first(),
                'steals_per_game': row.xpath('td[25]//text()').extract_first(),
                'blocks_per_game': row.xpath('td[26]//text()').extract_first(),
                'turnovers_per_game': row.xpath('td[27]//text()').extract_first(),
                'personal_fouls_per_game': row.xpath('td[28]//text()').extract_first(),
                'points_per_game': row.xpath('td[29]//text()').extract_first()
            }
