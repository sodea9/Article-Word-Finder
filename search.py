# Author: Sean O'Dea
# Email: sodea@umass.edu
# Spire ID: 33851478

import urllib.request
import re
import string
import sys

def read_article_file(url):
    """
    Input: URL source
    Output: Article text in one string
    """
    req = urllib.request.urlopen(url)
    text = req.read()            # reads in text
    text = text.decode('UTF-8')  # decodes from bytes to text
    return text

def text_to_article_list(text):
    """
    Input: Article text as one string
    Output: List with each item being a different article
    """
    articles = re.split('<NEW ARTICLE>', text)
    for article in articles:
        if article == '':
            articles.remove(article) #gets rid of any blank items
    return articles

def split_words(bigString):
    """
    Input: article as one string
    Output: list of every sequential word in the article
    """
    splitString = bigString.splitlines() #splits by new lines
    i = 0
    words = []
    while i < len(splitString):
        temp = splitString[i]
        words.extend(temp.split()) #splits by spaces into separate words
        i += 1
    return words

def scrub_word(text):
    """
    Input: string containing word with punctuation
    Output: string containing word without punctuation
    """
    text = text.strip()                   #removes extra whitespace
    return text.strip(string.punctuation) #removes punctuation

def scrub_words(words):
    """
    Input: list of words from article
    Output: list of words in lowercase without punctuation
    """
    #removes punctuation of each word in list, ignores any remaining empty strings
    scrubbedWords = [scrub_word(word.lower()) for word in words if scrub_word(word.lower()) != '']
    return scrubbedWords

def build_article_index(article_list):
    """
    Input: list of strings containing article text
    Output: article index containing data of which articles each word can be found in
    """
    article_index = {}

    for (index, article) in enumerate(article_list):
        words = split_words(article)           
        scrubbedWords = scrub_words(words)          #splits current article's text into list of all contained words

        for word in scrubbedWords:
            if word in article_index:               #if the word is in the article_index
                article_index[word].add(index)      #add index of current article into associated set 
            else:
                article_index.update({word: {index}})   #else: update the article_index with a new keyword and set pair

    return dict(sorted(article_index.items()))      #returns alphabetized index; unsure if this is necessary

def find_words(keywords, index):
    """
    Input: List of keywords to search for, Article index
    Output: Set containing indexes of articles that contain all keywords
    """
    intersect_docs = set()
    for keyword in keywords:
        if keyword not in index:
            #returns empty set if one of the keywords isn't found in any article
            return set()
        elif len(intersect_docs) == 0:
            #if first keyword is checked, adds corresponding set from index to later compare to
            intersect_docs = index[keyword.lower()]
        else: 
            #compares current set and set of articles keyword is found in
            intersect_docs = intersect_docs.intersection(index[keyword.lower()])
    return intersect_docs

if __name__ == '__main__':
    articles = text_to_article_list(read_article_file(sys.argv[1])) #reads in given website

    #print command
    if sys.argv[2] == "print":
        print(articles[int(sys.argv[3])])       #prints given index from article list
    #find command
    elif sys.argv[2] == "find":
        index = build_article_index(articles)   #builds article index
        keywords = sys.argv[3].split()          #splits single string of words into list
        intersect = find_words(keywords, index) #finds intersections
        for num in intersect:
            print(num, end = ' ')
    else:
        print("Error: Unknown command")