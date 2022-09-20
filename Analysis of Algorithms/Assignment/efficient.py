import math
import sys
import time
import tracemalloc
from writer_function import WriterFuncs
from time_and_memory import GetTime


class SequenceAlignment:
    def __init__(self):
        self.delta = 30
        self.alpha = [[0, 110, 48, 94],
                        [110, 0, 118, 48],
                        [48, 118, 0, 110],
                        [94, 48, 110, 0]]
        
        self.alpha_enum = {'A': 0, 
                            'C': 1, 
                            'G': 2, 
                            'T': 3}

    def concatenate_string(self, input_strings, index):
        if input_strings[index].isalpha():
            str = input_strings[index]
            index += 1
        
        while (input_strings[index].isnumeric()):
            num = int(input_strings[index])
            str_first = str[:num+1]
            str_last = str[num+1:]
            str = str_first + str + str_last
            index += 1
            if index == len(input_strings):
                break

        return str, index
    
    def divide_and_conquer(self, X, Y):
        len_x, len_y = int(len(X)), int(len(Y))
        if len_x<2 or len_y<2:
            return self.dynamic_programming_new(X, Y)

        else:
            F, B = self.forward(X[:len_x//2], Y), self.backward(X[len_x//2:], Y)

            partition = [F[j] + B[len_y - j] for j in range(len_y + 1)]

            cut = partition.index(min(partition))

            F, B, partition = [], [], []

            callLeft = self.divide_and_conquer(X[ :len_x//2], Y[ :cut])
            callRight = self.divide_and_conquer(X[len_x//2: ], Y[cut: ])

            return [callLeft[r] + callRight[r] for r in range(3)]

    def forward(self, X, Y):
        len_x, len_y = len(X), len(Y)

        matrix = []
        for i in range(len_x + 1):
            matrix.append([0] * (len_y + 1))
        
        for j in range(len_y+1):
            matrix[0][j] = self.delta * j
        
        for i in range(1, len_x+1):
            matrix[i][0] = matrix[i-1][0] + self.delta
            
            for j in range(1, len_y+1):
                matrix[i][j] = min(matrix[i-1][j-1] + self.alpha[self.alpha_enum[X[i-1]]][self.alpha_enum[Y[j-1]]],
                                matrix[i-1][j] + self.delta,
                                matrix[i][j-1] + self.delta)

            matrix[i-1] = []
        return matrix[len_x]
    
    def backward(self, X, Y):
        len_x, len_y = len(X), len(Y)

        matrix = []
        for i in range(len_x+1):
            matrix.append([0]*(len_y+1))

        for j in range(len_y+1):
            matrix[0][j] = self.delta * j

        for i in range(1, len_x+1):
            matrix[i][0] = matrix[i-1][0] + self.delta

            for j in range(1, len_y+1):
                matrix[i][j] = min(matrix[i-1][j-1] + self.alpha[self.alpha_enum[X[len_x-i]]][self.alpha_enum[Y[len_y-j]]],
                                matrix[i-1][j] + self.delta,
                                matrix[i][j-1] + self.delta)
            
            matrix[i-1] = []

        return matrix[len_x]
    

if __name__ == "__main__":

    tracemalloc.start()
    gt = GetTime()
    gt.reset_time()

    #f = open('BaseTestcases_CS570FinalProject_Updated\\input1.txt', 'r')
    
    data_input_file = str(sys.argv[1])
    print(sys.argv)
    f = open(data_input_file, 'r')

    input_strings = f.readlines()

    sa = SequenceAlignment()

    for i in range(len(input_strings)):
        input_strings[i] = input_strings[i].rstrip('').rstrip('\n')
    
    str1, index = sa.concatenate_string(input_strings, 0)
    str2, _ = sa.concatenate_string(input_strings, index)

    list_of_strings_and_penalty = sa.divide_and_conquer(str1, str2)
    res_string_1 = list_of_strings_and_penalty[0]
    res_string_2 = list_of_strings_and_penalty[1]
    similarity = list_of_strings_and_penalty[2]

    print("Sim Scrore:" + str(similarity))

    print (res_string_1[0:50] + " " + res_string_1[-50:])
    print (res_string_2[0:50] + " " + res_string_2[-50:])

    print (res_string_1[0:50] + " " + res_string_1[-50:])
    print (res_string_2[0:50] + " " + res_string_2[-50:])
    
    #print("Sim Scrore:" + str)

    current, peak  = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    wf = WriterFuncs('output.txt')
    end_time = gt.end_time()
    wf.write_labels(res_string_1, res_string_2, score=similarity, time=end_time, memory=peak/1024.0)
