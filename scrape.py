import requests
import lxml.html as lh
import pandas as pd
import sqlite3

conn = sqlite3.connect('TestDB2.db')
c = conn.cursor()
c.execute('CREATE TABLE ggs (Profile text, Name text, Short text, Korean_Name text, Debut text, Company text)')
conn.commit()
url = "https://dbkpop.com/db/k-pop-girlgroups"

# Create a handle, page, to handle the contents of the website
page = requests.get(url)
# Store the contents of the website under doc
doc = lh.fromstring(page.content)
# Parse data that are stored between <tr>..</tr> of HTML
tr_elements = doc.xpath('//tr')
col = []
i = 0
# For each row, store each first element (header) and an empty list
for t in tr_elements[0]:
    i += 1
    name = t.text_content()
    col.append((name, []))

for j in range(1, len(tr_elements)):
    # T is our j'th row
    T = tr_elements[j]

    # If row is not of size 10, the //tr data is not from our table
    if len(T) != 10:
        break

    # i is the index of our column
    i = 0

    # Iterate through each element of the row
    for t in T.iterchildren():
        data = t.text_content()
        # Check if row is empty
        if i > 0:
            # Convert any numerical value to integers
            try:
                data = int(data)
            except:
                pass
        # Append the data to the empty list of the i'th column
        col[i][1].append(data)
        # Increment i for the next column
        i += 1

Dict = {title: column for (title, column) in col}
pd.DataFrame(Dict).to_sql('ggs', conn, if_exists='replace', index=True)
c.execute("SELECT * FROM ggs")

for row in c.fetchall():
    print(row)
