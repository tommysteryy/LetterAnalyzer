import pandas as pd
import requests
import bs4
import string
import re
from collections import Counter

def words(url):
    '''
    Consumes a url of a webpage, produces a list of all the words used in the page
    '''
    req = requests.get(url)
    soup = bs4.BeautifulSoup(req.text, 'lxml')
    
    lowords = filter(lambda x: x != " ", soup.get_text().lower().replace('\n', ' ').translate(str.maketrans("", "", string.punctuation)).split(" "))
    
    lowords_lst = []
    for word in lowords:
        if word.isdigit():
            continue
        if len(word) == 0:
            continue
        elif word[0].isdigit():
            lowords_lst.append(word[1:])
        else:
            lowords_lst.append(word)
    return lowords_lst

def letters(url):
      
    '''
    Takes in url from any website, produces 1 long string of all the letters used on that page.
    '''
    req = requests.get(url)
    soup = bs4.BeautifulSoup(req.text, 'lxml')
    raw_text = soup.get_text().replace("\n", '').replace(' ', '')
    clean_letter_upper = ''.join(filter(lambda x: re.match("[\x41-\x5A]", x), raw_text)).lower()
    clean_letter_lower = ''.join(filter(lambda x: re.match("[\x61-\x7A]", x), raw_text)).lower()
    clean_letters = clean_letter_lower + clean_letter_upper
    return clean_letters

def gen_title(url):
    '''
    Given the url of a PreTeXT textbook website in 'lxml' form, return a string for the title of the textbook
    '''
    req = requests.get(url)
    soup = bs4.BeautifulSoup(req.text, 'lxml')
    title = soup.select('.BookBanner__TopBar-sc-1avy0c0-1.jVswHX')[0].select('a')[0].getText()
    title_clean = title.translate(str.maketrans("", "", string.punctuation)).replace(' ', '')
    return title_clean

def common_string(string1, string2):
    """
    Given two urls, provide the common url that was the base for the webpages. Must end on a / to prevent
    redundant half-strings at the end. E.g:
    
    start_url = 'https://faculty.uml.edu//klevasseur/ads/index-ads.html'
    end_url = 'https://faculty.uml.edu//klevasseur/ads/index-1.html'
    
    Want: 'https://faculty.uml.edu//klevasseur/ads/'
    NOT: 'https://faculty.uml.edu//klevasseur/ads/index-'    
    
    """
    
    def slash_end(string):
        """
        Recursively ensure that the last char of the string is a /
        assume: must have a / near the the end (if not THE end)
        
        """
        if string.endswith('/'):
            return string
        else:
            string = string[0:-1]
            return slash_end(string)
    
    common = ''
    for i in range(0, min(len(string1), len(string2))):
        if string1[i] == string2[i]:
            common += string1[i]
        if string1[i] != string2[i]:
            break
    
    result = slash_end(common)
    
    return result