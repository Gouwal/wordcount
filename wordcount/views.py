from flask import render_template, request, url_for
import requests
from bs4 import BeautifulSoup
import nltk
import re
import operator
from collections import Counter

from . import app, db
from .models import Result
from .stop_words import stops

@app.route('/', methods=['GET','POST'])
def index():
    errors = []
    results = {}
    if request.method == 'POST':
        try:
            url = request.form['url']
            resp = requests.get(url)
            # print resp.text
        except:
            errors.append("Unable to get URL. Please make sure it's valid and try again.")
            return render_template('index.html',errors=errors)
        if resp:
            results, errors = textProcess(resp.text,url,errors)
            # print results

    return render_template("index.html", errors=errors, results=results)


def textProcess(text, url, errors):
    raw = BeautifulSoup(text, 'html.parser').get_text()
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
    results = sorted(
        no_stop_words_count.items(), 
        key=operator.itemgetter(1), 
        reverse=True
    )
    try:
        result = Result(
            url=url, 
            result_all=raw_words_count, 
            result_no_stop_words=no_stop_words_count
        )
        db.session.add(result)
        db.session.commit()
    except:
        errors.append("Unable to add item to database.")
    return results, errors