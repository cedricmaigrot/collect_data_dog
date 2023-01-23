import os

from fci import scrapper as fci
from laspa import scrapper as laspa
from wamiz import scrapper as wamiz

if not os.path.exists("data"):
    os.makedirs("data")

data = fci.run()
data = laspa.run()
data = wamiz.run()
