import csv

from pymilvus import connections
from pymilvus import CollectionSchema, FieldSchema, DataType
from pymilvus import utility
from pymilvus import Collection
from book_parsing import Vector
from pymilvus import Collection
from req_get import Requester
import urllib.request
import os

connections.connect(
    alias="default",
    host='localhost',
    port='19530'
)

def search_descriptions(id, element):
    # logo = urllib.request.urlopen("https://drive.google.com/u/0/uc?id=1hW5gqpwmf3rTyDR4IT4nGEs293pF3uNn&export=download").read()
    # f = open("books.csv", "w")
    # f.write(logo)
    # f.close()
    count = 0
    with open("book_new.csv", encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        for row in file_reader:
            count += 1
            if count == id:
                if element == 0:
                    return row[0]
                else:
                    return row[1]

#utility.drop_collection("book_name")
# book_id = FieldSchema(
#     name="book_id",
#     dtype=DataType.INT64,
#     is_primary=True,
# )
# word_count = FieldSchema(
#     name="word_count",
#     dtype=DataType.INT64,
# )
# book_intro = FieldSchema(
#     name="book_intro",
#     dtype=DataType.FLOAT_VECTOR,
#     dim=40
# )
# schema = CollectionSchema(
#     fields=[book_id, word_count, book_intro],
#     description="Test book search"
# )
#
# collection_name = "book_desc"
# collection = Collection(
#     name=collection_name,
#     schema=schema,
#     using='default',
#     shards_num=2,
#     consistency_level="Strong"
# )

# print(utility.has_collection("book_desc"))
# print(utility.has_collection("book_name"))

# collection = Collection("book_desc")      # Get an existing collection.
# v = Vector()
# mr = collection.insert(v.parsi("desc"))
# r = Requester()
# v = Vector()
def searche_vector(status, text):
    if status == "book_name":
        r = Requester()
        collection = Collection(status)
        collection.load()
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        results = collection.search(
            data=[r.parsi(text)],
            anns_field="book_intro",
            param=search_params,
            limit=10,
            consistency_level="Strong"
        )
        print(results[0].ids)
        for i in results[0].ids:
            print(search_descriptions(i, 0))
        collection.release()
    else:
        r = Requester()
        collection = Collection("book_desc")
        collection.load()
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        results = collection.search(
            data=[r.parsi(text)],
            anns_field="book_intro",
            param=search_params,
            limit=10,
            consistency_level="Strong"
        )
        print(results[0].ids)
        for i in results[0].ids:
            print(search_descriptions(i, 1))
        collection.release()

#print(search_descriptions(1,1))
searche_vector("book_desc", "Раскольников студент убил")