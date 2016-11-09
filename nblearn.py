import os
import sys

###################### Reading HAM/SPAM folder ######################

def ham_spam(root, cat, vocabulary):

	count_data = 0
	vocab = dict()
	total_words = 0
	total_email = 0
	emails = []
	for subdir, dirs, files in os.walk(root):
		if 'train' in subdir and subdir.endswith(cat):
			email_list = os.listdir(subdir)
			emails.extend(email_list)
			total_email += len(email_list)
			for email in email_list:
				if email.endswith('.txt'):
					filename = subdir + '/' + email
					with open(filename,'r', encoding='latin-1') as infile:
						for line in infile:
							tokens = line.strip().split()
							for t in tokens:
								t = t.lower()
								total_words += 1
								if t not in vocabulary:
									vocabulary[t] = 1
								if t not in vocab:
									vocab[t] = 1
								else:
									vocab[t] += 1
						infile.close()
	return vocab, total_words, total_email, vocabulary, emails
						
def main(argv):

	root = argv[0]
	global_vocab = dict()
	cat = ['ham','spam']

	vocab_ham, total_words_ham, total_emails_ham, global_vocab, ham_email_list = ham_spam(root, cat[0], global_vocab)
	vocab_spam, total_words_spam, total_emails_spam, global_vocab, spam_email_list = ham_spam(root, cat[1], global_vocab)

	#print(len(vocab_ham),len(vocab_spam))

	with open('nbmodel.txt','w') as output:
		for key, value in vocab_ham.items():
			output.write(key+' '+str(value))
			output.write('\n')
		output.write('END OF HAM DICTIONARY')
		output.write('\n')
		
		for key, value in vocab_spam.items():
			output.write(key+' '+str(value))
			output.write('\n')
		output.write('END OF SPAM DICTIONARY')
		output.write('\n')
		
		output.write('total_words_ham' + '=' + str(total_words_ham))
		output.write('\n')
		output.write('total_emails_ham' + '=' + str(total_emails_ham))
		output.write('\n')
		output.write('total_words_spam' + '=' + str(total_words_spam))
		output.write('\n')
		output.write('total_emails_spam' + '=' + str(total_emails_spam))
		output.write('\n')
		output.write('global_vocab_len' + '=' + str(len(global_vocab)))

		output.close()

		'''
		with open('email.pickle', 'wb') as f:
			pickle.dump((ham_email_list,spam_email_list), f)
		'''

if __name__ == "__main__":
   main(sys.argv[1:])