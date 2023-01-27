# %%
import pandas as pd
import numpy as np

# %%
import os, sys

def print_msg_box(msg, indent=1, width=None, title=None):
    # credit to https://stackoverflow.com/a/58780542
    """Print message-box with optional title."""
    lines = msg.split('\n')
    space = " " * indent
    if not width:
        width = max(map(len, lines))
    box = f'╔{"═" * (width + indent * 2)}╗\n'  # upper_border
    if title:
        box += f'║{space}{title:<{width}}{space}║\n'  # title
        box += f'║{space}{"-" * len(title):<{width}}{space}║\n'  # underscore
    box += ''.join([f'║{space}{line:<{width}}{space}║\n' for line in lines])
    box += f'╚{"═" * (width + indent * 2)}╝'  # lower_border
    print(box)

# %%
def get_suite_number(file_name):
    num = file_name.split('-')[-1].split('.')[0]
    return int(num)

# %%
all_suite = os.listdir('../test-suites-in-13-months-study-range')
all_suite.sort(key=get_suite_number)

# %%
non_flaky_list = pd.read_csv('../1795-Non-Flaky-Tags.csv')
non_flaky_list = non_flaky_list['Non-flaky Image Tags'].values.tolist()

# %%
print('Test suite in study range: {} suites loaded.'.format(len(all_suite)))

# %% [markdown]
# ## Data for Figure 2

# %%
all_broken = []
all_reproducible = []

# %%
current_df = pd.read_csv('../test-suites-in-13-months-study-range/{}'.format(all_suite[0]))
current_df = current_df[current_df['Language'] == 'Java']
current_df = current_df[current_df['Image Tag'].isin(non_flaky_list)]
first_suite_broken = current_df[(current_df['Language']=='Java') & (current_df['Broken']=='Yes')]['Image Tag'].values.tolist()
all_broken.append(first_suite_broken)
first_suite_reproducible = current_df[(current_df['Language']=='Java') & (current_df['Broken']=='No')]['Image Tag'].values.tolist()
all_reproducible.append(first_suite_reproducible)

# %%
print_msg_box('Data for Figure 2')
df_figure_2 = pd.DataFrame(columns=['Suite', 'Newly Reproducible', 'Newly Broken'])

for idx in range(1, len(all_suite)):
    print('Processing {}'.format(all_suite[idx]), end=': ')
    current_df = pd.read_csv('../test-suites-in-13-months-study-range/{}'.format(all_suite[idx]))
    current_df = current_df[current_df['Language'] == 'Java']
    current_df = current_df[current_df['Status'] == 'Finished']
    current_df = current_df[current_df['Image Tag'].isin(non_flaky_list)]
    prev_df = pd.read_csv('../test-suites-in-13-months-study-range/{}'.format(all_suite[idx-1]))
    prev_df = prev_df[prev_df['Language'] == 'Java']
    prev_df = prev_df[prev_df['Status'] == 'Finished']
    prev_df = prev_df[prev_df['Image Tag'].isin(non_flaky_list)]
    

    newly_broken = []
    newly_reproducible = []
    newly_added_tags = []
    for tag in current_df['Image Tag'].values.tolist():
        try:
            if prev_df.loc[prev_df['Image Tag'] == tag, 'Broken'].values.tolist()[0] == 'No': 
                # and now it is broken in current suite
                if current_df.loc[current_df['Image Tag'] == tag, 'Broken'].values.tolist()[0] == 'Yes': 
                    newly_broken.append(tag)
            # if it is broken already
            if prev_df.loc[prev_df['Image Tag'] == tag, 'Broken'].values.tolist()[0] == 'Yes':
                # and now it is reproducible in current suite
                if current_df.loc[current_df['Image Tag'] == tag, 'Broken'].values.tolist()[0] == 'No':
                    newly_reproducible.append(tag)
        except IndexError:
            newly_added_tags.append(tag)
            continue
    print('{} newly reproducible, {} newly broken'.format(len(newly_reproducible), len(newly_broken)))
    # print('{} artifacts added'.format(len(newly_added_tags)))
    dict_to_append = {'Suite': all_suite[idx], 'Newly Reproducible': len(newly_reproducible), 'Newly Broken': len(newly_broken)}
    df_figure_2 = pd.concat([df_figure_2, pd.DataFrame.from_records([dict_to_append])])
    all_broken.append(newly_broken)
    all_reproducible.append(newly_reproducible)

df_figure_2.to_csv('figure_2.out.csv', index=False)

# %%
print_msg_box('Statistical Data for RQ3')
df_stat_rq3 = pd.DataFrame(columns={'Key', 'Value'})

# unique artifacts break at least once
print('Number of artifacts that break at least once: {}'.format(len(list(set(sum(all_broken, []))))))
df_stat_rq3.loc[len(df_stat_rq3)] = {'Key': 'Number of artifacts that break at least once', 'Value': len(list(set(sum(all_broken, []))))}

# %%
# all breakage instances
print('Number of breakage instances: {}'.format(sum([len(x) for x in all_broken])))
df_stat_rq3.loc[len(df_stat_rq3)] = {'Key': 'Number of breakage instances', 'Value': sum([len(x) for x in all_broken])}

# %%
print('Average newly broken: {}'.format(np.mean([len(x) for x in all_broken[1:]])))
df_stat_rq3.loc[len(df_stat_rq3)] = {'Key': 'Average newly broken', 'Value': np.mean([len(x) for x in all_broken[1:]])}

# %%
print('Median newly broken: {}'.format(np.median([len(x) for x in all_broken[1:]])))
df_stat_rq3.loc[len(df_stat_rq3)] = {'Key': 'Median newly broken', 'Value': np.median([len(x) for x in all_broken[1:]])}

# %%
print('Average newly reproducible: {}'.format(np.mean([len(x) for x in all_reproducible[1:]])))
df_stat_rq3.loc[len(df_stat_rq3)] = {'Key': 'Average newly reproducible', 'Value': np.mean([len(x) for x in all_reproducible[1:]])}

# %%
print('Median newly reproducible: {}'.format(np.median([len(x) for x in all_reproducible[1:]])))
df_stat_rq3.loc[len(df_stat_rq3)] = {'Key': 'Median newly reproducible', 'Value': np.median([len(x) for x in all_reproducible[1:]])}

df_stat_rq3.to_csv('stat_rq3.out.csv', index=False)

# %% [markdown]
# ## Data for Figure 1

# %%
from collections import Counter

# %%
print_msg_box('Data for Figure 1')
df_break_times = pd.DataFrame.from_dict(Counter(sum(all_broken, [])), orient='index', columns=['Break Times'])
df_break_times['Image Tag'] = df_break_times.index
print(df_break_times.groupby(['Break Times']).count())

df_break_times.groupby(['Break Times']).count().to_csv('figure_1.out.csv')

# %%
# average breakages on each test suites
suite_breakages_num = []
for idx in range(len(all_suite)):
    df = pd.read_csv('../test-suites-in-13-months-study-range/{}'.format(all_suite[idx]))
    df = df[df['Image Tag'].isin(non_flaky_list)]
    # df = df[df['Language']=='Java']
    suite_breakages_num.append(len(df[(df['Status'] == 'Finished') & (df['Broken'] == 'Yes')]))

# %%
print('Average breakages in each test suite: {}'.format(np.mean(suite_breakages_num)))

# %%



