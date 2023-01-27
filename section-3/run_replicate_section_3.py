#!/usr/bin/python
import subprocess

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

print('Replicating Statistical Data for Section 3: RQ3, RQ4 and RQ5')
print()

print('========== RQ3 ==========')
subprocess.call(['python', 'RQ3.py'], cwd='RQ3')
print()

print('========== RQ4 ==========')
print_msg_box('Data for Figure 3')
subprocess.call(['python', 'RQ4.py'], cwd='RQ4')
print()

print('========== RQ5 ==========')
print_msg_box('Data for Figure 4\nReproducibility of Cached Artifacts')
subprocess.call(['python', 'RQ5-eval-cached-artifacts.py'], cwd='RQ5')
print()

print_msg_box('Data for Figure 4\nReproducibility of Isolated Artifacts')
subprocess.call(['python', 'RQ5-eval-isolated-artifacts.py'], cwd='RQ5')
print()