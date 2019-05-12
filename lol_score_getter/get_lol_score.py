from email.mime.text import MIMEText
from smtplib import SMTP
import time

from bs4 import BeautifulSoup
import requests


SUMMONER_URL = 'https://eune.op.gg/summoner/userName=%CE%BD%CE%B1%CE%B3%CE%B7%CE%B5'


def get_summoner_score(summoner_url):
    resp = requests.get(summoner_url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    score_element = soup.find('meta', attrs={'name': 'description'})
    score_content = score_element.attrs['content']
    score_parts = score_content.split(' / ')

    return {
        'summoner_name': score_parts[0],
        'win_ratio': _parse_win_ratio(score_parts[2]),
        'champion_ratios': _get_per_champion_scores(score_parts[3])
    }


def _get_per_champion_scores(all_champions_string):
    champion_strings = all_champions_string.split(', ')

    champion_data = {}
    for champion_string in champion_strings:
        name, score = champion_string.split(' - ')
        champion_data[name] = _parse_win_ratio(score)

    return champion_data


def _parse_win_ratio(ratio_string):
    return int(ratio_string[-3:-1])


def send_mail_if_over_threshold(threshold: int):
    vayne_score = get_summoner_score(SUMMONER_URL)['win_ratio']
    if vayne_score >= threshold:
        print(f'Vayne ma {vayne_score}! Leci mail!')

        mail = MIMEText('O chuj! :)')
        mail['Subject'] = f'Vayne podbił do {vayne_score}!'
        with SMTP('localhost') as smtp:
            smtp.sendmail('dudus@prezydent.pl', 'abuk.ch@gmail.com', mail.as_string())
    else:
        print(f'Vayne nie ma {threshold}, ale za to ma {vayne_score}...')


def _run_loop():
    print('Zaczynam patrzenie na staty!')
    try:
        while True:
            print('Sprawdzam...')
            send_mail_if_over_threshold(49)
            time.sleep(60*10)
    except KeyboardInterrupt:
        print('Kończe patrzenie na staty! Dobranoc!')


if __name__ == '__main__':
    _run_loop()
