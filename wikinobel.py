import requests
from bs4 import BeautifulSoup
import pandas as pd

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


url = 'https://en.wikipedia.org/wiki/List_of_Nobel_laureates'

url2 = "https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country"

df = pd.DataFrame(scrape_data(url), columns=['year', 'physics', 'chemistry', 'medicine', 'literature', 'peace', 'economics'])

# Load the data with specified encoding
df = pd.read_csv('nobel.csv', encoding='ISO-8859-1')


# Remove any leading/trailing whitespace
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Handle missing values (this will depend on your specific data)
df = df.dropna()  # This line removes any rows with missing values

# Convert data to appropriate types
df['year'] = pd.to_datetime(df['year'], format='%Y', errors='coerce')



def convert_encoding(element):
    if isinstance(element, str):
        return element.encode('ISO-8859-1').decode('UTF-8')
    else:
        return element

df = df.applymap(convert_encoding)
df = df.dropna(how='any')
print(df)

print(df.head())
df = pd.read_csv('nobel.csv').dropna(how='all')
df = df.fillna('No award')


df.to_csv("nobel.csv", index=False)

def scrape_data2(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the specific section by its heading
    h2s = soup.find_all('h2')
    for h2 in h2s:
        if h2.span and 'Country (or territory) of birth' in h2.span.text:
            break
    print("This is H2")
    print(h2)  # Check the content of h2

    # Get the next sibling element that is a 'div'
    div = h2.find_next_sibling('div')
    print("This is DIV")
    print(div)  # Check the content of div

    data = []
    for country in div.find_all('h3'):
        country_name = country.span.text
        for li in country.find_next_sibling('ul').find_all('li'):
            laureate_info = [country_name] + [info.strip() for info in li.text.split(',')]
            data.append(laureate_info)

    return data

#print(scrape_data2(url2))

def look_year_category(year, category):
    df_year = df[(df['year'] == year)]
    word_list = df_year[category].tolist()
    word_list = (word_list[0].split(';'))
    return word_list

print(look_year_category(1903, 'economics'))


