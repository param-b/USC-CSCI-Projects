from collections import defaultdict
import json


counter = 0
total = 0

f1 = open("hmm-training-data\\hmm-training-data\\it_isdt_dev_tagged.txt",  'r' ,encoding = 'UTF-8')
#f1 = open("hmm-training-data\\hmm-training-data\\ja_gsd_dev_tagged.txt", encoding = 'UTF-8')

f2 = open("hmmoutput.txt", 'r' ,encoding = 'UTF-8')

data_in = []
data_out = []

data_in += f1
data_out += f2

print (len(data_in))
print (len(data_out))

wrond_dict = defaultdict(int)
for i in range(0, len(data_in)):
	l1 = data_in[i].split()
	l2 = data_out[i].split()
	for j in range(0, len(l1)):
		for a,b in zip(l1[j].split(' '),l2[j].split(' ')):
			if a==b:
				counter += 1
			else:
				wrond_dict["".join(a.split('/')[-1])+"~"+"".join(b.split('/')[-1])] += 1
		total += 1

print (total)
print (counter)
print (float(counter * 100)/total)
f2 = open("err.txt",'w', encoding = 'UTF-8')
f2.write('wrong_ans~right_ans\n')
for inx, val in wrond_dict.items():
	f2.write(f'{inx} \t {val}\n')
#f2.write(json.dumps(wrond_dict))
