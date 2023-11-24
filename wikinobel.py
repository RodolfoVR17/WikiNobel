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

df.to_csv("nobel.csv", index=False)
def scrape_data2(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the specific section by its heading
    li = soup.find_all('ol')

    print(li)

    for h2 in li:
        if h2.span and 'Country (or territory) of birth' in h2.span.text:
            break

    # Get the next sibling element that is a 'div'
    div = h2.find_next_sibling('div')

    data = []
    for country in div.find_all('h3'):
        country_name = country.span.text
        for li in country.find_next_sibling('ul').find_all('li'):
            laureate_info = [country_name] + [info.strip() for info in li.text.split(',')]
            data.append(laureate_info)

    return data

print(scrape_data2(url2))
