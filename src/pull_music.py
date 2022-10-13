import pandas as pd
from rymscraper import rymscraper, RymUrl
import json
import requests
from io import StringIO


def parse_rym(response_text):
    user_reviews = pd.read_csv(StringIO(response_text))
    user_reviews.columns = user_reviews.columns.str.strip()
    user_reviews.columns = user_reviews.columns.str.replace(' ', '_')
    user_reviews.fillna('', inplace=True)
    user_reviews['Artist'] = user_reviews['First_Name'] + ' ' + user_reviews['Last_Name']
    user_reviews['Artist'] = user_reviews['Artist'].str.strip()
    artist_list = list(set(user_reviews['Artist']))

    artist_list_clean = [x.replace('&amp;', '&') for x in artist_list]
    return artist_list_clean


def get_new_releases(artist_list, day_filter=30):
    network = rymscraper.RymNetwork()
    # TODO: implement multiprocessing on list of artists - runtime > 1 sec per artist
    artist_discography = network.get_discography_infos(name=artist_list[0])
    release_dates = [x['Date'] for x in artist_discography]

    return new_release


# TODO: add cookie grabber
def pull_rym(rym_user='jeff'):
    user_credentials = CREDENTIALS[CREDENTIALS.user == rym_user]

    cookies = {
        'sec_bs': user_credentials['sec_bs'],
        'sec_ts': user_credentials['sec_ts'],
        'sec_id': user_credentials['sec_id'],
        'ulv': user_credentials['ulv'],
        'is_logged_in': '1',
        'username': user_credentials['username']
    }

    headers = {
        'authority': 'rateyourmusic.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9,es;q=0.8',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'sec_bs=3be019af3a466a6d1ec874f266cedb39; sec_ts=1665694946; sec_id=55ab9625a74610bdd21a542c5b25543d; ulv=1h4xx98AmooybnYFyxnKgYwnbKnpg0eUcp3ipGb8QjNYWlPxtHBnKW6ia75Dohx11644339695643305; is_logged_in=1; username=Albinodino',
        'dnt': '1',
        'referer': 'https://rateyourmusic.com/~Albinodino',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    }

    album_list_id = user_credentials['review_id']

    response = requests.get(f'https://rateyourmusic.com/user_albums_export?album_list_id={album_list_id}&noreview',
                            cookies=cookies, headers=headers)

    artist_list = parse_rym(response.text)
    new_releases = get_new_releases(artist_list)

    return new_releases

#
# def pull_last_fm()
#     music_list = []
#     return music_list


def manage_scraping(user):
    rym_releases = pull_rym(user)
#     TODO: export/pass to deezer


def main():
    user = 'jeff'
    manage_scraping(user)


if __name__ == '__main__':
    CREDENTIALS = pd.read_csv('backend/rym_login_info.csv')
    main()
