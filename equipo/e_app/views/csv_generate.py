# ample.py

import pandas as pd
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse

# Base URL and headers
base_url = 'https://www.hcpcsdata.com/Codes/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


def parse_group(group_url, group_name):
    group_url = 'https://www.hcpcsdata.com/Codes/'
    response = requests.get(group_url, headers=headers)
    # import pdb;
    # pdb.set_trace()

    if response.status_code != 200:
        print(response.status_code)
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'table table-hover table-responsive'})
    if table is None:
        print(table)

        return None

    table_rows = table.find('tbody').find_all('tr')
    rows = []
    for tr in table_rows:
        tds = tr.find_all('td')
        if len(tds) == 3:
            codes = tds[0].get_text(strip=True)
            count = tds[1].get_text(strip=True)
            category = tds[2].get_text(strip=True)

            individual_code_call_url = group_url + f'{group_name}'
            individual_code_call_response = requests.get(individual_code_call_url, headers=headers)
            if individual_code_call_response.status_code != 200:
                return None

            soup_2 = BeautifulSoup(individual_code_call_response.content, 'html.parser')
            table_2 = soup_2.find('table', {'class': 'table table-hover'})
            h1_data = soup_2.find('h1')

            if table_2 is None:
                return None
            table_rows_2 = table_2.find('tbody').find_all('tr')

            for tr_2 in table_rows_2:
                tds_2 = tr_2.find_all('td')
                if len(tds_2) == 2:
                    code = tds_2[0].get_text(strip=True)
                    description = tds_2[1].get_text(strip=True)

                    short_description_url = individual_code_call_url + f"/{code}"
                    short_description_url_reponse = requests.get(short_description_url, headers=headers)
                    # import pdb; pdb.set_trace()
                    if short_description_url_reponse.status_code != 200:
                        print("short_description_url_reponse")

                        return None
                    soup_3 = BeautifulSoup(short_description_url_reponse.content, 'html.parser')
                    table_3 = soup_3.find('table', {'class': 'table table-hover table-condensed'})

                    if table_3 is None:
                        print("table_3")
                        return None

                    first_row_3 = table_3.find('tbody').find('tr')
                    short_description = None
                    if first_row_3:
                        tds_3 = first_row_3.find_all('td')
                        short_description = tds_3[1].get_text(strip=True)

                    rows.append([h1_data.text.strip(), category, code, description, short_description])
    return rows


def scrape_all_groups():
    try:
        groups = [
            # ('A', base_url + 'A'),
            # ('B', base_url + 'B'),
            # ('C', base_url + 'C'),
            # ('E', base_url + 'E'),
            # ('G', base_url + 'G'),
            # ('H', base_url + 'H'),
            # ('J', base_url + 'J'),
            # ('K', base_url + 'K'),
            # ('L', base_url + 'L'),
            # ('M', base_url + 'M'),
            # ('P', base_url + 'P'),
            # ('Q', base_url + 'Q'),
            ('R', base_url + 'R'),
            # ('S', base_url + 'S'),
            # ('T', base_url + 'T'),
            # ('U', base_url + 'U'),
            # ('V', base_url + 'V'),
        ]

        all_data = []
        for group_name, group_url in groups:
            # for group_name, group_url in ('a','https://www.hcpcsdata.com/Codes/'):
            #     import pdb; pdb.set_trace()
            group_data = parse_group(group_url, group_name)
            if group_data:
                all_data.extend(group_data)

        return all_data
    except Exception as e:
        print(e)
        return None


def download_hcpcs_codes(request):
    # Scrape the data
    data = scrape_all_groups()
    if not data:
        return HttpResponse("Failed to retrieve HCPCS data", status=500)

    # Convert the data to a CSV format
    df = pd.DataFrame(data, columns=['Group', 'Category', 'Code', 'Long Description', 'Short Description'])

    # Create a response object for the CSV file download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="hcpcs_codes.csv"'

    # Write the DataFrame to the response
    df.to_csv(response, index=False)

    return response
