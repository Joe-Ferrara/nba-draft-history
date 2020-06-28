import mysql.connector
from mysql.connector import errorcode
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
exec(open('stats_functions.py').read())


# MySQL connection with user information removed
cnx = mysql.connector.connect(user=user, password=password, host='localhost', database='nba_history_and_stats')

cursor = cnx.cursor()

query = """
        SELECT Player.name,
          Player.years_played,
          Player.games_played,
          Player.minutes_played,
          Player.win_shares,
          Player.win_shares_per_48,
          Player.box_score_plus_minus,
          Player.value_over_replacement,
          Year.year,
          Pick.pick,
          College.college,
          Team.team
        FROM Player JOIN Year JOIN Pick JOIN College JOIN Team
        ON Player.year_id = Year.year_id
          AND Player.pick_id = Pick.pick_id
          AND Player.college_id = College.college_id
          AND Player.team_id = Team.team_id
        WHERE Year.year >= 1967 AND Year.year <= 2017 AND Pick.pick <= 60;
        """

draft_hist = pd.read_sql(query, cnx, index_col = 'name')

cursor.close()
cnx.close()


# set aside rows of players with less that 100 games played
not_enough_games = []
enough_games = []
for i in range(draft_hist.shape[0]):
    if draft_hist['games_played'].iloc[i] <= 100:
        not_enough_games.append(i)
    else:
        enough_games.append(i)

not_enough_games_players = draft_hist.iloc[not_enough_games]

rel_draft_hist = draft_hist.iloc[enough_games]

# make games per year stat

games_per_year = rel_draft_hist['games_played']/(rel_draft_hist['years_played'])

games_per_year.name = 'games_per_year'

rel_draft_hist = pd.concat([rel_draft_hist, games_per_year], axis=1)

cols_to_scale = ['years_played',
                 'games_played',
                 'minutes_played',
                 'games_per_year',
                 'win_shares',
                 'win_shares_per_48',
                 'box_score_plus_minus',
                 'value_over_replacement']

X = rel_draft_hist[cols_to_scale]

min_max_scaler = MinMaxScaler()

min_max_scaler.fit(X)
X_scaled = min_max_scaler.transform(X)

weights = [1/4, 1/4, 1/4, 1/4, 9/4, 9/4, 9/4, 9/4]

names = list(rel_draft_hist.index)

agg_stat_col = agg_stat(X_scaled, weights)
agg_stat_col = pd.DataFrame({'agg_stat':agg_stat_col}, index=names)

scaled_cols = {}
for i in range(len(cols_to_scale)):
    scaled_cols[cols_to_scale[i]] = X_scaled[:,i]
scaled_cols = pd.DataFrame(scaled_cols, index=names)

normalized_stats = pd.concat([agg_stat_col, scaled_cols], axis=1)

agg_stat_1_series = normalized_stats['agg_stat']


#########################
# five year normalizing #
#########################

for col in cols_to_scale:
    rel_draft_hist = five_year_scaling(rel_draft_hist, col, col + '_adv')

# drop years before 1969 and after 2013
rows_to_keep = []
for i in range(rel_draft_hist.shape[0]):
    year = rel_draft_hist['year'].iloc[i]
    if year >= 1969 and year <= 2013:
        rows_to_keep.append(i)

rel_draft_hist = rel_draft_hist.iloc[rows_to_keep]

adv_cols = [x + '_adv' for x in cols_to_scale]

X_scaled = rel_draft_hist[adv_cols].to_numpy()

weights = [1/4, 1/4, 1/4, 1/4, 9/4, 9/4, 9/4, 9/4]

names = list(rel_draft_hist.index)

agg_stat_col = agg_stat(X_scaled, weights)
agg_stat_col = pd.DataFrame({'agg_stat':agg_stat_col}, index=names)

rel_draft_hist = pd.concat([rel_draft_hist, agg_stat_col], axis=1)

