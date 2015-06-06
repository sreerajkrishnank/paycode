import uuid
import sys
from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()

customerId = "8886819008" 
doc = {
    'customerId': "8886819008",
    'mobileNumber': '8886819008',
    'amount': 120,
    'email' : "sreerajkrishnan.k@gmail.com",
    'pin': "1234",
    "name" : "sreeraj krishnan"
}
res = es.index(index="hackathon", doc_type='userData', id=customerId, body=doc)
print(res['created'])
