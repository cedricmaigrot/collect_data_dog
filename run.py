import pandas as pd
from fci import scrapper as fci


df = pd.DataFrame(data=fci.run())
# df.to_excel("fci.xlsx")
df.to_csv("fci.csv")
df.to_json("fci.json")
