from collections import defaultdict
import sys
import os
import glob
import json
import math
from normalize_data import PreProcessData

def class_num_to_name(class_type):
    if class_type == "1,3":
        return "truthful positive " 
    if class_type == "1,4":
        return "deceptive positive " 
    if class_type == "2,3":
        return "truthful negative " 
    if class_type == "2,4":
        return "deceptive negative " 

def find_max_class_type(class_values_dict):
    max_class_type = 0
    max_val = float('-inf')
    for class_type, value in class_values_dict.items():
        if max_val < value:
            max_val = value
            max_class_type = class_type
    return str(max_class_type) 

def find_class(file_name, wordClassCount, classPriorProbability):
    # Used to Find the Class which th file belongs to!
    class_values_dict = defaultdict(int) 
    with open(file_name, 'r') as file_obj:
        file_content = file_obj.read()
        pd = PreProcessData(file_content)
        processed_data = pd.pre_process_data()
        for class_value in range(1,5):
            for word in processed_data:
                try:
                    class_values_dict[class_value] += math.log(wordClassCount[word][str(class_value)])         
                except KeyError:
                    continue
            class_values_dict[class_value] += math.log(classPriorProbability[str(class_value)])
    
    positive_negative_dict = { your_key: class_values_dict[your_key] for your_key in [1,2] }
    truthful_deceptive_dict = { your_key: class_values_dict[your_key] for your_key in [3,4] }
    return find_max_class_type(positive_negative_dict) + "," + find_max_class_type(truthful_deceptive_dict)
   

def classify():

    # Load Model
    model_file = open('nbmodel.txt', 'r')
    wordClassCount = json.loads(model_file.read())

    # Default Prior Probabilites
    classPriorProbability = {
        1 : 0.25,
        2 : 0.25,
        3 : 0.25,
        4 : 0.25 
    }

    # Loading Prior Probabilites
    classPriorProbability = wordClassCount['Class Priors']

    # For Local Debugging
    debug_file_path = '.\op_spam_training_data'
    all_files = glob.glob(os.path.join(debug_file_path, '*/*/*/*.txt'))

    # Get all Testing Files
    #all_files = glob.glob(os.path.join(sys.argv[1], '*/*/*/*.txt')) 
    with open('nboutput.txt', 'w') as op_file_obj:  
        for file_path in all_files:
            class_type = find_class(file_path, wordClassCount, classPriorProbability)
            class_type_val = class_num_to_name(str(class_type))
            file_op = class_type_val + file_path + "\n"
            op_file_obj.write(file_op)
    return

if __name__ == "__main__":
    classify()