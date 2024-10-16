import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns


import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



url = "https://www.mlb.com/stats/san-francisco-giants/all-time-by-season"
response = requests.get(url)


if response.status_code == 200:
    print("Successfully fetched the webpage!")
else:
    print(f"Failed to fetch the webpage. Status code: {response.status_code}")
    exit()


soup = BeautifulSoup(response.content, "html.parser")

tables = soup.find_all("table")


if tables:
    print(f"Found {len(tables)} tables on the webpage.")
    table = tables[0]  
else:
    print("No tables found on the webpage.")
    exit()


rows = table.find_all("tr")
table_data = []


headers = [header.text.strip() for header in rows[0].find_all("th")]
table_data.append(headers)


for row in rows[1:]:
    cols = [col.text.strip() for col in row.find_all("td")]
    
    
    if len(cols) < len(headers):
        cols += [None] * (len(headers) - len(cols))
    
    table_data.append(cols)


df = pd.DataFrame(table_data[1:], columns=table_data[0])


print("Extracted Data:")
print(df)



df.dropna(inplace=True) 

df.to_csv("mlb_stats.csv", index=False)
print("Data saved to mlb_stats.csv")

# Runs Batted In by Year


if 'Year' in df.columns and 'Runs batted in' in df.columns:
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Year', y='Runs batted in', data=df)
    plt.title("San Francisco Giants Runs Batted In by Year")
    plt.xticks(rotation=90)
    plt.xlabel('Year')
    plt.ylabel('Runs Batted In (RBIs)')
    plt.show()

    
# Double by Year

if 'Year' in df.columns and 'Doubles' in df.columns:
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Year', y='Doubles', data=df)
    plt.title("San Francisco Giants Doubles by Year")
    plt.xticks(rotation=90)
    plt.xlabel('Year')
    plt.ylabel('Doubles')
    plt.show()

# Stolen Bases by Year

if 'Year' in df.columns and 'Stolen bases' in df.columns:
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Year', y='Stolen bases', data=df)
    plt.title("San Francisco Giants Stolen Bases by Year")
    plt.xticks(rotation=90)
    plt.xlabel('Year')
    plt.ylabel('Stolen Bases')
    plt.show()