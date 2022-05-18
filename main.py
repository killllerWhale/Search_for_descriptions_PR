from pymilvus import connections
from pymilvus import CollectionSchema, FieldSchema, DataType
from pymilvus import utility
from pymilvus import Collection
from book_parsing import Vector
from pymilvus import Collection
from req_get import Requester

connections.connect(
    alias="default",
    host='localhost',
    port='19530'
)


r = Requester()
v = Vector()
collection = Collection("book")
collection.load()
search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
results = collection.search(
    data=[r.parsi()],
    anns_field="book_intro",
    param=search_params,
    limit=10,
    consistency_level="Strong"
)


print(results[0].ids)
for i in range(len(results[0].ids)):
    print(v.book_name[results[0].ids[i]-10000], end="\n")

collection.release()
