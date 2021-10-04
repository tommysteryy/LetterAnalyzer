import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
import requests
import bs4
import string
import re

textbook_name = input("What is the name of the file of the textbook you would like to create a wordcloud for? \n "
                      "Do NOT include the file extension, such as '.csv': \n")
while not (textbook_name.__contains__("WordData") and not textbook_name.__contains__(".csv")):
    textbook_name = input("Invalid input. Must be a file that contains word data. Please try again: ")

df = pd.read_csv('textbook_data/' + textbook_name + ".csv")[:200]

url = "https://en.wikipedia.org/wiki/Most_common_words_in_English"
req = requests.get(url)
soup = bs4.BeautifulSoup(req.text, 'lxml')
all_words = soup.select('.extiw')
lo_common_words = []
for n in range(0, 100):
    lo_common_words.append(all_words[n].get_text())
lo_common_words += ['are', 'is']

## custom words, ADD MORE IF NECESSARY
lo_common_words += ['hphantom0000', 'beginequation', 'endequation', 'displaystyle', 'is',
                    'questionscritical', 'questionspersonal']
lo_common_words += ['termssummaryreview', 'openstax', 'are', 'was', "displaystyle"]
lo_common_words += ['summaryselfcheck', 'questionsreview', 'termskey', 'text', "beginalign", "endalign" ]

df_clean = df[~df["Word"].isin(lo_common_words)]

## making a dictionary for the wordcloud
word_dict = {}
for word, freq in df_clean.values:
    word_dict[word] = freq

wordcloud = WordCloud(width=900, height=700, min_font_size=20, background_color="white", margin=9)
wordcloud.generate_from_frequencies(frequencies=word_dict)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")

wordcloud_name = textbook_name.replace("WordData", "WordCloud")
wordcloud.to_file("wordclouds/" + wordcloud_name + ".png")
print("Your word cloud has now been saved to " + "wordclouds/" + wordcloud_name)
