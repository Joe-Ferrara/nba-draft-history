# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector

class NbaDraftHistoryPipeline(object):

    add_team = ("INSERT INTO Team "
               "(team) "
               "VALUES (%s)")

    add_year = ("INSERT INTO Year "
               "(year) "
               "VALUES (%s)")

    add_round = ("INSERT INTO Round "
                "(round) "
                "VALUES (%s)")

    add_college = ("INSERT INTO College "
                  "(college) "
                  "VALUES (%s)")

    add_pick = ("INSERT INTO Pick "
               "(pick) "
               "VALUES (%s)")

    add_player = ("INSERT INTO Player "
                 "(name,"
                 " team_id,"
                 " year_id,"
                 " round_id,"
                 " college_id,"
                 " pick_id,"
                 " years_played,"
                 " games_played,"
                 " minutes_played,"
                 " points_total,"
                 " rebounds_total,"
                 " assists_total,"
                 " field_goal_percent,"
                 " three_point_percent,"
                 " min_per_game,"
                 " points_per_game,"
                 " rebounds_per_game,"
                 " assists_per_game,"
                 " win_shares,"
                 " win_shares_per_48,"
                 " box_score_plus_minus,"
                 " value_over_replacement"
                 ") "
                 "VALUES (%(name)s,"
                 " %(team_id)s,"
                 " %(year_id)s,"
                 " %(round_id)s,"
                 " %(college_id)s,"
                 " %(pick_id)s,"
                 " %(years_played)s,"
                 " %(games_played)s,"
                 " %(minutes_played)s,"
                 " %(points_total)s,"
                 " %(rebounds_total)s,"
                 " %(assists_total)s,"
                 " %(field_goal_percent)s,"
                 " %(three_point_percent)s,"
                 " %(min_per_game)s,"
                 " %(points_per_game)s,"
                 " %(rebounds_per_game)s,"
                 " %(assists_per_game)s,"
                 " %(win_shares)s,"
                 " %(win_shares_per_48)s,"
                 " %(box_score_plus_minus)s,"
                 " %(value_over_replacement)s"
                 ")")

    def open_spider(self, spider):
        self.cnx = mysql.connector.connect(user='jferrara', password='kr3EZ@7lR1', host='localhost', database='nba_draft_history')
        self.cursor = self.cnx.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.cnx.close()

    def process_item(self, item, spider):
        try: # try to retreive team_id
            query = ("SELECT team_id FROM Team WHERE team = %s")
            self.cursor.execute(query, (item['team'],))
            team_id = self.cursor.fetchall()[0][0]
        except:
            data_team = (item['team'],)
            self.cursor.execute(self.add_team, data_team)
            team_id = self.cursor.lastrowid
        try: # try to retreive year_id
            query = ("SELECT year_id FROM Year WHERE year = %s")
            self.cursor.execute(query, (int(item['year']),))
            year_id = self.cursor.fetchall()[0][0]
        except:
            data_year = (int(item['year']),)
            self.cursor.execute(self.add_year, data_year)
            year_id = self.cursor.lastrowid
        try: # try to retreive round_id
            query = ("SELECT round_id FROM Round WHERE round = %s")
            self.cursor.execute(query, (int(item['round']),))
            round_id = self.cursor.fetchall()[0][0]
        except:
            data_round = (int(item['round']),)
            self.cursor.execute(self.add_round, data_round)
            round_id = self.cursor.lastrowid
        # college may by None
        if item['college'] == None:
            item['college'] = 'None'
        try: # try to retreive college_id
            query = ("SELECT college_id FROM College WHERE college = %s")
            self.cursor.execute(query, (item['college'],))
            college_id = self.cursor.fetchall()[0][0]
        except:
            data_college = (item['college'],)
            self.cursor.execute(self.add_college, data_college)
            college_id = self.cursor.lastrowid
        if item['pick'] == None: # territorial picks
            item['pick'] = int(0)
        try: # try to retreive the pick_id
            query = ("SELECT pick_id FROM Pick WHERE pick = %s")
            self.cursor.execute(query, (int(item['pick']),))
            pick_id = self.cursor.fetchall()[0][0]
        except:
            data_pick = (int(item['pick']),)
            self.cursor.execute(self.add_pick, data_pick)
            pick_id = self.cursor.lastrowid

        # deal with the None values in item
        for x in item.keys():
            if item[x] == None:
                item[x] = '0'

        data_player = {'name':item['name'],
                       'team_id':team_id,
                       'year_id':year_id,
                       'round_id':round_id,
                       'college_id':college_id,
                       'pick_id':pick_id,
                       'years_played':int(item['years_played']),
                       'games_played':int(item['games_played']),
                       'minutes_played':int(item['minutes_played']),
                       'points_total':int(item['points_total']),
                       'rebounds_total':int(item['rebounds_total']),
                       'assists_total':int(item['assists_total']),
                       'field_goal_percent':float(item['field_goal_percent']),
                       'three_point_percent':float(item['three_point_percent']),
                       'min_per_game':float(item['min_per_game']),
                       'points_per_game':float(item['points_per_game']),
                       'rebounds_per_game':float(item['rebounds_per_game']),
                       'assists_per_game':float(item['assists_per_game']),
                       'win_shares':float(item['win_shares']),
                       'win_shares_per_48':float(item['win_shares_per_48']),
                       'box_score_plus_minus':float(item['box_score_plus_minus']),
                       'value_over_replacement':float(item['value_over_replacement'])
                      }
        self.cursor.execute(self.add_player, data_player)
        self.cnx.commit()

        return item
