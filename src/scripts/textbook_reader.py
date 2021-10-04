import pandas as pd
import requests
import bs4
import string
import re
from collections import Counter
from textbook_reader_package import gen_title, words, letters, common_string, gen_author

start_url = input('What is the url of the first page of the textbook? ')
end_url = input('What is the url of the last page of the textbook? ')

textbook_title = gen_title(start_url)
textbook_author = gen_author(start_url)

lo_urls = [start_url]
cons_url_prefix = common_string(start_url, end_url)
url = start_url
while end_url not in lo_urls:
    req = requests.get(url)
    soup = bs4.BeautifulSoup(req.text, 'lxml')
    next_url = soup.select(".next-button.button.toolbar-item")[0]['href']
    url = cons_url_prefix + next_url
    lo_urls.append(url)

unique_urls = set(lo_urls)
lo_urls_uniq = [url for url in unique_urls]

all_letters = ''
for url in lo_urls_uniq:
    all_letters += letters(url)
letter_counter = Counter(all_letters)

all_words = []
for url in lo_urls_uniq:
    all_words += words(url)
word_counter = Counter(all_words)

letter_dict = {}
for key in sorted(letter_counter.keys()):
    letter_dict[key] = letter_counter[key]

word_dict = {}
for key in sorted(word_counter.keys()):
    word_dict[key] = word_counter[key]

df_letters = pd.DataFrame(list(letter_dict.items()), columns=["Letter", "Frequency"])
df_words = pd.DataFrame(list(word_dict.items()), columns=["Word", "Frequency"])

letters_name = 'textbook_data/' + textbook_title + '_' + textbook_author + '_LetterData.csv'
words_name = 'textbook_data/' + textbook_title + '_' + textbook_author + '_WordData.csv'

df_letters.to_csv(letters_name, index=False)
df_words.sort_values(by='Frequency', ascending=False).to_csv(words_name, index=False)

print(f'Your two files have now been saved in "textbook_data", with names {letters_name} and {words_name}')
