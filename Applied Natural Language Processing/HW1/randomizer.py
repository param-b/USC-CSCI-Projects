from random import random


import random
with open('stopwords2.txt', 'r') as stop_word_file:
    stop_words_content = stop_word_file.read()
    #print("Stop Words:" + stop_words_content)
    split_content = stop_words_content.split(";")
    random.shuffle(split_content)
    ans = ';'.join(split_content)
    with open('stopwords3.txt', 'w') as stop_word_file_2:
        stop_word_file_2.write(ans)



    
