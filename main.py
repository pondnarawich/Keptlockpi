from flask import Flask
from flask import request
import requests

app = Flask(__name__)

@app.route('/keptlock/unlock')