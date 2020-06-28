import mysql.connector
from mysql.connector import errorcode
import matplotlib.pyplot as plt

from matplotlib import colors as mcolors

colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)

college_colors = {
                  'Kentucky':colors['midnightblue'],
                  'UCLA':colors['gold'],
                  'Duke':colors['blue'],
                  'UNC':colors['skyblue'],
                  'Kansas':colors['grey'],
                  'Arizona':colors['red']
                 }

# MySQL connection with user information removed
cnx = mysql.connector.connect(user=user, password=password, host='localhost', database='nba_history_and_stats')

print('opened connection')

cursor = cnx.cursor()

query = """
        SELECT College.college, COUNT(1) AS number_of_picks
        FROM Player JOIN College JOIN Pick JOIN Year
        ON Player.college_id = College.college_id AND Player.pick_id = Pick.pick_id
        AND Player.year_id = Year.year_id
        WHERE Year.year >= 1967 AND Pick.pick <= 60
        GROUP BY College.college
        HAVING COUNT(1) > 20
        ORDER BY number_of_picks DESC;
        """

cursor.execute(query)

colleges_table = cursor.fetchall()

plt.style.use('fivethirtyeight')
for i in range(1, 7):
    fig2, ax2 = plt.subplots(figsize=(13,8))
    college = (colleges_table[i][0],)
    query = """
            SELECT Year.year, COUNT(1) AS number_of_picks
            FROM Player JOIN College JOIN Pick JOIN Year
            ON Player.college_id = College.college_id AND Player.pick_id = Pick.pick_id AND Player.year_id = Year.year_id
            WHERE Year.year >= 1967 AND Pick.pick <= 60 AND College.college = %s
            GROUP BY College.college, Year.year
            ORDER BY Year.year ASC;
            """
    cursor.execute(query, college)

    picks = cursor.fetchall()

    # dictionary to keep picks per year
    num_picks = {}
    for year in range(1967, 2020):
        num_picks[year] = 0 # set each year to 0
    # use table to set years with nonzero number of picks
    for j in range(len(picks)):
        num_picks[picks[j][0]] = picks[j][1]

    # list that is total number of picks
    total_picks = []
    # list of years
    years = list(num_picks.keys())
    # list of picks per year
    num_picks = list(num_picks.values())
    # make the total number of picks list
    total = 0
    for j in range(len(years)):
        total += num_picks[j]
        total_picks.append(total)
    # plot total number of picks of ax1, all teams on this graph
    c = college_colors[college[0]]
    # plot the picks per year on ax2, one graph per team
    ax2.bar(years, num_picks, color = c)
    ax2.set_xlabel('Year')
    labels = []
    for i in range(len(years)):
        if i%5 == 0:
            labels.append(years[i])
        else:
            labels.append(None)
    plt.xticks(ticks=years, labels=labels, rotation=90)
    ax2.set_ylabel('Number of Picks')
    ax2.set_ylim([0, 6])
    ax2.set_title('Number of ' + college[0] + ' Picks Each Year')
    plt.tight_layout()
    fig2.savefig(college[0] + '_picks_per_year_since_1967_gap.png')

cursor.close()
cnx.close()

print('closed connection')
