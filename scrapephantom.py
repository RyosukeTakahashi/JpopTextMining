import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import re
from collections import OrderedDict
import urllib.parse


def get_driver():
    des_cap = dict(DesiredCapabilities.PHANTOMJS)
    des_cap["phantomjs.page.settings.userAgent"] = (
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/28.0.1500.52 Safari/537.36'
    )

    driver = webdriver.PhantomJS(desired_capabilities=des_cap,service_log_path=os.path.devnull)

    return driver

def get_soup_of_url(url,driver):
    driver.get(url)
    html = driver.page_source.encode('utf-8')
    return BeautifulSoup(html, "lxml")
    

def artist_pages_suggested_by_search_term(search_term,driver) :

    keyword = urllib.parse.quote_plus(search_term, encoding='utf8')
    prefix = "https://www.joysound.com/web/search/cross?match=1&keyword="
    artist_suggest_url = prefix + keyword
    soup = get_soup_of_url(artist_suggest_url, driver).find("div", class_="jp-cmp-music-list-artist-001")

    suggestion_artistname_soups = soup.find_all("h3", class_="jp-cmp-music-title-001")
    artist_names = list(map(lambda h3: re.sub(r'\s|新曲あり',"",h3.get_text()), suggestion_artistname_soups))
    suggestion_a_soups = soup.find_all("a", class_="jp-cmp-link-block-002")
    suggestion_urls = list(map(lambda a: a["href"], suggestion_a_soups))
    suggestions = OrderedDict(zip(artist_names, suggestion_urls))

    return suggestions

def define_artist_from_user_input(suggestions, search_term):
    print("We seaarched for `{}` . Which one do you mean?".format(search_term))
    
    for i, (name, url) in enumerate(suggestions.items()):
        print("{} : {}".format(i+1, name))

    num = 0
    while num < 1 or num > len(suggestions.items()):
        try:
            num = int(input("choose a valid number and press enter."))
        except:
            print("choose a number")

    artist_info = list(suggestions.items())[num-1]
    print(artist_info)
    return artist_info

def get_song_count_of_artist(artist_info, driver):

    artist_id = artist_info[1]
    searchresult_url = \
            "https://www.joysound.com/web/{0}".format(artist_id)
    soup = get_soup_of_url(searchresult_url, driver)
    song_count_text = soup.find('em', class_="ng-binding ng-scope").get_text()
    song_count = re.sub(r'件[.\s\S]+', "", song_count_text)
    print("{0} songs for {1}.".format(song_count, artist_info[0]))

    return int(song_count)


def get_artist_search_page_urls(artist_pageid, song_count): 
    base_searchpage_url = \
            "https://www.joysound.com/web/{0}/?startIndex=XX#songlist"\
            .format(artist_pageid)

    song_counts_about = int(song_count/20) * 20 + 1
    search_page_urls = [base_searchpage_url.\
            replace("XX", str(x)) for x in range(0, song_counts_about, 20)]

    return search_page_urls


def get_all_song_urls_from_search_page_urls(search_page_urls, driver):
    song_urls_2d = map(lambda url: get_20urls_of_songs_from_searchpage(url, driver), search_page_urls)

    flattened_song_urls = [item for innerlist in song_urls_2d for item in innerlist]
    return flattened_song_urls


def get_20urls_of_songs_from_searchpage(searchpage_url, driver):
    soup = get_soup_of_url(searchpage_url, driver)
    song_a_soups = soup.find_all("a", class_="jp-cmp-table-column")
    song_urls = list(map(lambda a: a["href"], song_a_soups))

    return song_urls

def generate_textfiles(all_song_directories, artist_dir, driver):
    lyrics_data = map(lambda directory: get_lyric_data(directory, driver), all_song_directories)
    print("start getting lyrics")
    for lyric in lyrics_data:
        lyricfile = open(artist_dir + "/" + lyric["id"] + "_" + lyric["title"] + '.txt', 'w', encoding='utf-8')
        lyricfile.write(lyric["text"])
        lyricfile.close()


def get_lyric_data(directory, driver):
    print(directory)
    soup = get_soup_of_url("https://www.joysound.com" + directory, driver)
    title_tag = re.sub(r'[¥/:*?"<>|]', "", soup.find("title").get_text())
    lyric_soup = soup.find("p", class_="ng-binding")
    print(lyric_soup)

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

def main(artist_name):

    driver = get_driver()

    artist_dir = make_artist_directory(artist_name)
    suggestions = artist_pages_suggested_by_search_term(artist_name, driver)
    artist_info = define_artist_from_user_input(suggestions, artist_name)

    driver = get_driver()
    song_count = get_song_count_of_artist(artist_info, driver)

    artist_pageid = artist_info[1]
    search_page_urls = get_artist_search_page_urls(artist_pageid, song_count)
    all_song_directories = get_all_song_urls_from_search_page_urls(search_page_urls, driver)

    driver = get_driver()
    generate_textfiles(all_song_directories, artist_dir, driver)

if __name__ == '__main__':
    artist_name = "スガシカオ"
    main(artist_name)
    wordcloud.main(artist_name)

