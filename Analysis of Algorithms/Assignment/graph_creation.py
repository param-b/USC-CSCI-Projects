import math
import sys
import time
import tracemalloc
import random
from writer_function import WriterFuncs
from time_and_memory import GetTime
import csv


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

    def dynamic_programming_new(self, X, Y):
    # The Needleman-Wunsch algorithm
    
    # Stage 1: Create a zero matrix and fills it via algorithm
        len_x, len_y = len(X), len(Y)
        mat = []
        for i in range(len_x+1):
            mat.append([0]*(len_y+1))
        for j in range(len_y+1):
            mat[0][j] = self.delta*j
        for i in range(len_x+1):
            mat[i][0] = self.delta*i
        for i in range(1, len_x+1):
            for j in range(1, len_y+1):
                mat[i][j] = min(mat[i-1][j-1] + self.alpha[self.alpha_enum[X[i-1]]][self.alpha_enum[Y[j-1]]], mat[i][j-1] + self.delta, mat[i-1][j] + self.delta)

        # Stage 2: Computes the final alignment, by backtracking through matrix
        alignmentA = ""
        alignmentB = ""
        i, j = len_x, len_y
        while i and j:
            score, scoreDiag, scoreUp, scoreLeft = mat[i][j], mat[i-1][j-1], mat[i-1][j], mat[i][j-1]
            if score == scoreDiag + self.alpha[self.alpha_enum[X[i-1]]][self.alpha_enum[Y[j-1]]]:
                alignmentA = X[i-1] + alignmentA
                alignmentB = Y[j-1] + alignmentB
                i -= 1
                j -= 1
            elif score == scoreUp + self.delta:
                alignmentA = X[i-1] + alignmentA
                alignmentB = '_' + alignmentB
                i -= 1
            elif score == scoreLeft + self.delta:
                alignmentA = '_' + alignmentA
                alignmentB = Y[j-1] + alignmentB
                j -= 1
        while i:
            alignmentA = X[i-1] + alignmentA
            alignmentB = '_' + alignmentB
            i -= 1
        while j:
            alignmentA = '_' + alignmentA
            alignmentB = Y[j-1] + alignmentB
            j -= 1
        # Now return result in format: [1st alignment, 2nd alignment, similarity]

        return [alignmentA, alignmentB, mat[len_x][len_y]]
        
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
    
def create_random_strings():
    string_1 = []
    string_2 = []
    chars_avail = ['A','C','G','T']
    for i in range(5, 25):
        k = 2**i
        selection_1 = random.choices(chars_avail, k=k)
        selection_2 = random.choices(chars_avail, k=k)
        string_1.append(''.join(selection_1))
        string_2.append(''.join(selection_2))
    return string_1, string_2



if __name__ == "__main__":
    run_dict = {}
    i = 5
    string_1, string_2 = create_random_strings()
    with open('output.tsv', 'a', newline='') as f_output:
        tsv_output = csv.writer(f_output, delimiter='\t')
        tsv_output.writerow(['String Power', 'Memory DP', 'Memory DC', 'Time DP', 'Time DC'])

        for str1, str2 in zip(string_1, string_2):
            
            # For DP Soln
            print(i)
            tracemalloc.start()
            gt = GetTime()
            gt.reset_time()
            sa = SequenceAlignment()
            strings = sa.dynamic_programming_new(str1, str2)
            res_string_1 = strings[0]
            res_string_2 = strings[1]
            score = strings[2]

            current, peak_dp  = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            end_time_dp = gt.end_time()

            # For DC Solution
            tracemalloc.start()
            gt = GetTime()
            gt.reset_time()

            list_of_strings_and_penalty = sa.divide_and_conquer(str1, str2)
            res_string_1 = list_of_strings_and_penalty[0]
            res_string_2 = list_of_strings_and_penalty[1]
            similarity = list_of_strings_and_penalty[2]

            current, peak_dc  = tracemalloc.get_traced_memory()
            end_time_dc = gt.end_time()
            tracemalloc.stop()

            # Writing outputs into file
            tsv_output.writerow([i, peak_dp/1024.0, peak_dc/1024.0, end_time_dp, end_time_dc])
            i += 1


        #print("Sim Scrore:" + str(similarity))

        #print (res_string_1[0:50] + " " + res_string_1[-50:])
        #print (res_string_2[0:50] + " " + res_string_2[-50:])