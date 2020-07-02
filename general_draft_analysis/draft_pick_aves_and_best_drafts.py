## list draft pick aves
## determine top 5 and bottom 5 drafts in terms of overall Agg

import pandas as pd

draft_hist = pd.read_csv('draft_hist_with_agg_stat.csv', index_col='name')

picks_gpby = draft_hist.groupby(['pick'])
ave_agg = {}
for pick, group in picks_gpby:
    ave_val = str(round(100*group['agg_stat'].mean())/100)
    if len(ave_val) == 3:
        ave_val += '0'
    ave_agg[pick] = ave_val

print('{:>4s}{:>8s}{:>5s}{:>8s}'.format('Pick', 'Ave Agg', 'Pick', 'Ave Agg'))
for i in range(1, 16):
    p1 = str(i)
    v1 = ave_agg[i]
    p2 = str(i + 15)
    v2 = ave_agg[i + 15]
    print('{:>4s}{:>8s}{:>5s}{:>8s}'.format(p1, v1, p2, v2))

year_gpby = draft_hist.groupby(['year'])

year_data = []

for year, picks in year_gpby:
    tot_val = picks['agg_stat'].sum()
    year_data.append([year, tot_val])

def sort_help(l):
    return l[1]

year_data.sort(key=sort_help)
print('')
print('********************************************')
print('Ranking from Best to Worst Drafts Since 1990')
print('********************************************')
print('')
count = 0
i = 0
while True:
    year = year_data[-i-1][0]
    score = str(round(100*year_data[-i-1][1])/100)
    if year < 1990:
        i += 1
        continue
    else:
        count += 1
        i += 1
    title = str(count) + '. ' + str(year)
    title += ', Score ' + score
    print(title)
    b = '  '
    s0 = 'Rk '
    s1 = 'Players (pick)'
    s2 = 'Agg'
    print('{:<2s}{:>4s}{:<30s}{:>4s}'.format(b, s0, s1, s2))
    picks = year_gpby.get_group(year)
    sorted = picks.sort_values(by='agg_stat', ascending = False)
    for j in range(14):
        player = sorted.index[j]
        pick = sorted['pick'].iloc[j]
        s = player + ' (' + str(pick) + ')'
        agg = str(round(100*sorted['agg_stat'].iloc[j])/100)
        if len(agg) == 3:
            agg += '0'
        r = str(j+1) + '. '
        print('{:<2s}{:>4s}{:<30s}{:>4s}'.format(b, r, s, agg))
    print('')
    if count == 24:
        break
