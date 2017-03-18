import random
import time
import urllib2

from bs4 import BeautifulSoup

""" This is a bad joke maker.
    It uses the Unix words list, so the words_path may require
    adjusting in different environments."""

words_path = "/usr/share/dict/"
words_file = "words"
words_list = words_path + words_file
all_words = []
open_words_list = open(words_list, "r")

for line in open_words_list:
    if "'" not in line: # ignore stuff with apostrophes
        all_words.append(line)

open_words_list.close()

words_starting_with_m = []

for line in all_words:
    if line.startswith("m"):
        words_starting_with_m.append(line)

stripped_words = []

for word in words_starting_with_m:
    stripped_words.append(word[1:])


found_a_word = False

while found_a_word == False:

    joke_word_index = random.randint(0, len(words_starting_with_m)-1)
    word_1 = words_starting_with_m[joke_word_index]
    word_2 = stripped_words[joke_word_index]

    if word_2 in all_words:
        found_a_word=True

# Yeah, this is where I decided I should go to bed soon and just put in 
# the first thing that worked even slightly. TODO: tidy up.

word_1 = word_1[:-1]
word_2 = word_2[:-1]
dictionary = "http://wordnetweb.princeton.edu/perl/webwn?s="
meaning_1_url = dictionary+word_1
meaning_2_url = dictionary+word_2

meaning_1_html = urllib2.urlopen(meaning_1_url).read()
meaning_2_html = urllib2.urlopen(meaning_2_url).read()

soup1 = BeautifulSoup(meaning_1_html, 'html.parser')
soup2 = BeautifulSoup(meaning_2_html, 'html.parser')

meaning_1 = soup1.li.get_text()
meaning_1 = meaning_1.split("(n)")
meaning_1 = meaning_1[-1][len(word_1)+2:]

meaning_2 = soup2.li.get_text()
meaning_2 = meaning_2.split("(n)")
meaning_2 = meaning_2[-1][len(word_1)+2:]

print "What's a word that means:"
print meaning_1
print "And can also be used to express appreciation for:"
print meaning_2
print "?"
time.sleep(3)
print "That's right, " + word_1 + " (mmm," + word_2 + "!)"
