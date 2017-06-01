import os
from functools import reduce

def get_text_files(artist_name):
    artist_directory = "artists/{0}/".format(artist_name)
    filenames = os.listdir(artist_directory)
    texts = map(lambda x:read_file_content(artist_directory + x) , filenames)

    return texts

def read_file_content(file_directory):

    lyricfile = open(file_directory,'r', encoding="utf-8")
    lyric_str = lyricfile.read()
    lyricfile.close()
    return lyric_str

def main(artist_name):

    texts = list(get_text_files(artist_name))
    all_texts = reduce(lambda a,b: a + b, texts)
    all_texts_file = open("minedLyrics/" + artist_name + ".txt", 'w', encoding="utf-8")
    all_texts_file.write(all_texts)
    print("lyrics merged")


if __name__ == '__main__':
    
    main("スガシカオ") #必要なら引数与える
