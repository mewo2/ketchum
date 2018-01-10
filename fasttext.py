import annoy
import pickle
import numpy as np
from urllib.request import urlretrieve
import os
import zipfile

FASTTEXT_URL = 'https://s3-us-west-1.amazonaws.com/fasttext-vectors/wiki-news-300d-1M-subword.vec.zip'
row2str = None
str2row = None
ann = None

def load():
    global row2str, str2row, ann
    if ann is not None:
        return
    try:
        row2str, str2row = pickle.load(open("data/fasttext.pickle", "rb"))
        ann = annoy.AnnoyIndex(300)
        ann.load("data/fasttext.annoy")
    except IOError:
        return download_data()

    

def download_data():
    global row2str, str2row, ann
    print("Retrieving fasttext vectors...")
    try:
        os.mkdir('data')
    except FileExistsError:
        pass
    try:
        zf = zipfile.ZipFile('data/fasttext.zip')
        print("Already downloaded!")
    except IOError:
        urlretrieve(FASTTEXT_URL, 'data/fasttext.zip')
        print("Downloaded")
        zf = zipfile.ZipFile('data/fasttext.zip')

    filename = zf.namelist()[0]
    print(f"Reading {filename}")
    lines = zf.open(filename).readlines()

    nwords, ndim = [int(x) for x in lines[0].split()]
    print(f"Got {nwords} words with {ndim} dimensions")
    
    vecs = np.zeros((nwords, ndim))

    row2str = {}
    str2row = {}
    for i, line in enumerate(lines[1:]):
        tokens = line.decode().split(' ')
        w = tokens[0]
        row2str[i] = w
        str2row[w] = i
        vec = [float(x) for x in tokens[1:-1]]
        vecs[i,:] = vec
        if i % 10000 == 0:
            print(f"Processing word {i}: {w}")
    print("Saving indices")
    pickle.dump((row2str, str2row), open("data/fasttext.pickle", "wb"))

    print("Normalizing vectors")
    nvecs = vecs / ((vecs ** 2).sum(1) ** 0.5)[:,np.newaxis]

    print("Building annoy index")
    ann = annoy.AnnoyIndex(300)
    for i, v in enumerate(nvecs):
        ann.add_item(i, v)
    ann.build(10)
    print("Saving annoy index")
    ann.save('data/fasttext.annoy')


def vector(w):
    load()
    if w not in str2row:
        return np.zeros((300,))
    return ann.get_item_vector(str2row[w])

def words_near(v, n):
    load()
    idxs = ann.get_nns_by_vector(v, n)
    return [row2str[i] for i in idxs if i in row2str]

def suggest(words, blacklist):
    v = np.sum([vector(w) for w in words], 0)
    lowers = [w.lower() for w in blacklist]

    n = 10
    while True:
        for w in words_near(v, n):
            if w.lower() not in lowers:
                return w
        n *= 2