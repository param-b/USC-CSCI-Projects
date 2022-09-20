import sys
import time
import tracemalloc
from writer_function import WriterFuncs
from time_and_memory import GetTime


class SequenceAlignment:
    def __init__(self):
        self.delta = 30
        # The Mis-Match penalty is defined here
        self.penalty = [[0, 110, 48, 94],
                        [110, 0, 118, 48],
                        [48, 118, 0, 110],
                        [94, 48, 110, 0]]
        # The index of each letter
        self.penalty_index = {'A': 0, 'C': 1, 'G': 2, 'T': 3}

    def concatenate_string(self, input_strings, index):
        # Creates the input string
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
        # Basic dynamic Programming approach

        x_len, y_len = len(X), len(Y)
        table_dp = []

        # Fills the Table with all the base cases and initial values
        for i in range(x_len+1):
            table_dp.append([0]*(y_len+1))
        for j in range(y_len+1):
            table_dp[0][j] = self.delta*j
        for i in range(x_len+1):
            table_dp[i][0] = self.delta*i
        for i in range(1, x_len+1):
            for j in range(1, y_len+1):
                # Chooses the alignment which gives the least cost using tabulation. 
                table_dp[i][j] = min(
                    table_dp[i-1][j-1] + self.penalty[self.penalty_index[X[i-1]]][self.penalty_index[Y[j-1]]],
                    table_dp[i][j-1] + self.delta, 
                    table_dp[i-1][j] + self.delta)
        return self.make_alignment_string(table_dp, x_len, y_len, X, Y)

    def make_alignment_string(self, table_dp, x_len, y_len, X, Y):
        a_new_alignment = ""
        b_new_alignment = ""
        i, j = x_len, y_len
        while i and j:
            score, scoreDiag, scoreUp, scoreLeft = table_dp[i][j], table_dp[i-1][j-1], table_dp[i-1][j], table_dp[i][j-1]

            if score == scoreDiag + self.penalty[self.penalty_index[X[i-1]]][self.penalty_index[Y[j-1]]]:
                i -= 1
                j -= 1
                a_new_alignment = X[i] + a_new_alignment
                b_new_alignment = Y[j] + b_new_alignment

            elif score == scoreUp + self.delta:
                i -= 1
                a_new_alignment = X[i] + a_new_alignment
                b_new_alignment = '_' + b_new_alignment

            elif score == scoreLeft + self.delta:
                j -= 1
                a_new_alignment = '_' + a_new_alignment
                b_new_alignment = Y[j] + b_new_alignment
        
        while j:
            a_new_alignment = '_' + a_new_alignment
            b_new_alignment = Y[j-1] + b_new_alignment
            j -= 1
        
        while i:
            a_new_alignment = X[i-1] + a_new_alignment
            b_new_alignment = '_' + b_new_alignment
            i -= 1

        return [a_new_alignment, b_new_alignment, table_dp[x_len][y_len]]


if __name__ == "__main__":

    tracemalloc.start()
    gt = GetTime()
    gt.reset_time()

    #f = open('BaseTestcases_CS570FinalProject_Updated\\input1.txt', 'r')
    
    data_input_file = str(sys.argv[1])
    f = open(data_input_file, 'r')

    input_strings = f.readlines()

    sa = SequenceAlignment()

    for i in range(len(input_strings)):
        input_strings[i] = input_strings[i].rstrip('').rstrip('\n')
    
    str1, index = sa.concatenate_string(input_strings, 0)
    str2, _ = sa.concatenate_string(input_strings, index)

    result = sa.dynamic_programming_new(str1, str2)
    res_string_1 = result[0]
    res_string_2 = result[1]
    score = result[2]
  
    """
    print (res_string_1[0:50] + " " + res_string_1[-50:])
    print (res_string_2[0:50] + " " + res_string_2[-50:])
    
    print("Sim Scrore:" + str(score))
    """

    current, peak  = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    wf = WriterFuncs('output.txt')
    end_time = gt.end_time()
    wf.write_labels(res_string_1, res_string_2, score=score, time=end_time, memory=peak/1024.0)
