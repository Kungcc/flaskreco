# Movie Recommenderation

- Spark + Elasticsearch + Flask/gunicorn + nginx
    - auto-complete movie search with Elasticsearch
    - recommendation model
        - content-based recommendation 
        - user-item based recommendation

- Installation
    - run: `docker-compose -d up`
    - import data & model: `docker-compose -y data_init.yml`
    - http://localhost/index
  

