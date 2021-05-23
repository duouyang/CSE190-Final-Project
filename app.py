# from flask import Flask
import flask
from bs4 import BeautifulSoup
from urllib.request import urlopen
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)

def build_terms():
    url = "https://en.wikipedia.org/wiki/Glossary_of_biology"
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')
    term2def = {}

    dt = soup.find_all('dt')
    for i in range(len(dt)):
        term = dt[i].text.lower()
        definition = dt[i].findNext('dd').text.lower()
        term2def[term] = definition
    return term2def

term2def_db = build_terms()

@app.route('/api/annotate', methods=['POST'])
def annotate():
    req = flask.request.get_json(force=True)
    # Get passage from the requests
    passage = req.get('passage', None)
    new_text = ""
    words = passage.split(' ')
    for i in range(len(words)-1):
        two_words = words[i] + " " + words[i+1]
        if words[i].lower() in term2def_db:
            new_text += "<span class='term' id='" + words[i] + "' def='" + term2def_db[words[i].lower()] + "'>" + words[i] + "</span>"
        elif two_words.lower() in term2def_db:
            new_text += "<span class='term' id='" + two_words + "' def='" + term2def_db[two_words.lower()] + "'>" + two_words + "</span>"
            i += 1
        else:
            new_text += words[i]
        new_text += " "
    return new_text, 200

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)