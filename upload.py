import uuid
import sys
from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()

customerId = "9633281204" 
doc = {
    'customerId': "9633281204",
    'mobileNumber': '9633281204',
    'amount': 100,
    'email' : "joelkuriakose@gmail.com",
    'pin': "1234",
    "name" : "Joel Kurikose"
}
res = es.index(index="hackathon", doc_type='userData', id=customerId, body=doc)
print(res['created'])

customerId = "8886819008" 
doc = {
    'customerId': "8886819008",
    'mobileNumber': '8886819008',
    'amount': 120,
    'email' : "sreerajkrishnan.k@gmail.com",
    'pin': "1234",
    "name" : "Sreeraj Krishnan"
}
res = es.index(index="hackathon", doc_type='userData', id=customerId, body=doc)
print(res['created'])
