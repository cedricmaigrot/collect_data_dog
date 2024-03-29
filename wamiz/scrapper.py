"""Scrapper du site Wamiz
    """
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd


def run():
    """Fonction principale de la collecte"""
    path = "http://wamiz.com/chiens/race-chien"
    user_agent = (
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; "
        + "rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"
    )

    headers = {
        "User-Agent": user_agent,
    }

    with urllib.request.Request(path, None, headers) as response:
        mybytes = response.read()

    html_doc = mybytes.decode("utf8")

    soup = BeautifulSoup(html_doc, "html.parser")
    groups = soup.find_all("li", class_="col-6 col-sm-4 mb-3")
    dataframe = pd.DataFrame(data=get_breeds(groups))

    dataframe["taille femelle"] = dataframe["Chien femelle"]
    dataframe["taille mâle"] = dataframe["Chien mâle"]
    dataframe["poids femelle"] = dataframe["Chien femelle_"]
    dataframe["poids mâle"] = dataframe["Chien mâle_"]

    dataframe.pop("Chien femelle")
    dataframe.pop("Chien mâle")
    dataframe.pop("Chien femelle_")
    dataframe.pop("Chien mâle_")

    dataframe.to_csv("data/wamiz.csv")
    dataframe.to_json("data/wamiz.json")


def get_breeds(breeds):
    """Liste les races d'un groupe"""
    response = []
    for breed in breeds:
        links = breed.find_all("a")
        base_url = links[0]["href"]
        res = get_breed(f"https://wamiz.com{base_url}")
        response.append(res)
    return response


def get_breed(path):
    """Collecte les informations d'une race"""
    print(f"\t{path}")
    dictionary = {}
    user_agent = (
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7)"
        + " Gecko/2009021910 Firefox/3.0.7"
    )

    with urllib.request.urlopen(
        urllib.request.Request(
            path,
            None,
            {
                "User-Agent": user_agent,
            },
        )
    ) as response:
        mybytes = response.read()
    html_doc = mybytes.decode("utf8")

    soup = BeautifulSoup(html_doc, "html.parser")
    elems = soup.find_all("p", class_="tw-text-3")
    breed_name = soup.find("h1").text
    print(breed_name)
    for elem in elems:
        text = elem.text.strip().split(":")
        if len(text) == 2:
            if text[0].strip() not in dictionary:
                dictionary[text[0].strip()] = text[1].strip()
            else:
                dictionary[text[0].strip() + "_"] = text[1].strip()

    elems = soup.find_all("div", class_="breed-card")
    for elem in elems:
        # try:
        scores = elem.find_all(
            "p", class_="tw-text-4 tw-font-bold tw-font-poppins text-right"
        )
        score = scores[0].text.strip()
        scores = elem.find_all("h3", class_="tw-text-3")
        score_title = scores[0].text.strip().replace(f"Le {breed_name} et ", "")
        score_title = score_title.replace(f"Le {breed_name}", "")

        dictionary[score_title] = score
        # except Exception as exception:
        #     print(exception)
    return dictionary


if __name__ == "__main__":
    run()
