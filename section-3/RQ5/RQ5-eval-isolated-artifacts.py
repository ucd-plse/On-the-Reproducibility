# %%
import pandas as pd
import os

# %%
isolated_artifacts = pd.read_csv('1257-Isolated-Tags.csv')['Isolated Image Tags'].values.tolist()
print('{} artifacts are fully isolated.'.format(len(isolated_artifacts)))

# %%
def get_suite_number(file_name):
    num = file_name.split('-')[-1].split('.')[0]
    return int(num)

# %%
all_suite = os.listdir('../test-suites-for-eval-after-study-range')
all_suite.sort(key=get_suite_number)
print('{} test suites are read for evaluation.'.format(len(all_suite)))

df_figure4_isolated = pd.DataFrame(columns=['Suite', 'Isolated Java Artifacts', 'Reproducible', 'Reproducibility'])
# %%
for idx, suite_name in enumerate(all_suite):
    df = pd.read_csv('../test-suites-for-eval-after-study-range/{}'.format(suite_name))

    df = df[df['Language'] == 'Java']
    df = df[df['Image Tag'].isin(isolated_artifacts)]
    print('{}: {} cached isolated java artifacts;'.format(suite_name, len(df)), end=" ")
    # now got 1257 non flaky isolated cached Java
    print('{} reproducible.'.format(len(df[(df['Status']=='Finished') & (df['Broken'] == 'No')])), end = " ")
    print('Reproducibility: {}'.format(len(df[(df['Status']=='Finished') & (df['Broken'] == 'No')]) / len(df)))

    df_figure4_isolated.loc[len(df_figure4_isolated)] = [suite_name, len(df), len(df[(df['Status']=='Finished') & (df['Broken'] == 'No')]), len(df[(df['Status']=='Finished') & (df['Broken'] == 'No')]) / len(df)]


# %%

df_figure4_isolated.to_csv('figure_4_isolated.out.csv', index=False)



