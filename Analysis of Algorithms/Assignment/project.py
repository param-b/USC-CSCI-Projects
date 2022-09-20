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

    '''
    def dynamic_programming(self, x, y, pxy):

        m = len(x) #length of gene1
        n = len(y) # length of gene2
        
        #table for storing optimal
        #substructure answers

        dp = [[0]*(n+1) for i in range(m+1)]
        
        #initialising the table

        for i in range(m+n+1):
        
            dp[i][0] = i * self.delta
            dp[0][i] = i * self.delta
        
        # calculating the minimum penalty

        for i in range(1,m+1):
        
            for j in range(1,n+1):
            
                if (x[i - 1] == y[j - 1]):
                
                    dp[i][j] = dp[i - 1][j - 1]
                
                else:
                
                    dp[i][j] = math.min(math.min(dp[i - 1][j - 1] + pxy ,
                                                dp[i - 1][j] + self.delta) ,
                                                dp[i][j - 1] + self.delta )
                
        # Reconstructing the solution
        l = n + m # maximum possible length
        
        i = m
        j = n
        
        xpos = l
        ypos = l
    
        #Final answers for the respective strings

        xans =[] #= new int[l + 1]
        yans =[] #= new int[l + 1]
        
        while not(i == 0 or j == 0):
        
            if (x[i - 1] == y[j - 1]):
            
                xans[xpos-1] = x[i - 1]
                yans[ypos-1] = y[j - 1]
                i-=1
                j-=1
            
            elif (dp[i - 1][j - 1] + pxy == dp[i][j]):
            
                xans[xpos-1] = x[i - 1]
                yans[ypos-1] = y[j - 1]
                i-=1
                j-=1
            
            elif (dp[i - 1][j] + self.delta == dp[i][j]):
            
                xans[xpos-1] = x[i - 1]
                yans[ypos-1] = '_'
                i-1
            
            elif (dp[i][j - 1] + self.delta == dp[i][j]):
            
                xans[xpos-1] = '_'
                yans[ypos-1] = y[j - 1]
                j-1
            
        
        while (xpos > 0):
        
            if (i > 0):
                xans[xpos-1] = int(x[i-1])
            else:
                xans[xpos-1] = int('_')
        
        while (ypos > 0):
        
            if (j > 0):
                yans[ypos-1] = int(y[j-1])
            else:
                yans[ypos-1] = int('_')
        
    
        # Since we have assumed the answer to be n+m long, we need to remove the extra gaps in the starting id
        # represents the index from which the arrays xans, yans are useful
        id = 1
        for i in range(l,0,-1):
        
            if (yans[i] == '' and xans[i] == ''):
            
                id = i + 1
                break
    
        # Printing the final answer
        print("Minimum Penalty in " + "aligning the genes = ",(dp[m][n]))
        
        print("The aligned genes are :")
        for i in range(id,l+1):
        
            print(xans[i],end='')
        
        for i in range(id, l+1):
        
            print(yans[i])
    '''

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
     


if __name__ == "__main__":

    tracemalloc.start()
    gt = GetTime()
    gt.reset_time()

    f = open('BaseTestcases_CS570FinalProject_Updated\\input2.txt', 'r')
    
    #data_input_file = str(sys.argv[1])
    #f = open(data_input_file, 'r')

    input_strings = f.readlines()

    sa = SequenceAlignment()

    for i in range(len(input_strings)):
        input_strings[i] = input_strings[i].rstrip('').rstrip('\n')
    
    str1, index = sa.concatenate_string(input_strings, 0)
    str2, _ = sa.concatenate_string(input_strings, index)

    strings = sa.dynamic_programming_new(str1, str2)
    res_string_1 = strings[0]
    res_string_2 = strings[1]
    score = strings[2]

    print (res_string_1[0:50] + " " + res_string_1[-50:])
    print (res_string_2[0:50] + " " + res_string_2[-50:])
    
    #print("Sim Scrore:" + str)

    current, peak  = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    wf = WriterFuncs('output.txt')
    end_time = gt.end_time()
    wf.write_labels(res_string_1, res_string_2, score=score, time=end_time, memory=peak/1024.0)

    list_of_strings_and_penalty = sa.divide_and_conquer(str1, str2)
    res_string_1 = list_of_strings_and_penalty[0]
    res_string_2 = list_of_strings_and_penalty[1]
    similarity = list_of_strings_and_penalty[2]

    print("Sim Scrore:" + str(similarity))

    print (res_string_1[0:50] + " " + res_string_1[-50:])
    print (res_string_2[0:50] + " " + res_string_2[-50:])