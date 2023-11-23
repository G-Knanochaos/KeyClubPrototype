from flask import Blueprint, redirect, url_for, render_template
import requests #to communicate with events appscript proxy
import json
from datetime import date
import os
from time import time

requests_map = {
    "events":"https://script.google.com/macros/s/AKfycbzQFrs5AnxX-JjJuBOt_B41QoHLyc2iUmREIcJzIql6nzWW7VOxiTMNJchRK6Ptltjwlg/exec",
    "images":"https://script.google.com/macros/s/AKfycbzdLT7ZYBBf50gHiWll_qUatXHToagXeSqRsra7U1gitvEkDpgsUVXm-dr311D6BYzZ/exec",
    "FAQs":"https://script.google.com/macros/s/AKfycbwOy_dZXH1prFKOj_ZU-mgU9Vodot-KYK5FSpA0uPX8RyKlSNN6Lls8GZshkNGEoWoi6Q/exec",
    "Misc":"https://script.google.com/macros/s/AKfycbzmioExdkHHboQDNtZUjMjAlgcKrYutKkjZrJv3DpT0q-ruQI3tzo-wtChISbxLAnM/exec"
}
def fetch(type="events",n=4,s=1,override=False):#if override is set to True, changes won't be fetched until next day and changes will completely overwrite past state
    print(f"Fetching {type}!")
    url = url_for("static", filename = f"json/{type}.json")
    today = date.today().strftime("%m%d%y")
    with open(os.path.join(os.path.dirname(__file__),url[1:]), "r") as file:
        try: 
            f = json.load(file)
        except Exception as e:
            print("File JSON parsing error, emptying file and refetching data")
            print(e)
            f = {"date":None,type:[]}
    print(f.get("date"),today)
    if f.get("date",None) == today:
        print(len(f[type]),n)
        if override or len(f[type]) >= n:
            return f[type]
    
    n = n-len(f.get(type))
    payload = {"s":str(s),"n":str(n)}

    r = requests.get(requests_map[type],params = payload).text

    print(r)
    j = json.loads(r)
    j["date"] = today
    j[type] = (f[type] if not override else [])+j[type]
    with open(os.path.join(os.path.dirname(__file__),url[1:]), "w") as file:
        file.write(json.dumps(j))
    return j[type]

views = Blueprint('views', __name__)

#FOR DEBUGGING PURPOSES
@views.route('base')
def base():
    return render_template("base.html")    

@views.route('')
def default():
    start = time()
    events = fetch("events")
    print(f"Fetched events in {time()-start}")
    images = fetch("images",8)
    print(f"Fetched images in {time()-start}")
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
    faqs = fetch("FAQs",override=True)
    return render_template("resources-faq.html", faqs=faqs)

@views.route("resources-misc.html")
def misc():
    misc = fetch("Misc",override=True)
    print(misc)
    return render_template("resources-misc.html",misc=misc)

@views.route("resources-newsletters.html")
def newsletters():
    return render_template("resources-newsletters.html")

