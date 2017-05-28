import sys
import os
from selenium import webdriver
from bs4 import BeautifulSoup
import re
from collections import OrderedDict
import urllib.parse

def artist_pages_suggested_by_search_term(search_term) :

    artist_suggest_url = "https://www.joysound.com/web/search/cross?match=1&keyword=" + search_term

    driver = webdriver.PhantomJS(service_log_path=os.path.devnull)
    driver.get(artist_suggest_url)
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "lxml").find("div", class_="jp-cmp-music-list-artist-001")
    

    suggestion_artistname_soups = soup.find_all("h3", class_="jp-cmp-music-title-001")
    artist_names = list(map(lambda h3: re.sub(r'\s',"",h3.get_text()), suggestion_artistname_soups))
    suggestion_a_soups = soup.find_all("a", class_="jp-cmp-link-block-002")
    suggestion_urls = list(map(lambda a: a["href"], suggestion_a_soups))

    suggestions = dict(zip(artist_names, suggestion_urls))
    print(suggestions)

    return suggestions

# def get_song_count_of_artist(artist_id)


def get_artist_search_page_urls(artist_pageid, song_count): 
    base_searchpage_url = \
            "https://www.joysound.com/web/search/artist/{0}?startIndex=XX#songlist"\
            .format(artist_pageid)

    song_counts_about = int(song_count/20) * 20
    search_page_urls = [base_searchpage_url.\
            replace("XX", str(x)) for x in range(0, song_counts_about, 20)]

    return search_page_urls


def get_all_song_urls_from_search_page_urls(search_page_urls):
    song_urls_2d = map(lambda url: get_20urls_of_songs_from_searchpage(url), search_page_urls)

    flattened_song_urls = [item for innerlist in song_urls_2d for item in innerlist]
    return flattened_song_urls


def get_20urls_of_songs_from_searchpage(searchpage_url):
    driver = webdriver.PhantomJS(service_log_path=os.path.devnull)
    driver.get(searchpage_url)
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "lxml")

    song_a_soups = soup.find_all("a", class_="jp-cmp-table-column")
    song_urls = list(map(lambda a: a["href"], song_a_soups))

    return song_urls

def generate_textfiles(all_song_directories, artist_dir):
    print("running")
    lyrics_data = map(lambda directory: get_lyric_data(directory), all_song_directories)
    print("got lyrics")
    for lyric in lyrics_data:
        lyricfile = open(artist_dir + "/" + lyric["id"] + "_" + lyric["title"] + '.txt', 'w', encoding='utf-8')
        lyricfile.write(lyric["text"])
        lyricfile.close()


def get_lyric_data(directory):
    home_url = "https://www.joysound.com"
    driver = webdriver.PhantomJS(service_log_path=os.path.devnull)
    driver.get(home_url + directory)
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "lxml")
    title_tag = re.sub(r'[¥/:*?"<>|]', "", soup.find("title").get_text())
    lyric_soup = soup.find("p", class_="ng-binding")

    lyric_data = {
        "title": re.sub(r'／.*', "", title_tag),
        "id": directory.replace("/web/search/song/", ""),
        "text": lyric_soup.get_text().rstrip("\n")
    }

    return lyric_data


def make_artist_directory(artist_name):
    directory = "artists/{0}".format(artist_name)
    if not os.path.exists(directory):
        os.makedirs(directory)

    return directory


def main():
    artist_name = "AKB48"
    artist_pages_suggested_by_search_term(artist_name)
    # artist_pageid = 43285
    # song_count = 570
    # artist_dir = make_artist_directory(artist_name)

    # search_page_urls = get_artist_search_page_urls(artist_pageid, song_count)
    # all_song_directories = get_all_song_urls_from_search_page_urls(search_page_urls)
    # generate_textfiles(all_song_directories, artist_dir)

if __name__ == '__main__':

    main()
