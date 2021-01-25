import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = 'https://www.bcfi.be/nl/classified_vmp_sets/6866?view=mp'  # GET request http
# URL = 'https://www.bcfi.be/nl/chapters/10?frag=6866&trade_family=19471' # browser http
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/87.0.4280.88 Safari/537.36',
    'Accept': '*/*',
}

table = []


def parser(url):
    r = requests.get(URL, headers=HEADERS)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    block = soup.findAll('div', class_='group')  # parts of html tree with single table in each
    for i in block:
        brand = i.find('div', class_='name mps')  # first row before table - company name
        active_substance = i.find('span', class_='inbasis')  # second row - substance
        soup_table = i.find('table',
                            class_='table table-condensed group-table mps responsive')  # part of soup with table
        pd_table = pd.read_html(str(soup_table))  # all tables from html
        pd_table_clean = pd_table[0][[2, 6]]  # pandas table with tablet form and price
        for i in range(2, len(pd_table_clean)):  # getting information from table (first two rows unnecessary)
            if pd_table_clean[2][i] == pd_table_clean[6][i]:  # to get tablet name information ("filmomh", and so on)
                tablet_form = pd_table_clean[2][i]  # this will rewrite tablet name information to current name
            list = [
                pd_table_clean[2][i],  # tablet form
                pd_table_clean[6][i],  # price
                brand.text.strip(),
                tablet_form,
                active_substance.text.strip()
            ]
            table.append(list)
    return table


def main():
    parser(URL)
    for row in table:
        if row[0] != row[1]:
            print('{},{},{},{},{}'.format(row[2], row[4], row[3], row[0], row[1]))


if __name__ == '__main__':
    main()
