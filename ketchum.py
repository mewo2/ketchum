import flask
import fasttext
import random
import json

PORT = 8765

app = flask.Flask(__name__)

examples = []
blacklist = []

def subset(words, minsize=2, maxsize=5):
    n = random.randrange(minsize, maxsize+1)
    n = min(n, len(words))
    return sorted(random.sample(words, n))

@app.route("/")
def main():
    if examples:
        basisword = flask.request.args.get('basis', None)
        if basisword:
            basis = [basisword]
        else:
            basis = subset(examples)
        suggestion = fasttext.suggest(basis, examples + blacklist)
    else:
        suggestion = None
        basis = None
    return flask.render_template("index.html", examples=examples, suggestion=suggestion, basis=basis, json=json.dumps(examples))

@app.route("/add/")
@app.route("/add/<word>")
def add(word=None):
    if word is None:
        word = flask.request.args.get('word', None)
    if word:
        examples.append(word)
    return flask.redirect(flask.url_for("main"))

@app.route("/reset/")
def reset():
    global examples, blacklist
    examples = []
    blacklist = []
    return flask.redirect(flask.url_for("main"))

@app.route("/block/<word>")
def block(word):
    blacklist.append(word)
    return flask.redirect(flask.url_for("main"))

@app.route("/remove/<word>")
def remove(word):
    examples.remove(word)
    blacklist.append(word)
    return flask.redirect(flask.url_for("main"))

fasttext.load()
app.run(port=PORT)