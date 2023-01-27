# %%
import pandas as pd

# %%
patch_data = pd.read_csv('Patches-Applied.csv')

# %%
print(patch_data[['Image Tag', 'Num Patches']].groupby(['Num Patches']).count())

patch_data[['Image Tag', 'Num Patches']].groupby(['Num Patches']).count().to_csv('figure_3.out.csv')

# %%



