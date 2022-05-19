import re
import csv
import pymorphy2
from gensim.models import doc2vec


class Vector:
    def __init__(self):
        self.book_name = []
        self.book_name_norm = []
        self.book_desc = []
        self.book_desc_norm = []

    def pos(self,word, morth=pymorphy2.MorphAnalyzer()):
        return morth.parse(word)[0].tag.POS

    def parsi(self, status):
        #Создаем массив векторов описания
        with open("book_new.csv", encoding='utf-8') as r_file:
            file_reader = csv.reader(r_file, delimiter=",")
            for row in file_reader:
                for elem in range(len(row)):
                    words = row[elem].lower().split()
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
                    if len(row[1].split()) > 13:
                        if elem == 0:
                            self.book_name_norm.append(row[elem])
                            self.book_name.append(result)
                        else:
                            self.book_desc_norm.append(row[elem])
                            self.book_desc.append(result)
        def tagged_document(list_of_ListOfWords):
            for x, ListOfWords in enumerate(list_of_ListOfWords):
                yield doc2vec.TaggedDocument(ListOfWords, [x])


        #вектора
        data_train = list(tagged_document(self.book_desc))
        data_train_name = list(tagged_document(self.book_name))
        d2v_model = doc2vec.Doc2Vec(vector_size=40, min_count=2, epochs=30)
        d2v_model_name = doc2vec.Doc2Vec(vector_size=40, min_count=2, epochs=30)
        #расширить словарный запас
        d2v_model.build_vocab(data_train)
        d2v_model_name.build_vocab(data_train_name)

        #Обучение модели Doc2Vec
        d2v_model.train(data_train, total_examples=d2v_model.corpus_count, epochs=d2v_model.epochs)
        d2v_model_name.train(data_train_name, total_examples=d2v_model_name.corpus_count, epochs=d2v_model_name.epochs)

        if status == "name":
            data = [
                [i for i in range(len(self.book_name))],
                [i for i in range(10000, 10000 + len(self.book_name))],
                [d2v_model_name[_] for _ in range(len(self.book_name))],
            ]
        else:
            data = [
                [i for i in range(len(self.book_name))],
                [i for i in range(10000, 10000 + len(self.book_name))],
                [d2v_model[_] for _ in range(len(self.book_name))],
            ]
        return data

