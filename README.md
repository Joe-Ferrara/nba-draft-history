# NBA Draft History

Scripts to scrape NBA draft history and player statistics from basketball-reference.com, pipeline the scraped data into a MySQL relational database, and do analysis of the dataset.

### nba_draft_history

Directory that is a Scrapy project to scrape NBA draft history from basketball-reference.com for the years 1949 - 2019. An example of the data scraped for a given year is the main table for the 2003 draft found at [basketball-reference.com/draft/NBA_2003.html](https://www.basketball-reference.com/draft/NBA_2003.html).




Scrapes the draft pages on basketball-reference.com for the years 1950 - 2019. Scrapes the per year statistics for each year in a player's career for any player drafter during the years 1967 - 2019 that played one or more years in the NBA.
