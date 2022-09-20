from codecs import backslashreplace_errors
from tarfile import TarFile
from turtle import back
from typing import DefaultDict
from unittest import result
import re
from collections import defaultdict
import sys
import os
import glob
import json
import math


def read_files(file_path):
    # Read all the Data from the Path
    wordList = []
    with open(file_path, mode = 'r', encoding = 'UTF-8') as file_obj:   
        all_sentences = file_obj.read().split('\n')
        for single_sentence in all_sentences:
            single_sentence_array = single_sentence.strip().split()
            temp = []
            for single_word_pair in single_sentence_array:
                temp.append(single_word_pair.strip())  
            wordList.append(temp)          
    return wordList

def clean_file():
    pass

def load_data():
    
    allTagsCount = defaultdict(int)
    allWords = defaultdict(int)
    disregardWordCount = defaultdict(int)
    openClassTag = defaultdict(int)

    wordvsTagProbs = {}
    tagtoTagProbs = {}
    with open('hmmmodel.txt', 'r',encoding = 'UTF-8') as file_obj:
        result = json.load(file_obj)

        tagtoTagProbs =  result['Tag to Tag']
        allTagsCount = defaultdict(int,result['All Tags Count'])
        wordvsTagProbs = result['Word vs Tag']
        allWords = defaultdict(int,result['All Words'])
        disregardWordCount = defaultdict(int, result['Disregard Word Count'])
        openClassTag =  defaultdict(int,result['Open Class Tag'])

    return tagtoTagProbs, allTagsCount, wordvsTagProbs, allWords, disregardWordCount, openClassTag

def tag_sentence(sentence, backpointer):
    final_answer = ''
    back_pointer_len =  len(backpointer) - 1
    startTag = '<END>'
    i = len(sentence)
    j = i - 1

    current_tag = backpointer[i][startTag]
    #if(i == back_pointer_len):
    final_answer = sentence[j] + "/" + current_tag
    startTag = current_tag
    i -= 1
    j -= 1

    while i  >= 1: # i-1>=0 Initial Condition
        current_tag = backpointer[i][startTag]
        final_answer = sentence[j] + "/" + current_tag + " " + final_answer
        startTag = current_tag
        i -= 1
        j -= 1 
    return final_answer


def perform_viterbi(tagtoTag, allTagsCount, wordvsTag, allWords, disregardWordCount, sentence, openClassTag):

    viterbi = defaultdict(lambda: defaultdict(float))
    backpointer = defaultdict(lambda: defaultdict(str))

    sentenceLength = len(sentence)

    # Performing initial step at i = 0 
    firstWord = sentence[0]
    if allWords[firstWord] == 1:
        #current_emission_prob = 1.0
        for next_tag in wordvsTag[firstWord].keys():
            if next_tag == "<START>":
                continue
            viterbi[0][next_tag] = wordvsTag[firstWord][next_tag]*disregardWordCount[firstWord] + tagtoTag['<START>'][next_tag]
            backpointer[0][next_tag] = '<START>'
    else:
        for next_tag in tagtoTag["<START>"].keys():
            if next_tag == "<START>" or next_tag=="<END>":
                continue
            viterbi[0][next_tag] = tagtoTag['<START>'][next_tag]
            backpointer[0][next_tag] = '<START>'        

    # Performing recursion step from i = 1 to N-1
    for inx in range(1, sentenceLength):
        
        #curr_states  = []n
        current_word = sentence[inx]
        if allWords[current_word] == 1:
            for current_tag in wordvsTag[current_word].keys():
                # You can change this to all tags also.
                max_prob = float('-inf')
                max_res = ''
                current_emission = wordvsTag[current_word][current_tag]

                for prev_tag in viterbi[inx-1]:
                    try:
                        current_prob = viterbi[inx-1][prev_tag] + current_emission*disregardWordCount[current_word] + tagtoTag[prev_tag][current_tag]
                        if current_prob > max_prob:
                            max_prob = current_prob
                            max_res = str(prev_tag)
                    except KeyError:
                        continue
                
                viterbi[inx][current_tag]  = max_prob
                backpointer[inx][current_tag] = max_res
        else:
            for current_tag in openClassTag.keys():
                if current_tag != '<START>' and current_tag != '<END>':
                    max_prob = float('-inf')
                    max_res = ''
                    current_emission = 0
                    for prev_tag in list(viterbi[inx-1]):
                        try:
                            current_prob = viterbi[inx-1][prev_tag] + current_emission + tagtoTag[prev_tag][current_tag]
                            if current_prob > max_prob:
                                max_prob = current_prob
                                max_res = str(prev_tag)
                        except KeyError:
                            continue
                    
                    viterbi[inx][current_tag]  = max_prob
                    backpointer[inx][current_tag] = max_res
    
    # Performing last step at i = N

    """
    lastWord = sentence[-1]
    if allWords[lastWord] == 1:
            for current_tag in wordvsTag[lastWord].keys():
                max_prob = float('inf')
                max_res = ''
                current_emission = wordvsTag[current_word][current_tag]
                for prev_tag in list(viterbi[inx].keys()):
                    try:
                        current_prob = viterbi[inx][len(sentence)-1] + current_emission + tagtoTag[prev_tag]['<END>']
                        if current_prob > max_prob:
                                max_prob = current_prob
                                max_res = str(prev_tag)
                    except KeyError:
                        continue
                
                viterbi[len(sentence)-1][current_tag]  = max_prob
                backpointer[len(sentence)-1][current_tag] = max_res
    else:
    """
    for current_tag in ['<END>']:
        #if current_tag != '<START>' and current_tag != '<END>':
        max_prob = float('-inf')
        max_res = ''
        current_emission = 0
        for prev_tag in list(viterbi[len(sentence)-1]):
            try:
                current_prob = viterbi[len(sentence)-1][prev_tag] + current_emission + tagtoTag[prev_tag][current_tag]
                if current_prob > max_prob:
                    max_prob = current_prob
                    max_res = str(prev_tag)
            except KeyError:
                continue
        
        viterbi[len(sentence)][current_tag]  = max_prob
        backpointer[len(sentence)][current_tag] = max_res
   
    return tag_sentence(sentence, backpointer)


def write_answer(final_answer):
    with open('hmmoutput.txt', 'w', encoding = 'UTF-8') as file_obj:
        for line in final_answer:
            file_obj.write(line)
            file_obj.write('\n')


def hmm_code(file_path):
    
    # Load Data from the files
    wordList = read_files(file_path)

    # Load the Stat Data from Learning
    tagtoTagProbs, allTagsCount, wordvsTagProbs, allWords, disregardWordCount, openClassTag = load_data()

    final_answer = []
    # Perform viterbi for each of the sentences
    for sentence in wordList:
        if len(sentence) > 0:
            final_answer.append(perform_viterbi(tagtoTagProbs, allTagsCount, wordvsTagProbs, allWords, disregardWordCount, sentence, openClassTag))
    
    # Write Answers to the file
    write_answer(final_answer)


if __name__ == "__main__":
    file_path = 'hmm-training-data\\hmm-training-data\\it_isdt_dev_raw.txt' # For Local Work
    #file_path = 'hmm-training-data\\hmm-training-data\\ja_gsd_dev_raw.txt'
    #file_path = str(sys.argv[1]).strip() # For Vocareum Submission
    hmm_code(file_path)
    




