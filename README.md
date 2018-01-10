# Ketchum: build collections of words

This is code for generating lists of similar words, using word vector similarities from the [fasttext][fasttext] data, released by Facebook. It's useful for building collections of words to slot into generative grammars, such as Kate Compton's [tracery][tracery].

## Setup

The code has a few code dependencies, listed in `requirements.txt`. You'll need recent-ish versions of the `annoy`, `flask` and `numpy` libraries. `pip3 install -r requirements.txt` will grab them, if you don't already have them installed. I've only tested it on Python 3, but it shouldn't be difficult to translate it to Python 2 if you're really fussed.

Start the server by running `python3 ketchum.py`. The first time it runs, it will take a while (about half an hour on my machine) to download data and build some indices. You'll need around 2.5GB of free disk space, and a decent amount of RAM. Once this process has run once, subsequent runs should be pretty zippy.

The server runs on port 8765 (you can change this at the top of `ketchum.py`). Point your web browser at http://127.0.0.1:8765/ and have a play around.

## Support, licensing, ongoing development

This project is a proof-of-concept experiment. I might revisit it in the future, but I'm far more likely to build something new using similar ideas.

The code is available under the [MIT license][license], so you can fork it,
improve it, learn from it, build upon it. However, I have no interest in
maintaining it as an ongoing open source project, nor in providing support for
it. Pull requests will be either ignored or closed.

If you do make something interesting with this code, please do still let me know! I'm sorry that I can't provide much support, but I am still genuinely interested in seeing creative applications of the code and/or ideas.

[license]: https://github.com/mewo2/ketchum/blob/master/LICENSE.md
[fasttext]: https://fasttext.cc/
[tracery]: http://www.tracery.io/