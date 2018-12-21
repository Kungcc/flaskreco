from elasticsearch import Elasticsearch
from app import app

es = Elasticsearch([{'host':app.config['ELASTIC_HOST'], 'port':9200}], http_auth=(app.config['ELASTIC_USR'], app.config['ELASTIC_PWD']))

import pandas as pd
import json

def convert_vector(x):
    '''Convert a list or numpy array to delimited token filter format'''
    return " ".join(["%s|%s" % (i, v) for i, v in enumerate(x)])

def reverse_convert(s):
    '''Convert a delimited token filter format string back to list format'''
    return  [float(f.split("|")[1]) for f in s.split(" ")]

def vector_to_struct(x, version, ts):
    '''Convert a vector to a SparkSQL Struct with string-format vector and version fields'''
    return (convert_vector(x), version, ts)


# User Define Function by Gene
def get_movie(movieId, q="*", index="demo", dt="movies"):
    """
    Given a movie id, return *
    """
    response = es.get(index=index, doc_type=dt, id=movieId)
    res = response['_source']
    
    return res
    
# def get_sim(title):
#     body = {
#         "query": {
#             "term": {
#               "title": str(title)
#             }
#           }
#     }
#     response = es.search(index="demo", doc_type="movies", body=body)
#     return response

def get_sim(title):
    query = json.dumps({
     "query": {
         "match_phrase": {
            "title": str(title)
          }
      }
    })
    res = es.search(index="demo", doc_type="movies", body=query)
    return res

def get_poster_url(tmdbId):
    response = es.search(index='demo', doc_type='movies', q="tmdbId:%s" % tmdbId)
    try:
        poster_path = response['hits']['hits'][0]['_source']['poster_path']
        poster_path = 'https://image.tmdb.org/t/p/w500' + poster_path
        return poster_path
    except Exception as me:
        return "NA"

    
def fn_query(query_vec, q="*", cosine=False):
    """
    Construct an Elasticsearch function score query.
    
    The query takes as parameters:
        - the field in the candidate document that contains the factor vector
        - the query vector
        - a flag indicating whether to use dot product or cosine similarity (normalized dot product) for scores
        
    The query vector passed in will be the user factor vector (if generating recommended movies for a user)
    or movie factor vector (if generating similar movies for a given movie)
    """
    return {
    "query": {
        "function_score": {
            "query" : { 
                "query_string": {
                    "query": q
                }
            },
            "script_score": {
                "script": {
                        "inline": "payload_vector_score",
                        "lang": "native",
                        "params": {
                            "field": "@model.factor",
                            "vector": query_vec,
                            "cosine" : cosine
                        }
                    }
            },
            "boost_mode": "replace"
        }
    }
}


def get_similar(the_id, q="*", num=10, index="demo", dt="movies"):
    """
    Given a movie id, execute the recommendation function score query to find similar movies, ranked by cosine similarity
    """
    response = es.get(index=index, doc_type=dt, id=the_id)
    src = response['_source']
    if '@model' in src and 'factor' in src['@model']:
        raw_vec = src['@model']['factor']
        # our script actually uses the list form for the query vector and handles conversion internally
        query_vec = reverse_convert(raw_vec)
        q = fn_query(query_vec, q=q, cosine=True)
        results = es.search(index, dt, body=q)
        hits = results['hits']['hits']
        return src, hits[1:num+1]
    
    
def get_user_recs(the_id, q="*", num=10, index="demo"):
    """
    Given a user id, execute the recommendation function score query to find top movies, ranked by predicted rating
    """
    response = es.get(index=index, doc_type="users", id=the_id)
    src = response['_source']
    if '@model' in src and 'factor' in src['@model']:
        raw_vec = src['@model']['factor']
        # our script actually uses the list form for the query vector and handles conversion internally
        query_vec = reverse_convert(raw_vec)
        q = fn_query(query_vec, q=q, cosine=False)
        results = es.search(index, "movies", body=q)
        hits = results['hits']['hits']
        return src, hits[:num]

def get_movies_for_user(the_id, num=10, index="demo"):
    """
    Given a user id, get the movies rated by that user, from highest- to lowest-rated.
    """
    response = es.search(index=index, doc_type="ratings", q="userId:%s" % the_id, size=num, sort=["rating:desc"])
    hits = response['hits']['hits']
    ids = [h['_source']['movieId'] for h in hits]
    movies = es.mget(body={"ids": ids}, index=index, doc_type="movies", _source_include=['tmdbId', 'title'])
    movies_hits = movies['docs']
    tmdbids = [h['_source'] for h in movies_hits]
    return tmdbids

            
def display_user_recs(the_id, q="*", num=10, num_last=10, index="demo"):
    user, recs = get_user_recs(the_id, q, num, index)
    user_movies = get_movies_for_user(the_id, num_last, index)
    # check that posters can be displayed
    first_movie = user_movies[0]
    first_im_url = get_poster_url(first_movie['tmdbId'])
    # return first_im_url

    if first_im_url == "NA":
        return "<i>Cannot import tmdbsimple. No movie posters will be displayed!</i>"
    if first_im_url == "KEY_ERR":
        return "<i>Key error accessing TMDb API. Check your API key. No movie posters will be displayed!</i>"
        
    # display the movies that this user has rated highly
    title = "<h5>Get recommended movies for user id %s</h5>" % the_id
    user_html = title + """<b style="color:red;">The user has rated the following movies highly:</b>""" + "<table border=0>"
    i = 0
    for movie in user_movies:
        movie_im_url = get_poster_url(movie['tmdbId'])
        movie_title = movie['title']
        user_html += "<td><b>%s</b><img src=%s width=100></img></td>" % (movie_title, movie_im_url)
        i += 1
        if i % 5 == 0:
            user_html += "</tr><tr>"
    user_html += "</tr></table>"
    # return user_html
    
    # now display the recommended movies for the user
    title = "<br>" + """<h5 style="color:red;">Recommended movies:</h5>"""
    rec_html = title + "<table border=0>"
    i = 0
    for rec in recs:
        r_im_url = get_poster_url(rec['_source']['tmdbId'])
        r_score = rec['_score']
        r_title = rec['_source']['title']
        rec_html += "<td><b>%s</b><img src=%s width=100></img></td><td><b>%2.3f</b></td>" % (r_title, r_im_url, r_score)
        i += 1
        if i % 5 == 0:
            rec_html += "</tr><tr>"
    rec_html += "</tr></table>"
    
    detail_html = user_html + rec_html
    return detail_html

    
    
