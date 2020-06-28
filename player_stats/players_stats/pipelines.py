# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector

class PlayersStatsPipeline(object):

    add_season = ("INSERT INTO Season "
                 "(season) "
                 "VALUES (%s)")

    add_league = ("INSERT INTO League "
                 "(league) "
                 "VALUES (%s)")

    add_per_year_stats = ("INSERT INTO Per_Year_Stats "
                             "(player_id,"
                             " season_id,"
                             " team_id,"
                             " league_id,"
                             " age,"
                             " games_played,"
                             " games_started,"
                             " minutes_per_game,"
                             " field_goals_made_per_game,"
                             " field_goals_attempted_per_game,"
                             " field_goal_percent,"
                             " three_pointers_made_per_game,"
                             " three_pointers_attempted_per_game,"
                             " three_point_percent,"
                             " two_pointers_made_per_game,"
                             " two_pointers_attempted_per_game,"
                             " two_point_percent,"
                             " effective_field_goal_percent,"
                             " free_throws_made_per_game,"
                             " free_throws_attempted_per_game,"
                             " free_throw_percent,"
                             " offensive_rebounds_per_game,"
                             " defensive_rebounds_per_game,"
                             " total_rebounds_per_game,"
                             " assists_per_game,"
                             " steals_per_game,"
                             " blocks_per_game,"
                             " turnovers_per_game,"
                             " personal_fouls_per_game,"
                             " points_per_game"
                             ") "
                             "VALUES (%(player_id)s,"
                             " %(season_id)s,"
                             " %(team_id)s,"
                             " %(league_id)s,"
                             " %(age)s,"
                             " %(games_played)s,"
                             " %(games_started)s,"
                             " %(minutes_per_game)s,"
                             " %(field_goals_made_per_game)s,"
                             " %(field_goals_attempted_per_game)s,"
                             " %(field_goal_percent)s,"
                             " %(three_pointers_made_per_game)s,"
                             " %(three_pointers_attempted_per_game)s,"
                             " %(three_point_percent)s,"
                             " %(two_pointers_made_per_game)s,"
                             " %(two_pointers_attempted_per_game)s,"
                             " %(two_point_percent)s,"
                             " %(effective_field_goal_percent)s,"
                             " %(free_throws_made_per_game)s,"
                             " %(free_throws_attempted_per_game)s,"
                             " %(free_throw_percent)s,"
                             " %(offensive_rebounds_per_game)s,"
                             " %(defensive_rebounds_per_game)s,"
                             " %(total_rebounds_per_game)s,"
                             " %(assists_per_game)s,"
                             " %(steals_per_game)s,"
                             " %(blocks_per_game)s,"
                             " %(turnovers_per_game)s,"
                             " %(personal_fouls_per_game)s,"
                             " %(points_per_game)s"
                             ")")

    def open_spider(self, spider):
        # MySQL connection with user information removed
        cnx = mysql.connector.connect(user=user, password=password, host='localhost', database='nba_history_and_stats')
        self.cursor = self.cnx.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.cnx.close()

    def process_item(self, item, spider):
        # retreive player_id
        query = ("SELECT player_id FROM Player WHERE name = %s")
        self.cursor.execute(query, (item['name'],))
        player_id = self.cursor.fetchall()[0][0]
        # retreive team_id
        query = ("SELECT team_id FROM Team WHERE team = %s")
        self.cursor.execute(query, (item['team'],))
        team_id = self.cursor.fetchall()[0][0]
        try: # try to retreive season_id
            query = ("SELECT season_id FROM Season WHERE season = %s")
            self.cursor.execute(query, (item['season'],))
            season_id = self.cursor.fetchall()[0][0]
        except:
            data_season = (item['season'],)
            self.cursor.execute(self.add_season, data_season)
            season_id = self.cursor.lastrowid
        try: # try to retreive league_id
            query = ("SELECT league_id FROM League WHERE league = %s")
            self.cursor.execute(query, (item['league'],))
            league_id = self.cursor.fetchall()[0][0]
        except:
            data_league = (item['league'],)
            self.cursor.execute(self.add_league, data_league)
            league_id = self.cursor.lastrowid

        data_per_year_stats = {'player_id':player_id,
                               'season_id':season_id,
                               'team_id':team_id,
                               'league_id':league_id,
                               'age':int(item['age']),
                               'games_played':int(item['games_played']),
                               'games_started':int(item['games_started']),
                               'minutes_per_game':float(item['minutes_per_game']),
                               'field_goals_made_per_game':float(item['field_goals_made_per_game']),
                               'field_goals_attempted_per_game':float(item['field_goals_attempted_per_game']),
                               'field_goal_percent':float(item['field_goal_percent']),
                               'three_pointers_made_per_game':float(item['three_pointers_made_per_game']),
                               'three_pointers_attempted_per_game':float(item['three_pointers_attempted_per_game']),
                               'three_point_percent':float(item['three_point_percent']),
                               'two_pointers_made_per_game':float(item['two_pointers_made_per_game']),
                               'two_pointers_attempted_per_game':float(item['two_pointers_attempted_per_game']),
                               'two_point_percent':float(item['two_point_percent']),
                               'effective_field_goal_percent':float(item['effective_field_goal_percent']),
                               'free_throws_made_per_game':float(item['free_throws_made_per_game']),
                               'free_throws_attempted_per_game':float(item['free_throws_attempted_per_game']),
                               'free_throw_percent':float(item['free_throw_percent']),
                               'offensive_rebounds_per_game':float(item['offensive_rebounds_per_game']),
                               'defensive_rebounds_per_game':float(item['defensive_rebounds_per_game']),
                               'total_rebounds_per_game':float(item['total_rebounds_per_game']),
                               'assists_per_game':float(item['assists_per_game']),
                               'steals_per_game':float(item['steals_per_game']),
                               'blocks_per_game':float(item['blocks_per_game']),
                               'turnovers_per_game':float(item['turnovers_per_game']),
                               'personal_fouls_per_game':float(item['personal_fouls_per_game']),
                               'points_per_game':float(item['points_per_game'])
                              }
        self.cursor.execute(self.add_per_year_stats, data_per_year_stats)
        self.cnx.commit()

        return item
