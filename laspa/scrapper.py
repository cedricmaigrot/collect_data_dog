import requests
import pandas as pd


def run():
    print("LA SPA : collecte des données sur les refuges")
    get_shelters()
    print("LA SPA : collecte des données sur les animaux")
    get_animals()


def get_shelters():
    path = "https://www.la-spa.fr/app/wp-json/spa/v1/establishments/?api=1&types=refuges,maisons-spa&lat=&lng="
    response = requests.get(path)
    refuges = response.json()['items']
    df = pd.DataFrame(refuges)
    df.to_json('data/laspa_refuges.json')
    df.to_csv('data/laspa_refuges.csv')


def get_animals():
    url = f'https://www.la-spa.fr/app/wp-json/spa/v1/animals/search/?api=1&paged=1&seed=1'
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

    df = pd.DataFrame(elements)
    df.to_json('data/laspa_animaux.json')
    df.to_csv('data/laspa_animaux.csv')
