from sqlalchemy import create_engine, Float
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from sqlalchemy import Boolean
from sqlalchemy.types import Integer, Text, DateTime


### SQL ALCHEMY
table_name = "idols"
db_uri = "postgres+psycopg2://postgres:postgres@localhost:5432/postgres"
engine = create_engine(db_uri, echo=True)
###

## Selenium
browser = webdriver.Chrome()
browser.get('https://dbkpop.com/db/all-k-pop-idols')
#browser.find_element_by_xpath("//*[@id='table_1_next']").click()


soup = BeautifulSoup(browser.page_source, 'html.parser')
browser.quit()
##


## Data Gen
table = soup.find("table")
table_data = [[cell.text for cell in row.find_all(["th", "td"])][1:]
                        for row in table.find_all("tr")][1:]
df = pd.DataFrame(table_data)
df.columns = df.iloc[0, :]
df.drop(index=0, inplace=True)
print(df.head())

df.to_sql(
    table_name,
    engine,
    if_exists='append',
    index=True,
    chunksize=500,
    dtype={
        "stage_name": Text,
        "full_name": Text,
        "korean_name": Text,
        "korean_stage_name": Text,
        "birthdate": DateTime,
        "birthplace": Text,
        "group": Text,
        "other_group": Text,
        "former_group": Text,
        "country": Text,
        "second_country": Text,
        "height": Integer,
        "weight": Float,
        "debut": DateTime,
        "gender": Text,
        "position": Text,
    }
)
