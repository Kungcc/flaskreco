- https://www.npmjs.com/package/elasticdump


`docker pull taskrabbit/elasticsearch-dump`

# Backup index data to a file: 
docker run --rm -ti -v ${PWD}:/data taskrabbit/elasticsearch-dump --input=http://10.10.114.97:9200/demo/ --output=data/mapping.json --type=mapping
docker run --rm -ti -v ${PWD}:/data taskrabbit/elasticsearch-dump --input=http://10.10.114.97:9200/demo/ --output=data/data.json --type=data

docker run --rm -ti -v ${PWD}:/data taskrabbit/elasticsearch-dump --input=http://10.10.114.97:9200/demo/users --output=data/users.json --type=data
docker run --rm -ti -v ${PWD}:/data taskrabbit/elasticsearch-dump --input=http://10.10.114.97:9200/demo/movies --output=data/movies.json --type=data
docker run --rm -ti -v ${PWD}:/data taskrabbit/elasticsearch-dump --input=http://10.10.114.97:9200/demo/ratings --output=data/ratings.json --type=data


elasticdump \
  --input=./alias.json \
  --output=http://es.com:9200 \
  --type=alias


docker run --rm -ti -v ${PWD}:/data taskrabbit/elasticsearch-dump --input=data/mapping.json --output=http://elastic:changeme@localhost:9200/ --type=mapping
docker run --rm -ti -v ${PWD}:/data taskrabbit/elasticsearch-dump --input=data/data.json --output=http://elastic:changeme@localhost:9200/demo --type=data


docker run --rm -ti -v ${PWD}:/data taskrabbit/elasticsearch-dump --input=data/data.json --output=http://elastic:changeme@10.10.114.125:9200/ --output-index=demo --type=data


docker inspect 67f797d200fd

docker run --rm -it -p 10.10.1.1:9200:9200 5857f98b5920