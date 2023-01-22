
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd


def run():
    path = "https://www.fci.be/fr/Nomenclature/"
    fp = urllib.request.urlopen(path)
    mybytes = fp.read()
    html_doc = mybytes.decode("utf8")
    fp.close()
    soup = BeautifulSoup(html_doc, 'html.parser')
    groups = soup.find_all("div", class_="group")
    df = pd.DataFrame(data=get_groups(groups))
    df['Fullname'] = df['Fullname'].apply(lambda x: x.replace(
        "\r\n\t\t\t", " ").strip().title())
    df.to_csv("data/fci.csv")
    df.to_json("data/fci.json")


def get_groups(groups):
    response = []
    for group in groups:
        base_url = group.a['href']
        res = get_group(f'https://www.fci.be{base_url}')
        for r in res:
            response.append(r)
    return response


def get_group(url):
    print(url)
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    html_doc = mybytes.decode("utf8")
    fp.close()
    soup = BeautifulSoup(html_doc, 'html.parser')
    breeds = soup.find_all("td", class_="race")
    return get_breeds(breeds)


def get_breeds(breeds):
    response = []
    for breed in breeds:
        links = breed.find_all("a", class_="nom")
        base_url = links[0]['href']
        res = get_breed(f'https://www.fci.be{base_url}')
        response.append(res)
    return response


def get_breed(url):
    print(f'\t{url}')
    d = {}
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    html_doc = mybytes.decode("utf8")
    fp.close()
    soup = BeautifulSoup(html_doc, 'html.parser')
    tables = soup.find_all("table", class_="racetable")
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            items = row.find_all("td")
            d[items[0].text.strip()] = items[1].text.strip()
    tables = soup.find_all("table", class_="racesgridview")
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            items = row.find_all("td")
            d[items[0].text.strip()] = items[1].text.strip()
    d['Fullname'] = soup.find_all("h2", class_="nom")[0].text
    d['Group'] = soup.find(id="ContentPlaceHolder1_GroupeHyperLink").text
    return d
