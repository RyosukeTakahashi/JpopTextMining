import unittest
import scrapephantom
import os
import re

class TestScrapePhantom(unittest.TestCase):

    @unittest.skip("time")
    def test_artist_suggest(self):

        search_term = "西野カナ"
        output = scrapephantom.artist_pages_suggested_by_search_term(search_term)
        # expected = {
        #     "西野カナ": "https://www.joysound.com/web/search/artist/49968",
        #     "INFINITY 16 welcomez MINMI&amp;西野カナ": "https://www.joysound.com/web/search/artist/208583"
        # }
        expected = dict(zip(["西野カナ", "INFINITY 16 welcomez MINMI&amp;西野カナ"],
        "https://www.joysound.com/web/search/artist/49968",["https://www.joysound.com/web/search/artist/208583"]))

        self.assertEqual(output, expected)

    @unittest.skip("timesave")
    def test_get_search_page_urls(self):

        artist_pageid = 3561
        song_count = 263
        output = scrapephantom.get_artist_search_page_urls(artist_pageid, song_count)
        expected = ["https://www.joysound.com/web/search/artist/3561?startIndex=0#songlist", \
                    "https://www.joysound.com/web/search/artist/3561?startIndex=20#songlist"]
        self.assertEqual(output[:2], expected)
        expected = ["https://www.joysound.com/web/search/artist/3561?startIndex=220#songlist", \
                    "https://www.joysound.com/web/search/artist/3561?startIndex=240#songlist"]
        self.assertEqual(output[-2:], expected)

    @unittest.skip("ok")
    def test_get_song_count(self):
        artist_tuple = ("AKB48", "43285")

        output = scrapephantom.get_song_count_of_artist(artist_tuple)
        expected = 570
        self.assertEqual(output, expected)

    @unittest.skip("time saver")
    def test_get_all_song_urls_from_search_page_urls(self):

        search_page_urls = ["https://www.joysound.com/web/search/artist/3561?startIndex=0#songlist", \
                            "https://www.joysound.com/web/search/artist/3561?startIndex=20#songlist"]

        output = scrapephantom.get_all_song_urls_from_search_page_urls(search_page_urls)
        expected = ["/web/search/song/121447",\
                    "/web/search/song/12554"]
        self.assertEqual(output[:2], expected)
        expected = ["/web/search/song/159892",\
                    "/web/search/song/126265"]
        self.assertEqual(output[-2:], expected)


    @unittest.skip("skippin for driver reading cost")
    def test_get_urls_of_songs_from_searchpage_url(self):

        searchpage_url = "https://www.joysound.com/web/search/artist/3561?startIndex=0#songlist"

        output = scrapephantom.get_20urls_of_songs_from_searchpage(searchpage_url)

        expected = ["/web/search/song/121447",\
                    "/web/search/song/12554"]
        self.assertEqual(output[:2], expected)

    @unittest.skip("time saving")
    def test_generate_textfile(self):
        all_song_directories = ["/web/search/song/159892"]
        artist_dir = "artists/Mr.Children"
        scrapephantom.generate_textfiles(all_song_directories, artist_dir)



    @unittest.skip("skippin for driver reading cost")
    def test_get_lyric_text(self):

        directory = "/web/search/song/12554" 
        output = scrapephantom.get_lyric_data(directory)

        expected = "Uh... Oh..."
        self.assertEqual(output.split("\n")[-1], expected)

    @unittest.skip("noneed")
    def test_make_artist_directory(self):

        artist_name = "RADWIMPS"
        scrapephantom.make_artist_directory(artist_name)
        self.assertTrue(os.path.exists("artists/Mr.Children"))

    @unittest.skip("noneed")
    def test_replace(self):
        text = "なんでもないや (movie ver.)／RADWIMPS-カラオケ・歌詞検索｜JOYSOUND.com"
        expected = "なんでもないや (movie ver.)"
        output = re.sub(r'／.*', "", text)
        print(output)
        self.assertEqual(expected, output)

    


if __name__ == '__main__':

    # dir = "artists/平井堅"
    # files = os.listdir(dir)
    # for file in files:
    #     print(file)
    #     if "JOYSOUND" in file:
    #         os.remove(dir + "/" +file)


    unittest.main()


