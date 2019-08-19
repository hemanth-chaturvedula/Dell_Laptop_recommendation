#For loading google's model
import gensim
#For file path
import os.path
#For supervised learning
from sklearn.svm import LinearSVC
#For preprocessing
import re

def get_data(filename):
    with open(filename) as f:
        content = f.readlines()
    #remove whitespace characters like `\n`
    content = [x.strip() for x in content]
    #print(content[0])
    #splitting content into different words and frequencies
    freqs = []
    for line in content:
        freqs.append(line.split())
    #print(freqs[0])
    #splitting content into distinct words and frequencies
    words_set = []
    corr_freqs_set = []
    for line in freqs:
        words = ['' for elem in line]
        corr_freqs = [0 for elem in line]
        for i in range(len(line)):
            [words[i], corr_freqs[i]] = line[i].split(':')
        words_set.append(words)
        corr_freqs_set.append(corr_freqs)
    #print(words_set[0])
    #print(corr_freqs_set[0])
    #splitting labels, words and frequencies
    labels = []
    for i in range(len(corr_freqs_set)):
        labels.append(corr_freqs_set[i][-1])
        words_set[i].pop(-1)
        corr_freqs_set[i].pop(-1)
    #print(labels)
    #print(words_set[0])
    #print(corr_freqs_set[0])
    return words_set, corr_freqs_set, labels

def pre_process(words, freqs):
    words_p = []
    freqs_p = []
    for j in range(len(words)):
        word_data=[]
        freq_data=[]
        for i in range(len(words[j])):
            if(words[j][i].find('_')!=-1):
                split_words = words[j][i].split(('_'))
                for i in range(len(split_words)):
                    word = split_words[i]
                    for char in '<>\'`123456789().&$^!\\-':
                        word = word.replace(char,'') 
                    #word = re.sub('< | > | \' ' , '', split_words[i])
                    word = re.sub('[...]', ' ', word)
                    if(word.find(' ')!=-1):
                        split_w = word.split(' ')
                        for k in range(len(split_w)):
                            if(split_w!=''):
                                word_data.append(split_w[k])
                                freq_data.append(freqs[j][i])         
                    else:
                        word_data.append(word)
                        freq_data.append(freqs[j][i])
            else:
                word_data.append(words[j][i])
                freq_data.append(freqs[j][i])
        words_p.append(word_data)
        freqs_p.append(freq_data)
    return words_p, freqs_p

def word2vec_google_embed(words):
	#loading the model with Google's pre-trained Word2Vec model.
	model = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True)
	print('Stats')
	#print('Total number of word embeddings in pretrained model : ', len(model.vocab.keys()))
	print('Total number of unique words in our corpus : ', len(words))
	embedding = []
	not_existing = []
	exist = 0
	for word in words:
		try:
			embedding.append(model[word].tolist())
			exist+=1
		except:
			embedding.append('NA')
			not_existing.append(word)
	print('Number of words from corpus that exist in pre-word-embeddings : ', len(words)-len(not_existing))
	print('Number of words from corpus that do not exist in pre-word-embeddings : ', len(not_existing))
	#print('List of non existing words : ', not_existing)
	#print('Percentage of existing : ', (len(words)-len(not_existing))*100.0/len(words))
	#embedding = []
	#embedding.append(model[words[0]])
	return embedding

def separate_unique(words):
    words_set = set()
    for words_review in words:
        words_set.update(words_review)
    #print words_set
    return list(words_set)

def make_vectors(review_words, freqs, unique_words, embeddings):
    review_vectors = []
    for i in range(len(review_words)):
        sum_vector = [0 for i in range(300)]
        count = 0
        for j in range(len(review_words[i])):
            ind = unique_words.index(review_words[i][j])
            if(embeddings[ind]!='NA'):
                count += int(freqs[i][j])
                #add the vector
                for k in range(len(embeddings[ind])):
                    sum_vector[k] += embeddings[ind][k]
        avg_vector = [0 for i in embeddings[0]]
        for elem in sum_vector:
            if (count!=0):
                avg_vector.append(elem/count)
        review_vectors.append(avg_vector)
    #print review_vectors
    return review_vectors

if(__name__ == "__main__"):
    filename = os.path.abspath("data/electronics_review.txt")
    #print(filename)
    #fetch data
    words, freqs, labels = get_data(filename)
    #text preprocessing
    words_p, freqs_p = pre_process(words, freqs)
    '''
    print(words[0])
    print(freqs[0])
    print (words_p[0])
    print (freqs_p[0])
    print(len(words[0]))
    print(len(freqs[0]))
    print (len(words_p[0]))
    print (len(freqs_p[0]))
    '''
    
    #separate words
    unique_words = separate_unique(words_p)
    #print(unique_words)
    #starting the vectorization
    embeddings = word2vec_google_embed(unique_words)
    #embedding the reviews by frequency averaging
    review_vectors = make_vectors(words_p, freqs_p, unique_words, embeddings)
    #supervised learning for classification    
    #test train split
    X_train, X_test, y_train, y_test = train_test_split(review_vectors, labels, test_size=0.20, random_state=42)
    #training
    clf = LinearSVC(random_state=0, tol=1e-5)
    clf.fit(X_train,y_train)
    #testing results
    train_accuracy = clf.score(X_train, y_train)
    test_accuracy = clf.score(X_test, y_test)
    print('Train accuracy', train_accuracy)
    print('Test accuracy', test_accuracy)
    
