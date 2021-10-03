import pandas as pd
from collections import Counter
import requests
import bs4
import re
import matplotlib.pyplot as plt
from openbc_reader_package import words, letters, common_string, gen_title


url1 = input('What is the first url of the textbook? ')
url2 = input("What is another url of the textbook? ")

req = requests.get(url1)
soup = bs4.BeautifulSoup(req.text, "lxml")
common_url = common_string(url1, url2)

lo_url = []
lo_chapters = soup.select('.styled__NavItem-sc-18yti3s-2.lcPtic')

for chapter in lo_chapters:
    lo_subchapters = chapter.select('a')
    for subchapter in lo_subchapters:
        lo_url.append(common_url + subchapter['href'])

unique = set(lo_url)
lo_url_unique = [url for url in unique]

all_letters = ''
for url in lo_url_unique:
    all_letters += letters(url)
letter_counter = Counter(all_letters)

all_words = []
for url in lo_url_unique:
    all_words += words(url)
word_counter = Counter(all_words)

letter_dict = {}
for key in sorted(letter_counter.keys()):
	letter_dict[key] = letter_counter[key]
    
word_dict = {}
for key in sorted(word_counter.keys()):
	word_dict[key] = word_counter[key]

df_letters = pd.DataFrame(list(letter_dict.items()), columns = ["Letter", "Frequency"])
df_words = pd.DataFrame(list(word_dict.items()), columns = ["Word", "Frequency"])

author_name = "OpenBCEducation"
title_name = gen_title(url1)

letters_name = 'Textbook_Data\\' + title_name + "_" + author_name +'_LetterData.csv'
words_name = 'Textbook_Data\\' + title_name + "_" + author_name +'_WordData.csv'

df_letters.to_csv(letters_name, index = False)
df_words.sort_values(by = 'Frequency', ascending = False).to_csv(words_name, index = False)

print(f'Your two files have now been saved in "Textbook_Data", with names {letters_name} and {words_name}')