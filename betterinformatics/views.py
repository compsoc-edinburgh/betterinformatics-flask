from flask import render_template, redirect
from flask import Markup
import markdown

from betterinformatics import app

@app.route('/')
def index():
    return redirect('/home')
