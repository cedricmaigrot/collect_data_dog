
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd


def run():
    path = "http://wamiz.com/chiens/race-chien"
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

    headers = {'User-Agent': user_agent, }

    request = urllib.request.Request(
        path, None, headers)  # The assembled request
    response = urllib.request.urlopen(request)

    mybytes = response.read()
    html_doc = mybytes.decode("utf8")
    response.close()

    soup = BeautifulSoup(html_doc, 'html.parser')
    groups = soup.find_all("li", class_="col-6 col-sm-4 mb-3")
    df = pd.DataFrame(data=get_breeds(groups))

    df.to_csv("data/wamiz.csv")
    df.to_json("data/wamiz.json")


def get_breeds(breeds):
    response = []
    for breed in breeds:
        links = breed.find_all("a")
        base_url = links[0]['href']
        res = get_breed(f'https://wamiz.com{base_url}')
        response.append(res)
    return response


def get_breed(path):
    print(f'\t{path}')
    d = {}
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

    headers = {'User-Agent': user_agent, }

    request = urllib.request.Request(
        path, None, headers)  # The assembled request
    response = urllib.request.urlopen(request)

    mybytes = response.read()
    html_doc = mybytes.decode("utf8")
    response.close()

    soup = BeautifulSoup(html_doc, 'html.parser')
    elems = soup.find_all("p", class_="tw-text-3")
    breed_name = soup.find("h1").text
    print(breed_name)
    for elem in elems:
        text = elem.text.strip().split(':')
        if len(text) == 2:
            if text[0].strip() not in d:
                d[text[0].strip()] = text[1].strip()
            else:
                d[text[0].strip()+"_"] = text[1].strip()

    elems = soup.find_all(
        "div", class_="breed-card")
    for elem in elems:
        try:
            scores = elem.find_all(
                'p', class_="tw-text-4 tw-font-bold tw-font-poppins text-right")
            score = scores[0].text.strip()
            scores = elem.find_all(
                'h3', class_="tw-text-3")
            score_title = scores[0].text.strip().replace(
                f"Le {breed_name} et ", "")
            score_title = score_title.replace(f"Le {breed_name}", "")

            d[score_title] = score
        except:
            pass
    return d


# tw-text-4 tw-font-bold tw-font-poppins text-right
