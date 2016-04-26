from flask import render_template
from flask import Markup
import markdown

from betterinformatics import app


@app.route('/')
def index():
    content = """
Chapter
=======

Section
-------

* Item 1
* Item 2
"""
    content = Markup(markdown.markdown(content))
    return render_template('index.html', **locals())
