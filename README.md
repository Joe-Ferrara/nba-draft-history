# NBA Draft History

Scripts to scrape NBA draft history and player statistics from basketball-reference.com, pipeline the scraped data into a MySQL relational database, and do analysis of the dataset.

Write-ups for the project: [NBA Draft History: The Aggregate Statistic](https://joe-ferrara.github.io/2020/06/28/nba-draft-history-1.html), [NBA Draft History: The Best and Worst Teams at Drafting](https://joe-ferrara.github.io/2020/06/30/nba-draft-history-2.html), and [NBA Draft History: Best Colleges at Producing NBA Players](https://joe-ferrara.github.io/2020/07/15/nba-draft-history-3.html).

------

``nba_draft_history``

Scrapy project directory to scrape NBA draft history from basketball-reference.com for the years 1949 - 2019. An example of the data scraped for a given year is the main table for the 2003 draft found at basketball-reference.com [here](https://www.basketball-reference.com/draft/NBA_2003.html).

``nba_draft_history/nba_draft_history/spiders/nba_draft_history_spider.py`` - contains the spider subclass that has the instructions to scrape the NBA draft history.

``nba_draft_history/pipelines.py`` - instructions to send the scraped data into a MySQL relational database I created on my computer (the files that created the relational database are in ``MySQL_management``, see below).

------

``fetch_player_urls``

Scrapy project directory that records the urls of the player pages on basketball-reference.com for all players drafted during the years 1967 - 2019 that played one season or more in the NBA. An example of a player page is the one for Lebron James, found [here](https://www.basketball-reference.com/players/j/jamesle01.html).

``fetch_player_urls/fetch_player_urls/spiders/fetch_player_urls_spider.py`` - contains the spider subclass that has the instructions to scrape the player urls.

``fetch_player_urls/fetch_player_urls/pipelines.py`` - instructions to send the scraped player urls into the text file ``fetch_player_urls/player_urls.txt``.

------

``player_stats``

Scrapy project directory that scrapes the per year statistics on basketball-reference.com from the player pages for all the players drafted during the years 1967 - 2019 that played one season or more in the NBA. The per year statistics are found in the table titled "Per Year" on a players player page.

``/player_stats/player_stats/spiders/play_stats_spider.py`` - contains the spider subclass that has the instructions to scrape the player statistics.

``/player_stats/player_stats/pipelines.py`` - instructions to send the scraped player statistics into MySQL relational database (same database as NBA draft history data is sent to).

------

``MySQL_management``

Scripts to create and maintaine a MySQL relational database for the above scraped data. MySQL Connector for Python was used to connect to a local server on my computer. The login information is removed from all files in this directory, and any other files in this project that connect to the database.

``MySQL_management/create_tables.py`` - creates the relational database for the project.

``MySQL_management/draft_day_trades_update.py`` - records any draft day trades that happened and updates the relational database. When a player is traded on draft day, basketball-reference.com records the original team that drafted the player in their draft history rather than the team the player ended up on. For my draft history analysis, I wanted to credit the team the player ended up on, on draft day as the team that drafted him. To determine when this happens, this script records when the draft team of a player is different than the team the player played his first season on. When this happens, the script prints the draft day trade to ``draft_day_trades_and_messed_up_stats.txt``, and changes the draft team of the player in the database to the team the player played his first season on. This script also catches when a player's per year stats are missing or messed up, and prints that player to the file ``draft_day_trades_and_messed_up_stats.txt``.

``MySQL_management/draft_day_trades_and_messed_up_stats.txt`` - contains all the draft day trades and players with missing or messed up statistics recorded by ``draft_day_trades.py``. Useful file to see where the above scraping went wrong. Two issues found: One, there are duplicate names of players (happens multiple times with father son duos) which was not accounted for in the relational database so these players' data is messed up. Two, basketball-reference.com records players being traded midseason in the per year statistics tables in a way that the above scraper did not handle well. A to do for the future is to fix these issues.

``manuel_updates.markdown`` - records manuel changes I made to the relational database while completing the project. While doing my analysis, I found some issues in the data that affected the analysis and manually corrected the data. These corrections are recorded here.

------

``five_year_period_analysis``

``five_year_period_analysis/create_and_save_agg_stat.py`` - creates and records the **Agg** stat used in my draft analysis write up. Writes a csv file with the players drafted in the top 60 picks from 1969 to 2013. The csv file has for each player, his names, his college, the team that drafted him, the year he was drafted, the pick number he was, and his **Agg** stat. The csv created is titled ``draft_hist_with_agg_stat.csv`` and is used in other scripts. Also saves a histogram of the **Agg** statistic.

``five_year_period_analysis/stats_functions.py`` - some functions used in ``create_and_save_agg_stat.py``.

``five_year_period_analysis/five_year_period_analysis.py`` - does NBA draft history analysis. Creates a list of every five year period of drafting for every team and every college. Using the **Agg** stat, orders the list to determine the best and worst five year periods of drafting NBA teams have done, as well as the best five year periods of NBA players colleges have produced.

------

``college_picks``

``college_picks/college_picks_each_year_since_67.py`` - records the top six colleges in terms of number of NBA players drafted since 1967. For each of the six colleges, creates a graph of the number of players drafted per year and saves the graph.

``college_picks/college_picks_top_teams_together.py`` - records the top six colleges in terms of number of NBA players drafted during the time periods 1967-1994, 1995-2019, and 1967-2019. For each time period graphs the total players drafted for each college over time and saves the graphs.

------

``general_draft_analysis``

``general_draft_analysis/draft_pick_aves_and_best_draft.py`` - determines the average Agg of each draft pick 1 - 60 over the years 1967 - 2015, and determines the draft years with the highest total Agg for all players drafted.

 ``general_draft_analysis/top_picks_by_AOA.py`` - produces a list of the top players drafted between 1967 and 2013 in terms of Agg over average (AOA).