def display_similar(the_id, q="*", num=10, index="demo", dt="movies"):
    """
    Display query movie, together with similar movies and similarity scores, in a table
    """
    movie, recs = get_similar(the_id, q, num, index, dt)
    q_im_url = get_poster_url(movie['tmdbId'])
        
    title = """<h5 style="color:red;">Get similar movies for (根據電影評分):</h5>""" + "<b>%s</b>" % movie['title']
    
    if q_im_url != "https://image.tmdb.org/t/p/w500NA":
        par_html = title + "<img src=%s width=120></img>" % q_im_url
    else:
        par_html = title
        
    title = "<br>" + "<br>" + """<h5 style="color:red;">People who liked this movie also liked these:</h5>"""
    sim_html = title + "<table border=0>"
    i = 0
    for rec in recs:
        r_im_url = get_poster_url(rec['_source']['tmdbId'])
        r_score = rec['_score']
        r_title = rec['_source']['title']
        sim_html += "<td><b>%s</b><img src=%s width=80></img></td><td><b>%2.3f</b></td>" % (r_title, r_im_url, r_score)
        i += 1
        if i % 5 == 0:
            sim_html += "</tr><tr>"
    sim_html += "</tr></table>"
    
    detail_html = par_html + sim_html
    return detail_html
    
    
## User Define Recommendation by Gene
## 熱門推薦 by Avg Rating
def display_high_rating(score, row_num):
    body = {
        "aggs": {
            "avg_terms_movieId": {
                # math function
                "aggs": {
                    "avg_rating": {
                        "avg": {
                            "field": "rating"
                        }
                    },


                    # having
                    "max_avg": {
                        "bucket_selector": {
                            "buckets_path": {
                                "var1": "avg_rating"
                            },
                            "script": "params.var1 > {}".format(score)
                        }
                    }

                },  
                # group by column
                "terms": {
                    "field": "movieId",
                    "size": row_num # limit
                }

            }
        },
        "size":0
    }
    
    res = es.search(index='demo', doc_type='ratings', body=body) # type = dict
    res_detail = res['aggregations']['avg_terms_movieId']['buckets']
    
    df = pd.DataFrame(res_detail)
    df["score"] = df['avg_rating'].apply(lambda x: round(list(x.values())[0], 2))
    df = df.sort_values(by=["score"], axis=0, ascending=False).reset_index(drop=True)
    df = df.drop(columns=["avg_rating"])
    df.columns = ['doc_count', 'movieId', 'avg_rating']
    df['title'] = df['movieId'].apply(lambda x: get_movie(x)['title'])
    df['tmdbId'] = df['movieId'].apply(lambda x: get_movie(x)['tmdbId'])
    df['poster_url'] = df['tmdbId'].apply(get_poster_url) # show poster image
    
    return df
    
    
    
## Content base 推薦 by 關鍵字、演員、導演
def display_content_sim(movieTitle):
    res = get_sim(movieTitle)
    # return movieTitle
    pp = get_poster_url(res['hits']['hits'][0]['_source']['tmdbId'])
    csim_m = res['hits']['hits'][0]['_source']['csim_movies']
    
    df = pd.DataFrame(csim_m, columns=['csim_m'])
    df['tmdbId'] = df['csim_m'].apply(lambda x: x.split('|')[0] if x != None else 0)
    df['title'] = df['csim_m'].apply(lambda x: x.split('|')[1] if x != None else 0)
    df['score'] = df['csim_m'].apply(lambda x: x.split('|')[2] if x != None else 0).astype(float)
    df['poster_path'] = df['tmdbId'].apply(get_poster_url)
    
    # html
    title = """<h5 style="color:red;">Get similar movies for (根據電影關鍵字、演員、導演):</h5>""" + "<b>%s</b>" % movieTitle
    if pp != "https://image.tmdb.org/t/p/w500NA":
        par_html = title + "<img src=%s width=120></img>" % pp
    else:
        par_html = title
    
    if csim_m != []:
        par_html = par_html + "<br>" + "<br>" + """<h5 style="color:red;">Top 5 similar movies:</h5>"""
        sim_html = par_html + "<table border=0>" + "<tr>"
        for i in df.index:
            c_score = df['score'][i]
            c_title = df['title'][i]
            c_url = df['poster_path'][i]
            sim_html += "<td><b>%s</b><img src=%s width=80></img></td><td><b>%2.3f</b></td>" % (c_title, c_url, c_score)
        sim_html += "</tr><tr>"
        c_html = sim_html + "</tr></table>"
        
        return c_html
    else:
        c_html = par_html + "<br>" + "<br>" + """<h5 style="color:red;">無資料</h5>"""
        return c_html