agg_stat_1_series = agg_stat_1_series.iloc[rows_to_keep]
agg_stat_2_series = rel_draft_hist['agg_stat']

print(len(agg_stat_1_series))
print(len(agg_stat_2_series))

agg_stat_3_series = (agg_stat_1_series + agg_stat_2_series)/2

print('all years')
print(agg_stat_1_series.sort_values(ascending=False).head(20))
print('')
print('normalized for 5 years')
print(agg_stat_2_series.sort_values(ascending=False).head(20))
print('')
print('average of the two')
print(agg_stat_3_series.sort_values(ascending=False).head(20))
print(agg_stat_3_series.sort_values(ascending=False).tail(10))
print('')

max_1 = agg_stat_1_series.max()
min_1 = agg_stat_1_series.min()
agg_stat_1_series_norm = 10*(agg_stat_1_series - min_1)/(max_1 - min_1)

max_2 = agg_stat_2_series.max()
min_2 = agg_stat_2_series.min()
agg_stat_2_series_norm = 10*(agg_stat_2_series - min_2)/(max_2 - min_2)
print('normalize then average')
agg_stat_4_series = (agg_stat_1_series_norm + agg_stat_2_series_norm)/2
print(agg_stat_4_series.sort_values(ascending=False).head(20))
print(agg_stat_4_series.sort_values(ascending=False).tail(10))
# put back in bad players

rows_to_keep = []
for i in range(not_enough_games_players.shape[0]):
    year = not_enough_games_players['year'].iloc[i]
    if year >= 1969 and year <= 2013:
        rows_to_keep.append(i)

not_enough_games_players = not_enough_games_players.iloc[rows_to_keep]

# make agg_stat column for these player
new_col = [1.0]*not_enough_games_players.shape[0]
new_col = {'agg_stat':new_col}
ind = list(not_enough_games_players.index)
new_col = pd.DataFrame(new_col, index = ind)
busts_draft_hist = pd.concat([not_enough_games_players, new_col], axis=1)
busts_draft_hist = busts_draft_hist[['pick', 'year', 'college', 'team', 'agg_stat']]

print(not_enough_games_players.head(10))
print(rel_draft_hist.head(10))

rel_draft_hist = rel_draft_hist[['pick', 'year', 'college', 'team']]
agg_stat_4_df = agg_stat_4_series.to_frame(name = 'agg_stat')
rel_draft_hist = pd.concat([rel_draft_hist, agg_stat_4_df], axis=1)

print(rel_draft_hist.columns)
print(busts_draft_hist.columns)

draft_hist = pd.concat([rel_draft_hist, busts_draft_hist], axis=0)
print(draft_hist.shape[0])
print(draft_hist.head(10))
print(draft_hist.tail(10))
print(rel_draft_hist.shape)
print(busts_draft_hist.shape)

# fig = plt.figure()
# rel_draft_hist['agg_stat'].hist(bins = 100)
# print('Mean: ' + str(rel_draft_hist['agg_stat'].mean()))
# print('Std Dev: ' + str(rel_draft_hist['agg_stat'].std()))
# print(rel_draft_hist['agg_stat'].describe(percentiles = [0.01, 0.015, 0.02, 0.03, 0.04, 0.05, 0.1, # 0.25, 0.5, 0.75, 0.9, 0.95, 0.99, 0.999]))
# fig.savefig('agg_stat_3_hist.png')

fig = plt.figure()
agg_stat_3_series.hist(bins = 100)
print(agg_stat_3_series.describe(percentiles = [0.01, 0.015, 0.02, 0.03, 0.04, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99, 0.999]))
fig.savefig('agg_stat_3_hist.png')

fig = plt.figure()
agg_stat_4_series.hist(bins = 100)
print(agg_stat_4_series.describe(percentiles = [0.01, 0.015, 0.02, 0.03, 0.04, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99, 0.999]))
fig.savefig('agg_stat_4_hist.png')

print(draft_hist.shape)
draft_hist.to_csv('draft_hist_with_agg_stat.csv')
