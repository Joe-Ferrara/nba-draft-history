

def agg_stat(stats_array, column_wts):
    """Returns a column vector that is the weighted sum of the columns of stats_array."""
    res = stats_array[:,0]*column_wts[0]
    for i in range(1, len(column_wts)):
        res += stats_array[:,i]*column_wts[i]
    return res

def five_year_scaling(draft_hist, old_col_name, new_col_name):
    """Scale old_col_name by five year max, and put in new_col_name.

    Returns draft_hist with the new column appended."""
    # make new column
    new_col = {new_col_name:[0.0]*draft_hist.shape[0]}
    names = list(draft_hist.index)
    new_col = pd.DataFrame(new_col, index = names)
    # append new column to draft_hist
    draft_hist = pd.concat([draft_hist, new_col], axis=1)
    # groupby by years and iterate through years
    draft_hist_gpby = draft_hist.groupby(['year'])
    for year, draft in draft_hist_gpby:
        if year < 1969 or year > 2013: # then not enough data
            continue
        else: # use 5 drafts
            drafts = draft_hist_gpby.get_group(year-2)
            for j in range(year-1, year+3):
                new_draft = draft_hist_gpby.get_group(j)
                drafts = pd.concat([drafts, new_draft], axis=0)
            max_val = drafts[old_col_name].max()
            min_val = drafts[old_col_name].min()
            for i in range(draft.shape[0]):
                ind = draft.index[i]
                val = draft[old_col_name].iloc[i]
                scaled_val = (val - min_val)/(max_val - min_val)
                draft_hist.at[ind, new_col_name] = scaled_val
    return draft_hist

def seven_year_scaling(draft_hist, old_col_name, new_col_name):
    """Scale old_col_name by five year max, and put in new_col_name.

    Returns draft_hist with the new column appended."""
    # make new column
    new_col = {new_col_name:[0.0]*draft_hist.shape[0]}
    names = list(draft_hist.index)
    new_col = pd.DataFrame(new_col, index = names)
    # append new column to draft_hist
    draft_hist = pd.concat([draft_hist, new_col], axis=1)
    # groupby by years and iterate through years
    draft_hist_gpby = draft_hist.groupby(['year'])
    for year, draft in draft_hist_gpby:
        if year < 1969 or year > 2013: # then not enough data
            continue
        elif year == 1969 or year == 2013: # use 5 drafts
            drafts = draft_hist_gpby.get_group(year-2)
            for j in range(year-1, year+3):
                new_draft = draft_hist_gpby.get_group(j)
                drafts = pd.concat([drafts, new_draft], axis=0)
            max_val = drafts[old_col_name].max()
            min_val = drafts[old_col_name].min()
            for i in range(draft.shape[0]):
                ind = draft.index[i]
                val = draft[old_col_name].iloc[i]
                scaled_val = (val - min_val)/(max_val - min_val)
                draft_hist.at[ind, new_col_name] = scaled_val
        else: # use 7 drafts
            drafts = draft_hist_gpby.get_group(year-3)
            for j in range(year-2, year+4):
                new_draft = draft_hist_gpby.get_group(j)
                drafts = pd.concat([drafts, new_draft], axis=0)
            max_val = drafts[old_col_name].max()
            min_val = drafts[old_col_name].min()
            for i in range(draft.shape[0]):
                ind = draft.index[i]
                val = draft[old_col_name].iloc[i]
                scaled_val = (val - min_val)/(max_val - min_val)
                draft_hist.at[ind, new_col_name] = scaled_val
    return draft_hist

def nine_year_scaling(draft_hist, old_col_name, new_col_name):
    """Scale old_col_name by five year max, and put in new_col_name.

    Returns draft_hist with the new column appended."""
    # make new column
    new_col = {new_col_name:[0.0]*draft_hist.shape[0]}
    names = list(draft_hist.index)
    new_col = pd.DataFrame(new_col, index = names)
    # append new column to draft_hist
    draft_hist = pd.concat([draft_hist, new_col], axis=1)
    # groupby by years and iterate through years
    draft_hist_gpby = draft_hist.groupby(['year'])
    for year, draft in draft_hist_gpby:
        if year < 1969 or year > 2013: # then not enough data
            continue
        elif year == 1969 or year == 2013: # use 5 drafts
            drafts = draft_hist_gpby.get_group(year-2)
            for j in range(year-1, year+3):
                new_draft = draft_hist_gpby.get_group(j)
                drafts = pd.concat([drafts, new_draft], axis=0)
            max_val = drafts[old_col_name].max()
            min_val = drafts[old_col_name].min()
            for i in range(draft.shape[0]):
                ind = draft.index[i]
                val = draft[old_col_name].iloc[i]
                scaled_val = (val - min_val)/(max_val - min_val)
                draft_hist.at[ind, new_col_name] = scaled_val
        elif year == 1970 or year == 2012: # use 7 drafts
            drafts = draft_hist_gpby.get_group(year-3)
            for j in range(year-2, year+4):
                new_draft = draft_hist_gpby.get_group(j)
                drafts = pd.concat([drafts, new_draft], axis=0)
            max_val = drafts[old_col_name].max()
            min_val = drafts[old_col_name].min()
            for i in range(draft.shape[0]):
                ind = draft.index[i]
                val = draft[old_col_name].iloc[i]
                scaled_val = (val - min_val)/(max_val - min_val)
                draft_hist.at[ind, new_col_name] = scaled_val
        else: # use 9 drafts
            drafts = draft_hist_gpby.get_group(year-4)
            for j in range(year-3, year+5):
                new_draft = draft_hist_gpby.get_group(j)
                drafts = pd.concat([drafts, new_draft], axis=0)
            max_val = drafts[old_col_name].max()
            min_val = drafts[old_col_name].min()
            for i in range(draft.shape[0]):
                ind = draft.index[i]
                val = draft[old_col_name].iloc[i]
                scaled_val = (val - min_val)/(max_val - min_val)
                draft_hist.at[ind, new_col_name] = scaled_val
    return draft_hist
