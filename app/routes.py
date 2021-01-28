from flask import render_template, request, redirect, session, url_for
from app.trade import simulate
from app import app
import time

tickers = [
    "AAPL", "TSLA", "AMZN", "GE", "DIS", "SNE", "TAN","VOO", "NVDA", "GLOB", "PLTR", "WMT"
]
tickers.sort()

@app.route("/",methods=["GET","POST"])
def form():
    if request.method == "POST":
        try:
            tick = request.form['tick']
            strat = request.form['strat']
            period = request.form['period']
            session['img'] = simulate(tick,strat,period)
            return redirect(url_for('show'))
        except:
            pass
    return render_template("form.html",tickers=tickers)

@app.route("/show",methods=["GET","POST"])
def show():
    if 'img' in session:
        img = session['img']
        session.pop('img')
        return render_template("modal.html",tickers=tickers,png=img)
    else:
        return "<h1>ERROR</h1>"