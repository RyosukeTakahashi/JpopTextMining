import re

artist_name ="西野カナ"
lyric_file = open(artist_name + ".txt", 'r', encoding="utf-8")

lyric = lyric_file.read()

sub_words = ["Oh", "OH", "oh", "Yeah", "me", "my","be","La", "la", 
"your", "wanna","yeah","know","don't","So","up","It","You","baby","Eh",
"so","say","no","way","make","can","Hey","Yes","My","Me","with","what","just","Cp","ME",
"Hello","Dance"]

lyric_edited = lyric

for word in sub_words:
    lyric_edited = lyric_edited.replace(word, "")

lyric_edited_file = open(artist_name + "edited.txt", 'w', encoding='utf8')
lyric_edited_file.write(lyric_edited)