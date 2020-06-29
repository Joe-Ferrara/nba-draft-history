# NBA Draft History

Scripts to scrape NBA draft history and player statistics from basketball-reference.com, pipeline the scraped data into a MySQL relational database, and do analysis of the dataset.

``nba_draft_history``

Scrapy project directory to scrape NBA draft history from basketball-reference.com for the years 1949 - 2019. An example of the data scraped for a given year is the main table for the 2003 draft found at basketball-reference.com [here](https://www.basketball-reference.com/draft/NBA_2003.html).

``nba_draft_history/nba_draft_history/spiders/nba_draft_history_spider.py`` is the spider file that does the scraping.

``nba_draft_history/pipelines.py`` pipelines the scraped data into a MySQL relational database I created on my computer (the files that created the relational database are in ``MySQL_management``, see below).

------

``fetch_player_urls``

Scrapy project directory that records the urls of the player pages on basketball-reference.com for all players drafted during the years 1967 - 2019 that played one season or more in the NBA. An example of a player page is the one for Lebron James, found [here](https://www.basketball-reference.com/players/j/jamesle01.html).

``fetch_player_urls/fetch_player_urls/spiders/fetch_player_urls_spider.py`` is the spider file that does the scraping of the player urls.

``fetch_player_urls/fetch_player_urls/pipelines.py`` pipelines the scraped player urls into the text file ``fetch_player_urls/player_urls.txt``.

------

``player_stats``

Scrapy project directory that scrapes the per year statistics on basketball-reference.com from the player pages for all the players drafted during the years 1967 - 2019 that played one season or more in the NBA.

------

``MySQL_management``

Explanation coming soon.

------

``five_year_period_analysis``

Explanation coming soon.

------

``college_picks``

Explanation coming soon.



