# %%
import pandas as pd
import numpy as np

# %%

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
def csv_diff(reference, generated):
    merged = pd.concat([reference,generated], axis=0)
    return merged.drop_duplicates(keep=False)

# %%
print_msg_box('Data for Figure 1')
try:
    reference = pd.read_csv('reference/figure_1.csv')
    print('Success: Found reference data: reference/figure_1.csv')
    generated = pd.read_csv('RQ3/figure_1.out.csv')
    print('Success: Found generated data: RQ3/figure_1.out.csv')
except:
    print('Error: Could not find reference data or generated data.')
    print('Please run run_replicate_section_3.py first.')
    exit(1)

if not reference.equals(generated):
    print('Error: Generated data does not match reference data. See the difference below.')
    print(csv_diff(reference, generated))
else:
    print('Success: Generated data matches reference data.')

# %%
print_msg_box('Data for Figure 2')
try:
    reference = pd.read_csv('reference/figure_2.csv')
    print('Success: Found reference data: reference/figure_2.csv')
    generated = pd.read_csv('RQ3/figure_2.out.csv')
    print('Success: Found generated data: RQ3/figure_2.out.csv')
except:
    print('Error: Could not find reference data or generated data.')
    print('Please run run_replicate_section_3.py first.')
    exit(1)

if not reference.equals(generated):
    print('Error: Generated data does not match reference data. See the difference below.')
    print(csv_diff(reference, generated))
else:
    print('Success: Generated data matches reference data.')

# %%
print_msg_box('Statistical Data for RQ3')
try:
    reference = pd.read_csv('reference/stat_rq3.csv')
    print('Success: Found reference data: reference/stat_rq3.csv')
    generated = pd.read_csv('RQ3/stat_rq3.out.csv')
    print('Success: Found generated data: RQ3/stat_rq3.out.csv')
except:
    print('Error: Could not find reference data or generated data.')
    print('Please run run_replicate_section_3.py first.')
    exit(1)

if not reference.equals(generated):
    print('Error: Generated data does not match reference data. See the difference below.')
    print(csv_diff(reference, generated))
else:
    print('Success: Generated data matches reference data.')

# %%
print_msg_box('Data for Figure 3')
try:
    reference = pd.read_csv('reference/figure_3.csv')
    print('Success: Found reference data: reference/figure_3.csv')
    generated = pd.read_csv('RQ4/figure_3.out.csv')
    print('Success: Found generated data: RQ4/figure_3.out.csv')
except:
    print('Error: Could not find reference data or generated data.')
    print('Please run run_replicate_section_3.py first.')
    exit(1)

if not reference.equals(generated):
    print('Error: Generated data does not match reference data. See the difference below.')
    print(csv_diff(reference, generated))
else:
    print('Success: Generated data matches reference data.')

# %%
print_msg_box('Data for Figure 4\nReproducibility of Cached Artifacts')
try:
    reference = pd.read_csv('reference/figure_4_cached.csv')
    print('Success: Found reference data: reference/figure_4_cached.csv')
    generated = pd.read_csv('RQ5/figure_4_cached.out.csv')
    print('Success: Found generated data: RQ5/figure_4_cached.out.csv')
except:
    print('Error: Could not find reference data or generated data.')
    print('Please run run_replicate_section_3.py first.')
    exit(1)

if not reference.equals(generated):
    print('Error: Generated data does not match reference data. See the difference below.')
    print(csv_diff(reference, generated))
else:
    print('Success: Generated data matches reference data.')

# %%
print_msg_box('Data for Figure 4\nReproducibility of Isolated Artifacts')
try:
    reference = pd.read_csv('reference/figure_4_isolated.csv')
    print('Success: Found reference data: reference/figure_4_isolated.csv')
    generated = pd.read_csv('RQ5/figure_4_isolated.out.csv')
    print('Success: Found generated data: RQ5/figure_4_isolated.out.csv')
except:
    print('Error: Could not find reference data or generated data.')
    print('Please run run_replicate_section_3.py first.')
    exit(1)

if not reference.equals(generated):
    print('Error: Generated data does not match reference data. See the difference below.')
    print(csv_diff(reference, generated))
else:
    print('Success: Generated data matches reference data.')

# %%



