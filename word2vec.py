from gensim.models import word2vec
import logging, os, re
# Import various modules for string cleaning
from bs4 import BeautifulSoup

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname
    def __iter__(self):
        for path, dirs, files in os.walk(self.dirname):
            for d in dirs:
                dir_path = os.path.join(self.dirname,d)
                for fname in os.listdir(dir_path):
                    for line in open(os.path.join(dir_path, fname)):
                        # 1. Remove HTML
                        line = BeautifulSoup(line).get_text()
                        # 2. Remove non-letters
                        line = re.sub("[^a-zA-Z]"," ", line)
                        # 3. Remove numbers from text
                        for i in range(10):
                            line.replace(str(i),'')
                        # 4. Convert words to lower case and split them
                        words=line.lower().split()

                        yield words

sentences = MySentences('20_newsgroups') # a memory-friendly iterator

# Set values for various parameters  
num_features = 100    # Word vector dimensionality                        
min_word_count = 20   # Minimum word count                          
num_workers = 4       # Number of threads to run in parallel  
context = 10          # Context window size                                                                                      
downsampling = 0.001   # Downsample setting for frequent words 

print "Training model..."  
model = word2vec.Word2Vec(sentences, workers=num_workers,size=num_features, min_count = min_word_count,window = context, sample = downsampling)  
# If you don't plan to train the model any further, calling   
# init_sims will make the model much more memory-efficient.  
model.init_sims(replace=True)  
  
# It can be helpful to create a meaningful model name and   
# save the model for later use. You can load it later using Word2Vec.load()  
model_name = "Newsgroups"  
model.save(model_name)  

print model.doesnt_match("theory study education science".split())
print model.doesnt_match("france england germany berlin".split())
print model.doesnt_match("beautiful awful gorgeous sweet".split())
print model.doesnt_match("breakfast computer dinner lunch".split())

print model.most_similar("man")
print model.most_similar("beautiful")
print model.most_similar("science")
