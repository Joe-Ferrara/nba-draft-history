import pandas as pd

draft_hist = pd.read_csv('draft_hist_with_agg_stat.csv', index_col='name')

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

sorted = draft_hist.sort_values(by = 'val_above_ave', ascending = False)
print('Best Picks By AOA')
print('{:>4s}{:<35s}{:>5s}'.format('Rk ', 'Player (pick, team)', 'AOA'))
for i in range(20):
    r = str(i + 1) + '. '
    pick = str(sorted['pick'].iloc[i])
    t = sorted['team'].iloc[i]
    p = sorted.index[i] + ' (' + pick + ', ' + t + ')'
    s = str(round(100*sorted['val_above_ave'].iloc[i])/100)
    if len(s) < 4:
        s += '0'
    print('{:>4s}{:<35s}{:>5s}'.format(r, p, s))
print('')
print('Worst Picks By AOA')
sorted = draft_hist.sort_values(by = 'val_above_ave')
print('{:>4s}{:<35s}{:>5s}'.format('Rk ', 'Player (pick, team)', 'AOA'))
for i in range(20):
    r = str(i + 1) + '. '
    pick = str(sorted['pick'].iloc[i])
    t = sorted['team'].iloc[i]
    p = sorted.index[i] + ' (' + pick + ', ' + t + ')'
    s = str(round(100*sorted['val_above_ave'].iloc[i])/100)
    if len(s) < 4:
        s += '0'
    print('{:>4s}{:<35s}{:>5s}'.format(r, p, s))
print('')
print('')
print('Worst Picks By AOA Since 1990')
sorted = draft_hist.sort_values(by = 'val_above_ave')
print('{:>4s}{:<35s}{:>5s}'.format('Rk ', 'Player (pick, team)', 'AOA'))
count = 0
i = 0
while count < 20:
    if sorted['year'].iloc[i] < 1990:
        i += 1
        continue
    else:
        count += 1
    r = str(count) + '. '
    pick = str(sorted['pick'].iloc[i])
    t = sorted['team'].iloc[i]
    p = sorted.index[i] + ' (' + pick + ', ' + t + ')'
    s = str(round(100*sorted['val_above_ave'].iloc[i])/100)
    if len(s) < 4:
        s += '0'
    print('{:>4s}{:<35s}{:>5s}'.format(r, p, s))
    i += 1
