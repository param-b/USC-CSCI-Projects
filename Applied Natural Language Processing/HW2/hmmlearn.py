import re
from collections import defaultdict
import sys
import os
import glob
import json
import math
import copy


def read_files(file_path):
    # Read all the Data from the Path
    wordList = []
    with open(file_path, mode = 'r', encoding = 'UTF-8') as file_obj:   
        all_sentences_obj = file_obj.read()
        all_sentences = str(all_sentences_obj).split('\n')
        for single_sentence in all_sentences:
            single_sentence_array = single_sentence.strip().split()
            temp = []
            for single_word_pair in single_sentence_array:
                temp.append(single_word_pair.strip())

            wordList.append(temp)          
    
    return wordList

def countWords(tagtoTag, allTagsCount, wordvsTag, allWordsCount, wordList, openClassTag):
    prev_tag = "<START>"

    for single_sentence in wordList:
        prev_tag = "<START>"
        
        for word_tag_combo in  single_sentence:
            
            word_tag_combo_list  = word_tag_combo.rsplit('/', 1)
            word = word_tag_combo_list[0]
            tag = word_tag_combo_list[-1]

            allTagsCount[tag] += 1
            wordvsTag[word][tag] += 1
            tagtoTag[prev_tag][tag] += 1
            allWordsCount[word] += 1

            # For the openClassTag

            openClassTag[tag].add(word)



            prev_tag = tag

        tagtoTag[prev_tag]["<END>"] += 1

    return tagtoTag, allTagsCount, wordvsTag, allWordsCount, openClassTag

def get_all_words(sentenceList):
    tmp = []
    for sentence in sentenceList:
        tmp.append(sentence.split())
    return tmp

def findOpenClassTags(openClassTag, smoothing_factorcount_threshold = 0):
    ans_arr = defaultdict(int)
    for tag, count in openClassTag.items():
        #print(count)
        if len(count) >= smoothing_factorcount_threshold:
            ans_arr[tag] = 1
    return ans_arr
        

def smoothEmission(wordvsTag, allWordsCount, allTagsCount, smoothing_factor):
    for tag in list(allTagsCount):
        for word in allWordsCount:
            wordvsTag[word][tag] += smoothing_factor
            allTagsCount[tag] += smoothing_factor
    return wordvsTag, allTagsCount, allWordsCount


def smoothTagtoTag(tagtoTag, allTagsCount, smoothing_factor, length_factor):

    for first_tag in allTagsCount.keys():
        
        allTagsCount[first_tag] += length_factor

        if first_tag == '<END>':
            continue
        
        for second_tag in allTagsCount.keys():
            if second_tag == "<START>":
                continue
            tagtoTag[first_tag][second_tag] += smoothing_factor
            #allTagsCount[first_tag] += smoothing_factor
            
    return tagtoTag, allTagsCount

def disregardTags(allTagsCount_copy, threshold=5, threshold2 =20):
    temp_allTagsCount = defaultdict(int)
    counter = 0
    for tag, value in allTagsCount_copy.items():
        if value <= threshold or value >= threshold2:
            temp_allTagsCount[tag] = value
        else:
            counter += 1
            print("Tag Deleted : " + tag + " Value: " + str(value)) 
    print("Tags Deleted " + str(counter))
    return temp_allTagsCount 

def disregard_word_emission(wordCount,threshold=0):
    disregardWordCount = defaultdict(int)
    for word, value in wordCount.items():
        if value < threshold:
            disregardWordCount[word] = 0
        else:
            disregardWordCount[word] = 1
    return disregardWordCount


def create_probabilities(tagtoTag, allTagsCount, wordvsTag):
    log_exponent = 2*len(allTagsCount.keys())
    #log_exponent = 0
    wordvsTagProbs = defaultdict(lambda: defaultdict(float))
    tagtoTagProbs = defaultdict(lambda: defaultdict(float))

    for word, temp_value in wordvsTag.items():
        for tag, wordvsTag_count in temp_value.items():
            if allTagsCount[tag] > 0 and wordvsTag_count > 0:
                wordvsTagProbs[word][tag] = math.log(wordvsTag_count) + log_exponent - math.log(allTagsCount[tag])

    for prev_tag, temp_value in tagtoTag.items():
        for next_tag, tagvsTag_count in temp_value.items():
            if allTagsCount[prev_tag] > 0 and allTagsCount[next_tag] > 0:
                tagtoTagProbs[prev_tag][next_tag] = math.log(tagvsTag_count) + log_exponent - math.log(allTagsCount[prev_tag])

    return wordvsTagProbs, tagtoTagProbs

def store_data(tagtoTag, allTagsCount, wordvsTag, disregardWordCount, openClassTag):
    with open('hmmmodel.txt', 'w', encoding = 'UTF-8') as file_obj:
        result = {}
        result['Tag to Tag'] = tagtoTag
        result['All Tags Count'] = allTagsCount
        result['Word vs Tag'] = wordvsTag
        result['Disregard Word Count'] = disregardWordCount
        result['Open Class Tag'] = openClassTag
        temp_word_dict = {}
        for word in wordvsTag.keys():
            temp_word_dict[word] = 1
        result['All Words'] = temp_word_dict
        file_obj.write(json.dumps(result))

def hmm_learn(file_path, smoothing_factor=1):
    
    wordvsTag = defaultdict(lambda: defaultdict(int))
    tagtoTag = defaultdict(lambda: defaultdict(int))
    allTagsCount = defaultdict(int)
    allWordsCount = defaultdict(int)
    openClassTag = defaultdict(set)

    wordList = read_files(file_path)
    
    #wordList = get_all_words(sentenceList)
    
    allTagsCount["<START>"] = len(wordList)
    allTagsCount["<END>"] = len(wordList)

    tagtoTag, allTagsCount, wordvsTag, allWordsCount, openClassTag = countWords(tagtoTag, allTagsCount, wordvsTag, allWordsCount, wordList, openClassTag)

    smoothing_factor = smoothing_factor
    length_factor  = smoothing_factor*2*len(allTagsCount) - smoothing_factor*2

    #allTagsCount = disregardTags(copy.deepcopy(allTagsCount), threshold=0, threshold2 = 0)

    openClassTag = findOpenClassTags(openClassTag, smoothing_factorcount_threshold = 300) 

    tagtoTag, allTagsCount = smoothTagtoTag(tagtoTag, allTagsCount, smoothing_factor, length_factor)

    #wordvsTag, allTagsCount, allWordsCount = smoothEmission(wordvsTag, allWordsCount, allTagsCount, smoothing_factor)

    wordvsTagProbs, tagtoTagProbs = create_probabilities(tagtoTag, allTagsCount, wordvsTag)

    disregardWordCount = disregard_word_emission(allWordsCount)

    store_data(tagtoTagProbs, allTagsCount, wordvsTagProbs, disregardWordCount, openClassTag)

    return

if __name__ == "__main__":
    #file_path = 'C:\Users\param\OneDrive - University of Southern California\CSCI 544 Applied NLP\HWS\CD2\hmm-training-data\hmm-training-data\it_isdt_dev_tagged.txt' # For Local Work
    file_path = 'hmm-training-data\\hmm-training-data\\it_isdt_train_tagged.txt'
    #file_path = "hmm-training-data\\hmm-training-data\\ja_gsd_train_tagged.txt"
    #file_path = str(sys.argv[1]).strip() # For Vocareum Submission
    hmm_learn(file_path, smoothing_factor=1)
    