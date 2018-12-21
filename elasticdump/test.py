from elasticsearch import Elasticsearch, helpers
import sys, json
import os
es =  Elasticsearch(["http://localhost:9200"], http_auth=('elastic', 'changeme'))
es.info(pretty=True)

es.indices.delete(index='demo')

filename = "users.json"
with open(filename,'r',encoding='UTF-8') as open_file:
    helpers.bulk(es, json.dumps(open_file), index='demo', doc_type='users')


usr=open("users.json", 'r',encoding='UTF-8')

usr.readline()
x=usr.readlines()

x[1]
x[2]

    


with open(filename,'r',encoding='UTF-8') as open_file:
    for line in open_file.readlines():
        helpers.bulk(es, line, index='demo', doc_type='movies')

import json
import requests
uri = 'http://elastic:changeme@localhost:9200/demo/movies/_search?pretty=true'

query = json.dumps({"query": 
{"match": 
    {"title": 'toy'}
    }
})
response = requests.get(uri, data=query)
results = json.loads(response.text)



es = Elasticsearch([{'host':app.config['ELASTIC_HOST'], 'port':9200}], http_auth=(app.config['ELASTIC_USR'], app.config['ELASTIC_PWD']))