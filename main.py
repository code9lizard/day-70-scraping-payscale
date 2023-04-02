import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
import requests

rank = []
major = []
early_career_pay = []
mid_career_pay = []
high_meaning = []

for page_num in range(1, 35):
    PAYSCALE_URL = f"https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors/page/{page_num}"
    response = requests.get(PAYSCALE_URL).text
    soup = BeautifulSoup(response, "html.parser")
    table = soup.find_all("tr", attrs={"class": "data-table__row"})

    for row in table:
        table_row_element = row.find_all("span", attrs={"class": "data-table__value"})
        rank.append(table_row_element[0].text)
        major.append(table_row_element[1].text)
        early_career_pay.append(int(table_row_element[3].text.replace("$", "").replace(",", "")))
        mid_career_pay.append(int(table_row_element[4].text.replace("$", "").replace(",", "")))
        high_meaning.append(int(table_row_element[5].text.replace("%", "").replace("-", "0")))

payscale_details = {
    "Rank": rank,
    "Major": major,
    "Early Career Pay": early_career_pay,
    "Mid-Career Pay": mid_career_pay,
    "High Meaning": high_meaning,
}

df = pd.DataFrame.from_dict(payscale_details)
df = df.replace(0, np.nan)
df.to_csv("college_major_salaries.csv", index=False)
