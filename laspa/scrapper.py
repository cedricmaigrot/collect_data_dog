"""Scrapper du site de la SPA
    """
import requests
import pandas as pd


def run():
    """Fonction principale de la collecte"""
    print("LA SPA : collecte des données sur les refuges")
    get_shelters()
    print("LA SPA : collecte des données sur les animaux")
    get_animals()


def get_shelters():
    """Liste les refuges"""
    arguments = "api=1&types=refuges,maisons-spa&lat=&lng="
    path = f"https://www.la-spa.fr/app/wp-json/spa/v1/establishments/?{arguments}"
    response = requests.get(path)
    refuges = response.json()['items']
    dataframe = pd.DataFrame(refuges)
    dataframe.to_json('data/laspa_refuges.json')
    dataframe.to_csv('data/laspa_refuges.csv')


def get_animals():
    """Collecte les informations sur les animaux d'un refuge"""
    url = 'https://www.la-spa.fr/app/wp-json/spa/v1/animals/search/?api=1&paged=1&seed=1'
    response = requests.get(url)
    elements = response.json()['results']

    page = 2
    while page <= response.json()['nb_pages']:
        print(f"Page {page}/{response.json()['nb_pages']}")
        url = f'https://www.la-spa.fr/app/wp-json/spa/v1/animals/search/?api=1&paged={page}&seed=1'
        response = requests.get(url)
        for elem in response.json()['results']:
            elements.append(elem)
        page += 1

    dataframe = pd.DataFrame(elements)
    dataframe.to_json('data/laspa_animaux.json')
    dataframe.to_csv('data/laspa_animaux.csv')
