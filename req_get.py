import re
import csv
import pymorphy2
from gensim.models import doc2vec


class Requester:
    def __init__(self):
        self.book_name = []
        self.book_desc = []
        self.book_desc_norm = []

    def pos(self,word, morth=pymorphy2.MorphAnalyzer()):
        return morth.parse(word)[0].tag.POS

    def parsi(self,text):
        words = text.lower().split()
        functors_pos = {'INTJ', 'PRCL', 'CONJ', 'PREP'}
        s = [word for word in words if self.pos(word) not in functors_pos]
        result = ""
        for i in range(len(s)):
            result += s[i]+" "
        result = result.replace("то","")
        result = re.sub('[^a-zA-ZА-я]', ' ', result)
        result = result.replace("  ", " ")
        result = result.replace("   ", " ")
        result = result.replace("    ", " ")
        result = result.replace("     ", " ")
        result = result.replace("      ", " ")
        self.book_desc.append(result)

        def tagged_document(list_of_ListOfWords):
            for x, ListOfWords in enumerate(list_of_ListOfWords):
                yield doc2vec.TaggedDocument(ListOfWords, [x])


        #вектора
        data_train = list(tagged_document(self.book_desc))
        d2v_model = doc2vec.Doc2Vec(vector_size=40, min_count=2, epochs=30)
        #расширить словарный запас
        d2v_model.build_vocab(data_train)

        #Обучение модели Doc2Vec
        d2v_model.train(data_train, total_examples=d2v_model.corpus_count, epochs=d2v_model.epochs)

        return d2v_model[0]

