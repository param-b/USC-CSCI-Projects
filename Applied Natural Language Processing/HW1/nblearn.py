import re
from collections import defaultdict
import sys
import os
import glob
import json
from normalize_data import PreProcessData

def get_all_files():
    # Finds all paths and find's classes of based on the folder name
    class_name_paths = {}

    # For Local Debugging
    debug_file_path = '.\op_spam_training_data'
    all_files = glob.glob(os.path.join(debug_file_path, '*/*/*/*.txt'))

    # Actual Code
    #print("Path to file : " + str(sys.argv[1]))
    #all_files = glob.glob(os.path.join(sys.argv[1], '*/*/*/*.txt'))
    #print("All Files: " + ','.join(all_files))

    for file_name in all_files:
        class1, class2 = '', ''
        temp_value = file_name.split('\\')[-4:]
        if type(temp_value) == list and len(temp_value) == 4:
            class1, class2, _, _ = temp_value
        else:
            class1, class2, _, _ = file_name.split('/')[-4:]
        if class1 in "positive_polarity":
            if class2 in "truthful_from_TripAdvisor":
                class_name_paths[file_name] = 1             
            else:
                class_name_paths[file_name] = 2
        else:
            if class2 in "truthful_from_Web":
                class_name_paths[file_name] = 3
            else:
                class_name_paths[file_name] = 4
    with open('nbclasses.txt', 'w') as fp:
        json.dump(class_name_paths, fp)
    return class_name_paths

def unpack_class_type(current_class):
    class_type_dict={
        1 : (1,3),
        2 : (1,4),
        3 : (2,3),
        4 : (2,4)
    }
    return class_type_dict[current_class]

def count_words(content, wordCount, wordClassCount, classCount, current_class):
    #wordCount = defaultDict(int)
    class_options = unpack_class_type(current_class)
    for word in content:
        for current_class_type in class_options:
            wordCount[word] += 1 
            wordClassCount[word][current_class_type] += 1 
            classCount[current_class_type]  += 1 
    return wordCount, wordClassCount, classCount
"""    
def find_unique_occurrences(paths, word_in_doc=defaultdict(int)):
  for path in paths:
    with open(path, 'w') as content:
      vocab  = set(content.split())
      for word in vocab:
        word_in_doc[word] += 1
  temp_word_in_doc = {}
  for key, value in word_in_doc.items():
    if value >= 5:
      temp_word_in_doc[key] = value
  return word_in_doc

"""
def find_and_remove_rare_words(wordCount, wordClassCount, classCount, threshold):
    additional_stop_words = []
    for word, value in wordCount.items():
        if value < threshold:
            additional_stop_words.append(word)
    for word in additional_stop_words:
        value = wordCount[word]
        class_dict = wordClassCount[word]
        for class_type, class_value in class_dict.items():
            classCount[class_type] -= class_value
        del wordClassCount[word]
    return wordCount, wordClassCount, classCount

def perform_k_smoothing(wordClassCount, classCount, k=1):
    total_vocab = len(wordClassCount.keys())
    
    # Add k smoothing based on vocab size to all class types
    for class_type in range(1,5):
        classCount[class_type] += total_vocab * k
    
    # Add k smoothing based on vocab size to all words
    for word in wordClassCount.keys():
        for class_type in range(1,5):
            wordClassCount[word][class_type] += k

    return wordClassCount, classCount

def calculate_class_priors(classCount):
    
    positive_negative_dict = { your_key: classCount[your_key] for your_key in [1,2] }
    truthful_deceptive_dict = { your_key: classCount[your_key] for your_key in [3,4] }
    
    totalCount = 0
    temp_dict = {}
    
    # For Pos Neg Classifier
    for key, value in positive_negative_dict.items():
        totalCount += value

    for key, value in positive_negative_dict.items():
        temp_dict[key] = float(value)/float(totalCount)

    # For Truthful Deceptive Classifier
    totalCount = 0
    for key, value in truthful_deceptive_dict.items():
        totalCount += value

    for key, value in truthful_deceptive_dict.items():
        temp_dict[key] = float(value)/float(totalCount)


    return temp_dict

def learn(type_of_learning, threshold=2, k=1):
    # Initialization
    wordClassCount = defaultdict(lambda: defaultdict(int))
    wordCount = defaultdict(int)
    classCount = defaultdict(int)

    # Get All File Paths
    all_file_paths_and_class = get_all_files()
    totalCountFiles = len(all_file_paths_and_class)

    # Count the words and other content information.
    for file_name, class_type in all_file_paths_and_class.items():
        with open(str(file_name),'r') as file_obj:
            #print("Current File: " + file_name)
            file_content = file_obj.read()
            #print("File Content: " + file_content)
            
            pd = PreProcessData(file_content)
            processed_data = pd.pre_process_data()

            #print(processed_data)
            wordCount, wordClassCount, classCount = count_words(processed_data, wordCount, wordClassCount, classCount, class_type)

    # Find Rarely occurring words and delete them so not to as tilt results too much too rare words.
    wordCount, wordClassCount, classCount = find_and_remove_rare_words(wordCount, wordClassCount, classCount, threshold)

    # Now Let us find probabilities!
    wordProbabilites = defaultdict(lambda: defaultdict(float))
    
    # Calculate and Store Class priors
    wordProbabilites['Class Priors'] = calculate_class_priors(classCount)

    # Perform K Smoothing
    wordClassCount, classCount = perform_k_smoothing(wordClassCount, classCount, k=k)

  
    #print("TRY 1")
    for word, word_class_occ in wordClassCount.items():
        #print(")
        for class_type, class_value in word_class_occ.items():
            wordProbabilites[word][class_type] = float(float(class_value)/float(classCount[class_type]))
    

    # Store Probabilities as JSon
    with open('nbmodel.txt', 'w') as fp:
        json.dump(wordProbabilites, fp)

if __name__ == '__main__':
    learn('smoothing')