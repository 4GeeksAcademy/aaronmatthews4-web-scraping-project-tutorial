import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

response = requests.get("https://www.mlb.com/stats/san-francisco-giants/all-time-by-season")
print(response.status_code)

soup = BeautifulSoup(response.content, "html.parser")

tables = soup.find_all("table")
tables

table = tables[0]

columns = []

for abbr in table.find_all('abbr', class_=lambda value: value and value.startswith("bui-text cellheader")):
    column_label = abbr.text.strip()
    columns.append(column_label)

print(columns)

from collections import OrderedDict

columns = list (OrderedDict.fromkeys(columns))
columns

all_rows = []

tr_tags = table.find_all('tr')

for tr in tr_tags[1:]:
    row = []

    player_span = tr.find_all('span', class_="short-IiSPVSQp")
    player_name = ' '.join(span.text for span in player_span)

    row.append(player_name)

    other_row_elements = [row.append (td.text.strip()) for td in tr.find_all('td')]

    all_rows.append(row)

all_rows

import pandas as pd

df = pd.DataFrame(all_rows, columns=columns)

df

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df['HR'] = pd.to_numeric(df['HR'], errors='coerce')
df['RBI'] = pd.to_numeric(df['RBI'], errors='coerce')


df.dropna(subset=['PLAYER', 'HR', 'RBI'], inplace=True)

# Bar Plot: Total Home Runs per Player

plt.figure(figsize=(12, 6))
sns.barplot(data=df, x='PLAYER', y='HR', color='skyblue')
plt.title('Home Runs per Player')
plt.xlabel('Player')
plt.ylabel('Home Runs')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Scatter Plot: Home Runs vs. RBI

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='HR', y='RBI', color='coral')
plt.title('Relationship between Home Runs and RBI')
plt.xlabel('Home Runs')
plt.ylabel('RBI')
plt.tight_layout()
plt.savefig("Figures.jpeg")

