import pandas as pd

draft_hist = pd.read_csv('draft_hist_with_agg_stat.csv', index_col='name')

five_year_starts = [i for i in range(1969, 2010)]

# college analysis

college_gpby = draft_hist.groupby(['college'])

college_data = [] # lists of lists
# entry in agg_data is [college - year, sum of agg_stats of picks, [picks]]

for college, pick_hist in college_gpby:
    if college == 'None':
        continue
    for start_year in five_year_starts:
        data = [college + ' - ' + str(start_year), 0.0, []]
        for i in range(pick_hist.shape[0]):
            year = pick_hist['year'].iloc[i]
            if year >= start_year and year <= start_year + 4:
                agg_stat = pick_hist['agg_stat'].iloc[i]
                pick_num = pick_hist['pick'].iloc[i]
                data[1] += agg_stat
                data[2].append([pick_hist.index[i], agg_stat, pick_num, year])
        college_data.append(data)

def sort_helper(l):
    return l[1]

college_data.sort(key=sort_helper)
for i in range(1, 21):
    print(str(i) + '. College: ' + str(college_data[-i][0]))
    print('   Score: ' + str(college_data[-i][1]))
    college_data[-i][2].sort(key=sort_helper, reverse=True)
    s0 = '    '
    s1 = 'Players (year, pick)'
    s3 = 'AggStatScore'
    print('{:<4s}{:<30s}{:>12s}'.format(s0, s1, s3))
    for j in range(len(college_data[-i][2])):
        name = college_data[-i][2][j][0]
        stat = str(round(100*college_data[-i][2][j][1])/100)
        pick = str(college_data[-i][2][j][2])
        year = str(college_data[-i][2][j][3])
        name = name + ' (' + year + ', ' + pick + ')'
        print('{:<4s}{:<30s}{:>12s}'.format(s0, name, stat))
    print('')

# do analysis adjusting for average value of the pick

new_col = [0.0]*draft_hist.shape[0]
new_col = {'ave_value':new_col}
names = list(draft_hist.index)
new_col = pd.DataFrame(new_col, index=names)
draft_hist = pd.concat([draft_hist, new_col], axis=1)
new_col = [0.0]*draft_hist.shape[0]
new_col = {'val_above_ave':new_col}
names = list(draft_hist.index)
new_col = pd.DataFrame(new_col, index=names)
draft_hist = pd.concat([draft_hist, new_col], axis=1)

picks_gpby = draft_hist.groupby(['pick'])
for pick, group in picks_gpby:
    ave_val = group['agg_stat'].mean()
    for i in range(group.shape[0]):
        val_above_ave = group['agg_stat'].iloc[i] - ave_val
        ind = group.index[i]
        draft_hist.at[ind, 'ave_value'] = ave_val
        draft_hist.at[ind, 'val_above_ave'] = val_above_ave

# team analysis adjusted

team_gpby = draft_hist.groupby(['team'])

team_data = [] # lists of lists
# entry in agg_data is [team - year, sum of agg_stats of picks, [picks]]

for team, pick_hist in team_gpby:
    for start_year in five_year_starts:
        data = [team + ' - ' + str(start_year), 0.0, []]
        for i in range(pick_hist.shape[0]):
            year = pick_hist['year'].iloc[i]
            if year >= start_year and year <= start_year + 4:
                stat_val = pick_hist['val_above_ave'].iloc[i]
                pick_num = pick_hist['pick'].iloc[i]
                data[1] += stat_val
                data[2].append([pick_hist.index[i], stat_val, pick_num, year])
        team_data.append(data)

print('*************************************')
print('BEST TEAMS AT DRAFTING')
print('*************************************')


team_data.sort(key=sort_helper)
for i in range(1, 35):
    print(str(i) + '. Team: ' + str(team_data[-i][0]))
    print('   Score: ' + str(team_data[-i][1]))
    team_data[-i][2].sort(key=sort_helper, reverse=True)
    s0 = '    '
    s1 = 'Players (year, pick)'
    s3 = 'ValOverAve'
    print('{:<4s}{:<30s}{:>12s}'.format(s0, s1, s3))
    for j in range(len(team_data[-i][2])):
        name = team_data[-i][2][j][0]
        stat = str(round(100*team_data[-i][2][j][1])/100)
        pick = str(team_data[-i][2][j][2])
        year = str(team_data[-i][2][j][3])
        name = name + ' (' + year + ', ' + pick + ')'
        print('{:<4s}{:<30s}{:>12s}'.format(s0, name, stat))
    print('')

print('*************************************')
print('*************************************')
print('')
print('*************************************')
print('WORST TEAMS AT DRAFTING')
print('*************************************')
#######################################
## NEED TO MAKE THIS ONLY SINCE 1990 ##
########################################

# for worst teams only use the lottery era

team_data = [] # lists of lists
# entry in agg_data is [team - year, sum of agg_stats of picks, [picks]]

five_year_starts = [i for i in range(1990, 2010)]

for team, pick_hist in team_gpby:
    for start_year in five_year_starts:
        data = [team + ' - ' + str(start_year), 0.0, []]
        for i in range(pick_hist.shape[0]):
            year = pick_hist['year'].iloc[i]
            if year >= start_year and year <= start_year + 4:
                stat_val = pick_hist['val_above_ave'].iloc[i]
                pick_num = pick_hist['pick'].iloc[i]
                data[1] += stat_val
                data[2].append([pick_hist.index[i], stat_val, pick_num, year])
        team_data.append(data)

team_data.sort(key=sort_helper)
for i in range(0, 34):
    print(str(i) + '. Team: ' + str(team_data[i][0]))
    print('   Score: ' + str(team_data[i][1]))
    team_data[i][2].sort(key=sort_helper)
    s0 = '    '
    s1 = 'Players (year, pick)'
    s3 = 'ValOverAve'
    print('{:<4s}{:<30s}{:>12s}'.format(s0, s1, s3))
    for j in range(len(team_data[i][2])):
        name = team_data[i][2][j][0]
        stat = str(round(100*team_data[i][2][j][1])/100)
        pick = str(team_data[i][2][j][2])
        year = str(team_data[i][2][j][3])
        name = name + ' (' + year + ', ' + pick + ')'
        print('{:<4s}{:<30s}{:>12s}'.format(s0, name, stat))
    print('')
