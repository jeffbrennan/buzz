import pandas as pd
from rymscraper import rymscraper, RymUrl
import json

def pull_rym():
    network = rymscraper.RymNetwork()
    # genre info etc
    # artist_info = network.get_artist_infos(name="Daft Punk")
    # json.dumps(artist_infos, indent=, ensure_ascii=False)

    # TODO: pull ratings from account

    music_list = []
    return music_list

#
# def pull_last_fm()
#     music_list = []
#     return music_list


def manage_scraping():
    rym_list = pull_rym()


def main():
    manage_scraping()


if __name__ == '__main__':
    main()
