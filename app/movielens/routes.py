from flask import render_template
from app.movielens import bp
from snippets import flash_errors

### 

## AutoComplete #####################
from flask import Flask, Response, request, jsonify
import json
from wtforms import TextField, Form

cities = ["Bratislava",
          "Banská Bystrica",
          "Prešov",
          "Považská Bystrica",
          "Žilina",
          "Košice",
          "Ružomberok",
          "Zvolen",
          "Poprad"]

# form class
class SearchForm(Form):
    autocomp = TextField('Insert City', id='city_autocomplete')

# backend api
@bp.route('/_autocomplete', methods=['GET'])
def autocomplete():
    return Response(json.dumps(cities), mimetype='application/json')

# frontend query form
# @bp.route('/auto', methods=['GET', 'POST'])
# def index():
#     form = SearchForm(request.form)
#     return render_template("movielens/search.html", form=form)


## MovieLens #####################
# using requests
import requests
import json

# https://stackoverflow.com/questions/34704997/jquery-autocomplete-in-flask
# form class
class MovieSearch(Form):
    movieTitle = TextField('Insert Title', id='movieTitle')

# backend api
@bp.route('/_title', methods=['GET'])
def search_title():
    """Simple Elasticsearch Query""" 
    uri='http://10.10.114.97:9200/demo/movies/_search?pretty=true'
    search = request.args.get('q')
    query = json.dumps({"query": 
    {"match": 
        {"title": str(search)}
        }
    })
    response = requests.get(uri, data=query)
    results = json.loads(response.text)
    # making json for autocomplete
    titles = [hit['_source'].get('title') for hit in results['hits']['hits']]
    tmdbId = [hit['_source'].get('tmdbId') for hit in results['hits']['hits']]
    resDict = [{'label': titles[i], 'value': tmdbId[i]} for i in range(0, len(titles))]
    return  Response(json.dumps(resDict), mimetype='application/json')

# frontend query form
@bp.route('/movie', methods=['GET', 'POST'])
def index():
    ## 1. Build form
    # form = SearchForm(request.form)
    movieForm = MovieSearch(request.form)

    ## 2. Get Select Movie
    title = request.form.get('movieTitle')
    tmdbId = request.form.get('movieVal')
    tmdbId = str(tmdbId)

    ## 3. Recommendation Results

    return render_template("movielens/search.html", movie=movieForm, movieTitle=title, movieVal=tmdbId)

# @bp.route('/_movieId', methods=['GET','POST'])
# def getSelect():
#     title = request.form.get('movieTitle')
#     tmdbId = request.form.get('movieVal')
#     tmdbId = str(tmdbId)
#     return render_template("movielens/search.html", movieTitle=title, movieVal=tmdbId)
 