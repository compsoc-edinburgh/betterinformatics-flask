from flask import Flask
app = Flask(__name__)

import betterinformatics.views
from betterinformatics.bi import BI


