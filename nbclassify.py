import os
import sys
import math

######################### CALCULATING PROB ##########################
def classify(opfile,root, category, ham_vocab, spam_vocab, corr_class, class_ham, class_spam, voc_len, p_ham, p_spam, total_words_ham, total_words_spam, cat):
	corr_class = 0
	total_email = 0
	#print (root)
	#print(type(root))
	for subdir, dirs, files in os.walk(root):
		if 'dev' in subdir and subdir.endswith(category):
			email_list = os.listdir(subdir)
			for email in email_list:
				if email.endswith('.txt'):
					total_email += 1
					filename = subdir + '/' + email
					nb_prob_ham = math.log(p_ham)
					nb_prob_spam = math.log(p_spam)
					with open(filename,'r', encoding='latin-1') as infile:
						for line in infile:
							tokens = line.strip().split(' ')
							for t in tokens:
								t = t.lower()
								if t in ham_vocab:
									nb_prob_ham += math.log((ham_vocab[t]+1)/(total_words_ham+voc_len))
								elif t in spam_vocab:
									nb_prob_ham+=math.log(1/(total_words_ham+voc_len))
								if t in spam_vocab:
									nb_prob_spam += math.log((spam_vocab[t]+1)/(total_words_spam+voc_len))
								elif t in ham_vocab:
									nb_prob_spam+=math.log(1/(total_words_spam+voc_len))
						if cat==1:
							if nb_prob_ham>nb_prob_spam:
								corr_class += 1
								class_ham += 1
							else:
								class_spam += 1
						elif cat==0:
							if nb_prob_ham<nb_prob_spam:
								corr_class += 1
								class_spam += 1
							else:
								class_ham += 1
					#storing label and path
					if nb_prob_ham>nb_prob_spam:
						opfile.append('ham'+' '+filename)
					else:
						opfile.append('spam'+' '+filename)
	#print(corr_class, class_ham, class_spam, total_email)
	return corr_class, class_ham, class_spam, total_email, opfile	

def main(argv):
	root = argv[0]
	############ GENERATING HAM AND SPAM VOCAB DICT, VAR  ###############
	ham_vocab = dict()
	spam_vocab =dict()
	param =[]
	ptr = 0
	with open('nbmodel_10.txt','r') as inp:
		for line in inp:
			line = line.rstrip()
			if line=='END OF HAM DICTIONARY':
				#print('succ')
				ptr = 1
				continue
			elif line=='END OF SPAM DICTIONARY':
				ptr = 2
				continue

			if ptr==0:
				arr = line.split(' ')
				ham_vocab[arr[0]] = int(arr[1])
			elif ptr==1:
				arr = line.split(' ')
				spam_vocab[arr[0]] = int(arr[1])
			else:
				arr = line.split('=')
				param.append(int(arr[1]))

	#print(len(ham_vocab), len(spam_vocab))
	#print('total_words_ham =', param[0])
	#print('total_emails_ham =', param[1])
	#print('total_words_spam =' , param[2])
	#print('total_emails_spam =', param[3])
	#print('global_vocab_len =', param[4])
	#####################################################################	

	###################### Reading HAM/SPAM folder ######################
	corr_class_spam = 0
	corr_class_ham = 0

	class_spam = 0
	class_ham = 0

	total_spam = 0
	total_ham = 0

	cat = ['ham','spam']

	p_ham = param[1]/(param[1]+param[3])
	p_spam = param[3]/(param[1]+param[3])
	#print(p_ham,p_spam) 

	opfile = []
	corr_class_ham, class_ham, class_spam, total_email_ham, opfile = classify(opfile, root, cat[0], ham_vocab, spam_vocab, corr_class_ham, class_ham, class_spam, param[4], p_ham, p_spam, param[0], param[2], 1)
	corr_class_spam, class_ham, class_spam, total_email_spam, opfile = classify(opfile, root, cat[1], ham_vocab, spam_vocab, corr_class_spam, class_ham, class_spam, param[4], p_ham, p_spam, param[0], param[2], 0)

	pre_ham = corr_class_ham/class_ham
	pre_spam = corr_class_spam/class_spam
	recall_ham = corr_class_ham/total_email_ham
	recall_spam = corr_class_spam/total_email_spam
	f1_ham = (2*pre_ham*recall_ham)/(pre_ham+recall_ham)
	f1_spam = (2*pre_spam*recall_spam)/(pre_spam+recall_spam)
	print('prec_ham = ',pre_ham)
	print('recall_ham = ',recall_ham)
	print('f1_ham = ',f1_ham)
	print('prec_spam = ',pre_spam)
	print('recall_spam = ',recall_spam)
	print('f1_spam = ',f1_spam)

	with open('nboutput_10.txt','w') as op:
		for i in opfile:
			op.write(i)
			op.write('\n')
		op.close

	#####################################################################

if __name__ == "__main__":
   main(sys.argv[1:])


