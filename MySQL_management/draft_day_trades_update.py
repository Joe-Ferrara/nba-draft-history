import mysql.connector
from mysql.connector import errorcode

# MySQL connection with user information removed
cnx = mysql.connector.connect(user=user, password=password, host='localhost', database='nba_history_and_stats')

cursor = cnx.cursor()

query = """
        SELECT Player.player_id
        FROM Player JOIN Year
          ON Player.year_id = Year.year_id
        WHERE Player.years_played > 0
          AND Year.year >= 1967;
        """

cursor.execute(query)

players_table = cursor.fetchall()

players_missing_stats = []
num_trades = 0

print('**************************')
print('**** number of players: ' + str(len(players_table)))
print('**************************')
print('')

trades = {}

for i in range(len(players_table)):
    player_id = players_table[i][0]

    query = """
            SELECT Team.team_id
            FROM Player JOIN Team
              ON Player.team_id = Team.team_id
            WHERE Player.player_id = %s;
            """

    data = (player_id,)

    cursor.execute(query, data)

    draft_team_id = cursor.fetchall()[0][0]

    query = """
            SELECT Team.team_id
            FROM Per_Year_Stats
              JOIN Player
              JOIN Season
              JOIN Team
                ON Per_Year_Stats.player_id = Player.player_id
                  AND Per_Year_Stats.season_id = Season.season_id
                  AND Per_Year_Stats.team_id = Team.team_id
            WHERE Player.player_id = %s
            ORDER BY Season.season ASC
            LIMIT 1;
            """

    cursor.execute(query, data)

    try:
        first_year_team_id = cursor.fetchall()[0][0]
    except:
        first_year_team_id = draft_team_id
        query = """
                SELECT Player.name, Player.years_played
                FROM Player
                WHERE Player.player_id = %s;
                """
        data = (player_id,)
        cursor.execute(query, data)
        info = cursor.fetchall()[0]
        name = info[0]
        years_played = info[1]
        players_missing_stats.append([name, player_id, years_played])

    if draft_team_id != first_year_team_id:
        num_trades += 1
        # change team that drafted the player
        # to the team he played on during first year
        query = """
                UPDATE Player
                SET Player.team_id = %s
                WHERE Player.player_id = %s;
                """
        data = (first_year_team_id, player_id)
        cursor.execute(query, data)

        cnx.commit()

        query = """
                SELECT Player.name
                FROM Player
                WHERE Player.player_id = %s;
                """
        data = (player_id,)
        cursor.execute(query, data)
        name = cursor.fetchall()[0][0]
        query = """
                SELECT Team.team
                FROM Team
                WHERE Team.team_id = %s;
                """
        data = (draft_team_id,)
        cursor.execute(query, data)
        draft_team = cursor.fetchall()[0][0]
        query = """
                SELECT Team.team
                FROM Team
                WHERE Team.team_id = %s;
                """
        data = (first_year_team_id,)
        cursor.execute(query, data)
        first_year_team = cursor.fetchall()[0][0]
        query = """
                SELECT Year.year
                FROM Player JOIN Year
                  ON Player.year_id = Year.year_id
                WHERE Player.player_id = %s;
                """
        data = (player_id,)
        cursor.execute(query, data)
        year = cursor.fetchall()[0][0]
        trade = name +  ' traded from ' + draft_team + ' to ' + first_year_team + '.'
        try:
            trades[year].append(trade)
        except:
            trades[year] = [trade]

cursor.close()
cnx.close()

print('****************************')
print('number of trades: ' + str(num_trades))
print('****************************')

for year in trades.keys():
    print('Year: ' + str(year))
    for trade in trades[year]:
        print('  ' + trade)

print('*******************************************')
print('*******************************************')
print('Number of messed up: ' + str(len(players_missing_stats)))
print(' ')
for triple in players_missing_stats:
    print('Name: ' + triple[0])
    print('player_id:' + str(triple[1]))
    print('years played: ' + str(triple[2]))
    print(' ')
