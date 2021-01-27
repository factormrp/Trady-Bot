from flask import Flask

app = Flask(__name__)
app.secret_key = "S0m3th1nG"

from app import routes