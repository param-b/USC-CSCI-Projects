import re
from collections import defaultdict
import sys
import os
import glob
import json

class PreProcessData():
    def __init__(self, content):
        self.content = content

    def lower_case_data(self):
        #self.content = self.content.strip()
        self.content = self.content.lower()
        return self.content
        
    def load_stop_words(self):
        stop_words = defaultdict(int)
        with open('stopwords.txt', 'r') as stop_word_file:
            stop_words_content = stop_word_file.read()
            #print("Stop Words:" + stop_words_content)
            for word in stop_words_content.split():
                stop_words[word] = 1
        self.stop_words = stop_words        

    def remove_stop_words(self):
        all_word = self.content.split()
        temp = []
        #temp = [word.strip() if self.stop_words[temp] != 1]
        #self.content = ' '.join()
        for word in all_word:
            if word.isnumeric():
                temp.append("<NUM>")
            elif self.stop_words[word] != 1:
                temp.append(word)
        return temp

    def keep_only_alphabets(self):
        #print(self.content)
        alpha_regex = re.compile('[^a-zA-Z1-9 ]')
        self.content = alpha_regex.sub('',self.content)
        #print(self.content)
        return self.content

    def pre_process_data(self):
        self.content = self.lower_case_data()
        self.content = self.keep_only_alphabets()
        #self.load_stop_words()
        #if len(self.stop_words) > 0:
        #return self.remove_stop_words()
        return self.content
