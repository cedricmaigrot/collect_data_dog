import os

from fci import scrapper as fci
from laspa import scrapper as laspa

if not os.path.exists("data"):
    os.makedirs("data")

data = fci.run()
# data = laspa.run()
