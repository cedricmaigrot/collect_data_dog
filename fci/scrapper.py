"""Scrapper du site de la FCI

    Returns:
        _type_: _description_
    """
import urllib.request

from bs4 import BeautifulSoup
import pandas as pd


def run():
    """Fonction principale de la collecte"""
    path = "https://www.fci.be/fr/Nomenclature/"
    with urllib.request.urlopen(path) as file_path:
        mybytes = file_path.read()
    html_doc = mybytes.decode("utf8")
    soup = BeautifulSoup(html_doc, 'html.parser')
    groups = soup.find_all("div", class_="group")
    dataframe = pd.DataFrame(data=get_groups(groups))
    dataframe['Fullname'] = dataframe['Fullname'].apply(lambda x: x.replace(
        "\r\n\t\t\t", " ").strip().title())
    dataframe.to_csv("data/fci.csv")
    dataframe.to_json("data/fci.json")


def get_groups(groups):
    """Liste les groupes de la FCI"""
    response = []
    for group in groups:
        base_url = group.a['href']
        res = get_group(f'https://www.fci.be{base_url}')
        for response_element in res:
            response.append(response_element)
    return response


def get_group(url):
    """Collecte les races d'un groupe"""
    print(url)
    with urllib.request.urlopen(url) as file_path:
        mybytes = file_path.read()
    html_doc = mybytes.decode("utf8")
    soup = BeautifulSoup(html_doc, 'html.parser')
    breeds = soup.find_all("td", class_="race")
    return get_breeds(breeds)


def get_breeds(breeds):
    """Liste les races d'un groupe"""
    response = []
    for breed in breeds:
        links = breed.find_all("a", class_="nom")
        base_url = links[0]['href']
        res = get_breed(f'https://www.fci.be{base_url}')
        response.append(res)
    return response


def get_breed(url):
    """Collecte les informations d'une race"""
    dictionary = {}
    with urllib.request.urlopen(url) as file_path:
        mybytes = file_path.read()
    html_doc = mybytes.decode("utf8")
    soup = BeautifulSoup(html_doc, 'html.parser')
    tables = soup.find_all("table", class_="racetable")
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            items = row.find_all("td")
            dictionary[items[0].text.strip()] = items[1].text.strip()
    tables = soup.find_all("table", class_="racesgridview")
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            items = row.find_all("td")
            dictionary[items[0].text.strip()] = items[1].text.strip()
    dictionary['Fullname'] = soup.find_all("h2", class_="nom")[0].text
    dictionary['Group'] = soup.find(
        id="ContentPlaceHolder1_GroupeHyperLink").text
    return dictionary
