import requests
from bs4 import BeautifulSoup
import pandas as pd

import wikipedia

def convert_encoding(element):
    if isinstance(element, str):
        return element.encode('ISO-8859-1').decode('UTF-8')
    else:
        return element

def scrape_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'wikitable'})
    rows = table.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        data.append(cols)
    return data


def clean_dataframe(df):

    # Load the data with specified encoding
    df = pd.read_csv('nobel.csv', encoding='ISO-8859-1')

    # Remove whitespaces
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Handle missing values (this will depend on your specific data)
    df = df.dropna()  # This line removes any rows with missing values

    # Convert data to appropriate types
    df['year'] = pd.to_datetime(df['year'], format='%Y', errors='coerce')

    df = df.applymap(convert_encoding)
    df = df.dropna(how='any')
    print(df)

    print(df.head())
    df = pd.read_csv('nobel.csv').dropna(how='all')
    df = df.fillna('No award')


    df.to_csv("nobel.csv", index=False)

    return df

url = 'https://en.wikipedia.org/wiki/List_of_Nobel_laureates'

url2 = "https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country"

df = pd.DataFrame(scrape_data(url), columns=['year', 'physics', 'chemistry', 'medicine', 'literature', 'peace', 'economics'])

df = clean_dataframe(df)


def look_year_and_category(year, category):
    df_year = df[(df['year'] == year)]
    word_list = df_year[category].tolist()
    word_list = (word_list[0].split(';'))
    return word_list


print(look_year_and_category(1998, 'economics'))




def find_column_with_name(df, name):
    # Convert all columns to string and apply the mask
    mask = df.applymap(str).apply(lambda col: col.str.contains(name, na=False))
    
    # Find columns where 'name' is found
    columns_with_name = df.columns[mask.any(axis=0)]
    
    # Return the column names as a list
    return list(columns_with_name)

print(find_column_with_name(df, 'Marie Curie'))


wikipedia.set_lang("en")  # For Spanish, for example


# Search for pages
results = wikipedia.search("Nobel Prize")

# Access a specific page
page = wikipedia.page("List of Nobel laureates by country")

# Get the whole page content
content = page.content

# Get a summary
summary = page.summary

# Get page title
title = page.title

# Other information like page URL, links, etc.
url = page.url
links = page.links

try:
    page = wikipedia.page("List of Nobel laureates by country")
    content = page.content
    print("Title: " + page.title)
    print(content)
except wikipedia.exceptions.PageError:
    print("Page not found")
except wikipedia.exceptions.DisambiguationError as e:
    print("Disambiguation error. Possible options include:")
    print(e.options)
