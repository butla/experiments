from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import pytz
import seaborn as sns

CATEGORY_FIELD = 'category'
COLUMN_1 = 'Spam'
COLUMN_2 = 'Ham'
COLUMN_TOTAL = 'total'
SIGNIFICANT_ROWS = 7

df = pd.DataFrame({
    CATEGORY_FIELD: ['Ada', 'Bob', 'Cody', 'Dio', 'El', 'Fig', 'Gia', 'Hec', 'Ida', 'Jay'],
    COLUMN_1: [44, 100, 49, 0, 0, 15, 7, 3, 0, 900],
    COLUMN_2: [33, 940, 50, 0, 250, 10, 17, 5, 0, 100],
})

# TODO can I get rid of the white background?
sns.set(style='dark')

# make sure the index (labels on the X axis) is set
df = df.set_index(CATEGORY_FIELD)

df[COLUMN_TOTAL] = df[COLUMN_1] + df[COLUMN_2]
df = df.sort_values(by=[COLUMN_TOTAL], ascending=False)
# leave a set number of most significant values
df = df.iloc[:SIGNIFICANT_ROWS]


# create the chart
df.plot(kind='bar', y=[COLUMN_1, COLUMN_2], stacked=True, color=['steelblue', 'red'], figsize=(8,8))

current_time_utc = datetime.now(pytz.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
CET = 'CET'
current_time_pst = datetime.now(pytz.timezone(CET)).strftime(f'%Y-%m-%d %H:%M:%S {CET}')
current_time_cet = datetime.now(pytz.timezone('US/Pacific')).strftime(f'%Y-%m-%d %H:%M:%S PST')

plt.title(f'{SIGNIFICANT_ROWS} people with biggest sums\n{current_time_cet}\n{current_time_utc}\n{current_time_pst}', fontsize=14)
plt.xlabel('Category')
plt.ylabel('Number')

plt.xticks(rotation=30)

figure_file_path = 'demo_figure.svg'
print('Writing', figure_file_path, '...')
plt.savefig(figure_file_path)

plt.show()
