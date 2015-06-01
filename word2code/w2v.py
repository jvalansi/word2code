from gensim.models import word2vec
import logging


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# sentences = word2vec.Text8Corpus('res/text8')
# model = word2vec.Word2Vec(sentences)
#
# model.save('res/text8.model')
#
# model.save_word2vec_format('res/text8.model.bin', binary=True)
model = word2vec.Word2Vec.load_word2vec_format('res/text8.model.bin', binary=True)

def get_similarity(word1,word2):
    return(model.similarity(word1,word2))

if __name__ == '__main__':
    print(model.similarity('set','number'))