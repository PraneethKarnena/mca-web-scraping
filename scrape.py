from sys import argv
import json

import requests
from bs4 import BeautifulSoup


def parse_cin():
    try:
        if len(argv) < 2:
            raise Exception('Invalid CIN input!')
        cin = argv[1].upper()
        download_webpage(cin)

    except Exception as e:
        print(f'Error: {str(e)}')


def download_webpage(cin):
    try:
        URL = 'http://www.mca.gov.in/mcafoportal/companyLLPMasterData.do'
        post_body = {'companyID': cin}
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.post(URL, headers=headers, data=post_body)
        if response.status_code != 200:
            raise Exception('Cannot fetch webpage!')
        webpage = response.content
        extract_content(webpage)

    except Exception as e:
        print(f'Error: {str(e)}')


def extract_content(webpage):
    try:
        soup = BeautifulSoup(webpage, 'html.parser')

        company_table = soup.find('table', attrs={'id': 'resultTab1'}).find_all('td')
        director_table = soup.find('table', attrs={'id': 'resultTab6'}).find_all('td')

        for i in range(len(company_table)):
            company_table[i] = remove_special_chars(company_table[i].text)
        for i in range(len(director_table)):
            director_table[i] = remove_special_chars(director_table[i].text)

        company_data = {}
        for i in range(0, len(company_table), 2):
            company_data[company_table[i]] = company_table[i+1]

        NO_OF_DIR_COLS = 5
        director_data = []
        director_data_cols = ['DIN/PAN', 'Name', 'Begin date', 'End date', 'Date of Modification', 'Status']
        for i in range(0, len(director_table), NO_OF_DIR_COLS):
            director_data.append(director_table[i:i+NO_OF_DIR_COLS])

        for i in range(len(director_data)):
            director_data[i] = dict(zip(director_data_cols, director_data[i]))

        print_data(company_data, director_data)

    except Exception as e:
        print(f'Error: {str(e)}')


def print_data(company_data, director_data):
    print('\n---------- COMPANY DATA ----------\n')
    print(json.dumps(company_data, sort_keys=True, indent=4))
    print('\n--------- Directors Data ---------\n')
    print(json.dumps(director_data, sort_keys=True, indent=4))


def remove_special_chars(s):
    return s.rstrip().replace('\n', '').replace('\t', '').replace('\r', '').strip()


if __name__ == '__main__':
    parse_cin()