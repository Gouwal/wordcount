from flask import render_template, request, url_for
import requests
from bs4 import BeautifulSoup
import nltk
import re
import operator
from collections import Counter
from rq import Queue
from rq.job import Job
from flask import jsonify
import json

from . import app, db, q
from .models import Result
from .stop_words import stops
from worker import conn


@app.route('/', methods=['GET','POST'])
def index():
    
    return render_template("index.html")


@app.route('/results/<job_key>', methods=['GET'])
def get_results(job_key):
    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        result = Result.query.filter_by(id=job.result).first()
        results = sorted(
            result.result_no_stop_words.items(), 
            key=operator.itemgetter(1), 
            reverse=True
        )[:10]
        return jsonify(results)
    else:
        return "Nay!", 202


@app.route('/start', methods=['POST'])
def get_counts():
    # get url
    data = json.loads(request.data.decode())
    url = data["url"]
    #start the job
    job = q.enqueue_call(func=count_and_save_words, args=(url,), result_ttl=5000)
    #return created job id
    return job.get_id()


def count_and_save_words(url):
    errors = []
    try:
        resp = requests.get(url)
    except:
        errors.append("Unable to get URL. Please make sure it's valid and try again.")
        return {"error": errors}

    raw = BeautifulSoup(resp.text, 'html.parser').get_text()
    nltk.data.path.append('./nltk_data/')
    tokens = nltk.word_tokenize(raw)
    # print tokens
    text = nltk.Text(tokens)
    # remove punctuation, count raw words
    nonPunct = re.compile('.*[A-Za-z]')
    raw_words = [w for w in text if nonPunct.match(w)]
    raw_words_count = Counter(raw_words)
    # stop words
    no_stop_words = [w for w in raw_words if w.lower() not in stops]
    no_stop_words_count = Counter(no_stop_words)
    # save the results
    try:
        result = Result(
            url=url, 
            result_all=raw_words_count, 
            result_no_stop_words=no_stop_words_count
        )
        db.session.add(result)
        db.session.commit()
        return result.id
    except:
        errors.append("Unable to add item to database.")
        return {"error": errors}