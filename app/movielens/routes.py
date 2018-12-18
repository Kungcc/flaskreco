from flask import render_template
from app.movielens import bp
from snippets import flash_errors

###

## Recommend functions 
from app.movielens.libs import *

## AutoComplete #####################
from flask import Flask, Response, request, jsonify
import json
from wtforms import TextField, Form

## MovieLens #####################
# using requests
import requests
import json

# https://stackoverflow.com/questions/34704997/jquery-autocomplete-in-flask
# form class
class MovieSearch(Form):
    movieTitle = TextField('Insert Title', id='movieTitle')
    
class UserSearch(Form):
    userId = TextField('Insert userId', id='userId')

# Backend api
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
    movieId = [hit['_source'].get('id') for hit in results['hits']['hits']]
    resDict = [{'label': titles[i], 'value': movieId[i]} for i in range(0, len(titles))]
    return  Response(json.dumps(resDict), mimetype='application/json')

# Frontend query form
@bp.route('/movie', methods=['GET', 'POST'])
def index():
    ## 1 熱門推薦
    df = display_high_rating(3.5, 10)
    
    h_html = "<table border=0>" + "<td><b>Ranking</b></td><td><b>Movie Title</b></td><td><b>Avg Rate</b></td><tr></tr>"
    for i in df.index:
        #r_im_url = get_poster_url(rec['_source']['tmdbId'])
        h_score = df['avg_rating'][i]
        h_title = df['title'][i]
        h_url = df['poster_url'][i]
        h_html += """<td><b style="color:red;">TOP %s</b></td><td><b>%s</b></td><td><b>%2.3f</b></td><td><img src=%s width=80></img></td>""" % (i+1, h_title, h_score, h_url)
        h_html += "</tr><tr>"
    x_html = h_html + "</tr></table>"

    ## 2-1 Build form
    movieForm = MovieSearch(request.form)
    userForm = UserSearch(request.form)
    
    ## 2-2 Get Select Movie
    title = request.form.get('movieTitle')
    movieId = request.form.get('movieVal')
    
    ## 2-3 Get userID
    userId = request.form.get('userId')

    ## 3 推薦結果
    ## 3-1 相似推薦
    if request.form.get('movieTitle') != None:
        ## 3-1.1 根據電影評分
        movie_html = display_similar(movieId, num=5)
        ## 3-1.2 根據電影關鍵字、演員、導演
        cs_html = display_content_sim(title)
        
        return render_template("movielens/search.html", movie=movieForm, movieTitle=title, movieVal=movieId, user=userForm, html=movie_html, csim_html=cs_html ,hr_html=x_html)
    
    ## 3-2 個人化推薦
    if request.form.get('userId') != None:
        user_html = display_user_recs(the_id=userId, num=5, num_last=5)
        return render_template('movielens/search.html', user=userForm, userId=userId, html=user_html, hr_html=x_html)
        
    return render_template("movielens/search.html", movie=movieForm, movieTitle=title, movieVal=movieId, hr_html=x_html)
