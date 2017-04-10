import random
import time
import urllib2

from bs4 import BeautifulSoup

""" This is a bad joke maker.
    It uses the Unix words list, so the words_path may require
    adjusting in different environments."""

def get_full_path(path, file):
    full_path = path + file
    return full_path

def make_words_list(words_path):
    all_words = []
    open_words_list = open(words_path, "r")
    
    for line in open_words_list:
        if "'" not in line: # ignore stuff with apostrophes
            all_words.append(line)

    open_words_list.close()
    return all_words

def get_words_starting_with_letter(words, letter):
    words_starting_with_letter = []

    for line in words:
        if line.startswith(letter):
            words_starting_with_letter.append(line)
    return words_starting_with_letter

def get_stripped_words(words_starting_with_letter):
    stripped_words = []

    for word in words_starting_with_letter:
        stripped_words.append(word[1:])
    return stripped_words

def get_suitable_word(words_starting_with_letter, stripped_words, words):

    found_a_word = False

    while found_a_word == False:

        list_length = len(words_starting_with_letter)-1
        joke_word_index = random.randint(0, list_length)
        word_1 = words_starting_with_letter[joke_word_index]
        word_2 = stripped_words[joke_word_index]

        if word_2 in words:
            found_a_word=True

    return word_1, word_2

def remove_newline(word):

    word = word[:-1]
    return word

def read_page(url):
    page = urllib2.urlopen(url).read()
    return page

# TODO: handle error when there are no <li> tags
def get_definition(soup):

    meaning = soup.li.get_text()
    meaning = meaning.split("(") # there are two pairs of brackets, 
                                 # we want stuff between 2nd pair
    meaning = meaning[2]         # get stuff after 2nd opening bracket
    meaning = meaning.split(")") # cut out stuff after second closing bracket
    meaning = meaning[0] 
    return meaning

def print_joke(meaning_1, meaning_2, word_1, word_2):
    print "What's a word that means:"
    print meaning_1
    time.sleep(3)
    print "And can also be used to express appreciation for:"
    print meaning_2 + "?"
    time.sleep(5)
    print "That's right, " + word_1 + " (mmm," + word_2 + "!)"

words_path = "/usr/share/dict/"
words_file = "words"

path_to_words = get_full_path(words_path, words_file)

all_words = make_words_list(path_to_words)

m = "m"

words_starting_with_m = get_words_starting_with_letter(all_words, m)

stripped_words = get_stripped_words(words_starting_with_m)

word_1, word_2 = get_suitable_word(words_starting_with_m, stripped_words, all_words)

word_1 = remove_newline(word_1)
word_2 = remove_newline(word_2)

dictionary = "http://wordnetweb.princeton.edu/perl/webwn?s="

meaning_1_url = get_full_path(dictionary, word_1)
meaning_2_url = get_full_path(dictionary, word_2)

meaning_1_html = read_page(meaning_1_url)
meaning_2_html = read_page(meaning_2_url)

# TODO: change these variable names to something better than 'soup'
soup_1 = BeautifulSoup(meaning_1_html, 'html.parser')
soup_2 = BeautifulSoup(meaning_2_html, 'html.parser')

meaning_1 = get_definition(soup_1)
meaning_2 = get_definition(soup_2)

print_joke(meaning_1, meaning_2, word_1, word_2)
