# %%
import pandas as pd
import os

# %%
non_flaky_artifacts = pd.read_csv('1700-Cached-Non-Flaky-Tags.csv')['Cached Non Flaky Images'].values.tolist()
print('{} artifacts are successfully cached.'.format(len(non_flaky_artifacts)))

# %%
def get_suite_number(file_name):
    num = file_name.split('-')[-1].split('.')[0]
    return int(num)

# %%
all_suite = os.listdir('../test-suites-for-eval-after-study-range')
all_suite.sort(key=get_suite_number)
print('{} test suites are read for evaluation.'.format(len(all_suite)))

df_figure4_cached = pd.DataFrame(columns=['Suite', 'Cached Non-Flaky Java Artifacts', 'Reproducible', 'Reproducibility'])
# %%
for idx, suite_name in enumerate(all_suite):
    df = pd.read_csv('../test-suites-for-eval-after-study-range/{}'.format(suite_name))

    df = df[df['Language'] == 'Java']
    df = df[df['Image Tag'].isin(non_flaky_artifacts)]
    print('{}: {} cached non-flaky java artifacts;'.format(suite_name, len(df)), end=" ")
    # now got 1700 non flaky cached Java
    print('{} reproducible.'.format(len(df[(df['Status']=='Finished') & (df['Broken'] == 'No')])), end = " ")
    print('Reproducibility: {}'.format(len(df[(df['Status']=='Finished') & (df['Broken'] == 'No')]) / len(df)))

    df_figure4_cached.loc[len(df_figure4_cached)] = [suite_name, len(df), len(df[(df['Status']=='Finished') & (df['Broken'] == 'No')]), len(df[(df['Status']=='Finished') & (df['Broken'] == 'No')]) / len(df)]

# %%

df_figure4_cached.to_csv('figure_4_cached.out.csv', index=False)



