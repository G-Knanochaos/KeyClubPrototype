from flask import Blueprint, redirect, url_for, render_template
import requests #to communicate with events appscript proxy
import json
from datetime import date
import os

requests_map = {
    "events":"https://script.google.com/macros/s/AKfycbzQFrs5AnxX-JjJuBOt_B41QoHLyc2iUmREIcJzIql6nzWW7VOxiTMNJchRK6Ptltjwlg/exec",
    "images":"https://script.google.com/macros/s/AKfycbzdLT7ZYBBf50gHiWll_qUatXHToagXeSqRsra7U1gitvEkDpgsUVXm-dr311D6BYzZ/exec"
}
def fetch(type="events",n=4,s=1):
    print(f"Fetching {type}!")
    url = url_for("static", filename = f"json/{type}.json")
    add = False
    with open(os.path.join(os.path.dirname(__file__),url[1:]), "r") as file:
        f = json.load(file)
    if f.get("date",None) == date.today():
        if len(f[type]) == n:
            return f[type]
        add = True
    n = len(f[type])-n
    payload = {"s":str(s),"n":str(n)}


    r = requests.get(requests_map[type], params = {}).text #wtf man

    print(r)
    j = json.loads(r)
    j["date"] = date.today().strftime('%m/%d/%Y')
    print(j[type])
    result = (f[type] if add else [])+j[type]
    with open(os.path.join(os.path.dirname(__file__),url[1:]), "w") as file:
        file.write(json.dumps(j))
    return result


views = Blueprint('views', __name__)

#FOR DEBUGGING PURPOSES
@views.route('base')
def base():
    return render_template("base.html")    

@views.route('')
def default():
    events = fetch("events")
    images = fetch("images")
    print(images)
    return render_template("index.html", images=images, events=events)

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

