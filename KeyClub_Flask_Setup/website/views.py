from flask import Blueprint, redirect, url_for, render_template, request
import requests #to communicate with events appscript proxy
import json
from datetime import date
import os

views = Blueprint('views', __name__)

#FOR DEBUGGING PURPOSES
@views.route('base')
def base():
    return render_template("base.html")

def fetch_events(s=1,n=4): #group multiplier, group size
    url = url_for("static", filename = "json/events.json")
    file = open(os.path.join(os.path.dirname(__file__),url[1:]), "r+")
    f = json.load(file)
    if f.get("date",None) == date.today():
        file.close()
        return f
    payload = {"s":str(s),"n":str(n)}
    r = json.loads(requests.get("https://script.google.com/macros/s/AKfycbyLcJe2rVvdbOofKLTjTVaTy3Tprh6VW6lLwsJ_YUIaDL2hgk8nGaLLlzSJahIMRGVEwQ/exec", 
                                params = payload).text)
    r["date"] = date.today()
    file.write(r)
    file.close()
    return r
    

@views.route('')
def default():
    events = fetch_events()
    return render_template("index.html", **events)

@views.route('landing')
def landing():
    return redirect(url_for("views.default"))

@views.route('home')
def home():
    return redirect(url_for("views.default"))

@views.route("about-division")
def about_division():
    return render_template("about-division.html")

@views.route("about-keyclub")
def about_keyclub():
    return render_template("about-keyclub.html")

@views.route("about-leadership")
def about_leadership():
    return render_template("about-leadership.html")

@views.route("events")
def events():
    return render_template("events.html")

@views.route("past-events")
def past_events():
    return render_template("past-events.html")

@views.route("resources-faq.html")
def faq():
    return render_template("resources-faq.html")

@views.route("resources-misc.html")
def misc():
    return render_template("resources-misc.html")

@views.route("resources-newsletters.html")
def newsletters():
    return render_template("resources-newsletters.html")

