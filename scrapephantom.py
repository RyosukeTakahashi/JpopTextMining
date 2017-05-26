import sys
import json
import os
import requests
from selenium import webdriver
from bs4 import BeautifulSoup


# def artist_pages_suggested_by_search_term(search_term) return [{name:, id: },{name:, id: }]

# def get_song_count_of_artist(artist_id)

# def get_artist_song_search_page_urls(artist_pageid, song_count): 

# https://www.joysound.com/web/search/artist/3561?startIndex=0#songlist
# https://www.joysound.com/web/search/artist/3561?startIndex=20#songlist
# https://www.joysound.com/web/search/artist/3561?startIndex=40#songlist

# return search_page_urls

# song_urls_2d = map(lambda url:get_urls_of_songs_from_searchpage(searchpage_url) in search_page_urls:
# song_urls = [ item for innerlist in outerlist for item in innerlist ]

# def get_urls_of_songs_from_searchpage(searchpage_url):
# return [song_url, song_url]

# songpage_soups = map(lambda url:get_songpage_soup(url), song_urls)
# lyrics = map(lambda soup:get_lyric_text(songpage_soup), songpage_soups)

# def get_songpage_soup(url):
# def get_lyric_text(soup)

# for lyric in lyrics: output file

# def output_lyric_txtfile(soup)



def get_lyric_soup(url):
    # Selenium settings
    driver = webdriver.PhantomJS(service_log_path=os.path.devnull)
    # get a HTML response
    driver.get(url)
    html = driver.page_source.encode('utf-8')  # more sophisticated methods may be available
    # parse the response
    soup = BeautifulSoup(html, "lxml")
    # extract
    ## title
    lyric = soup.find("p", class_="ng-binding")
    print(lyric.get_text())
    
    # # output
    # output = {"lyric": lyric}
    # # write the output as a json file
    # with open(output_name, "w") as fout:
    #     jsonoutput = json.dump(output, fout, indent=4, sort_keys=True)

if __name__ == '__main__':

    url = "https://www.joysound.com/web/search/song/121447"
    get_lyric_soup(url)
    print("done")
    