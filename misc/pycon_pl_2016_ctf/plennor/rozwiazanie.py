from itertools import permutations
from bs4 import BeautifulSoup
import requests


def extract_number(td):
    return float(td.text)

resp = requests.get('http://139.59.208.213/UKBWBNGQ/pelennor/')
soup = BeautifulSoup(resp.text, 'html.parser')

tds = soup.find_all('td')

rates = [
    [extract_number(td) for td in tds[0:3]],
    [extract_number(td) for td in tds[5:8]],
    [extract_number(td) for td in tds[10:13]],
]

for zestaw in rates:
    print(zestaw)

max_gain = -1000000
for permut in permutations([0,1,2]):
    gain = 0
    for rate in rates:
        gain +=
