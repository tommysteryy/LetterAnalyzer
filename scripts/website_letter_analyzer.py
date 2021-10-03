import pandas as pd
from collections import Counter
import requests
import bs4
import re
import matplotlib.pyplot as plt
from textbook_reader_package import gen_title, words, letters, common_string, gen_author


url = input("What website would you like to analyze? Input your url here: ")
req = requests.get(url)
soup = bs4.BeautifulSoup(req.text, 'lxml')
raw_text = soup.get_text().replace("\n", '').replace(' ', '')

clean_text_lower = ''.join(filter(lambda x: re.match("[\x41-\x5A]", x), raw_text)).lower()
clean_text_upper = ''.join(filter(lambda x: re.match("[\x61-\x7A]", x), raw_text)).lower()
clean_text = clean_text_lower + clean_text_upper

clean_numbers = ''.join(filter(lambda x: re.match(r"[0-9]",x), raw_text))
clean_all = clean_text + clean_numbers

total_alpha = len(clean_text)
total_digits = len(clean_numbers)
total = len(clean_all)

alpha = Counter(clean_text)
num = Counter(clean_numbers)
both = Counter(clean_all)

alpha_dict = {}
for key in sorted(alpha.keys()):
	alpha_dict[key] = alpha[key]/total_alpha

num_dict = {}
for key in sorted(num.keys()):
	num_dict[key] = num[key]/total_digits
    
both_dict = {}
for key in sorted(both.keys()):
	both_dict[key] = both[key]/total

# df_alpha = pd.DataFrame(list(alpha_dict.items()), columns = ["Letter", "Frequency"])
# df_alpha.plot(x = "Letter", kind = 'bar', title = "Letter Frequency by letter", figsize = (10,5))

# df_both = pd.DataFrame(list(both_dict.items()), columns = ["Letter", "Frequency"])
# df_both.plot(x = "Letter", kind = 'bar', title = "Letter Frequency by letter", figsize = (10,5))

lo_words = words(url)
web_title = "Sample Title"
words_name = 'Textbook_Data\\' + web_title + "_" + '_WordData.csv'

word_counter = Counter(lo_words)

word_dict = {}
for key in sorted(word_counter.keys()):
	word_dict[key] = word_counter[key]

df_words = pd.DataFrame(list(word_dict.items()), columns = ["Word", "Frequency"])
df_words.sort_values(by = 'Frequency', ascending = False).to_csv(words_name, index = False)
