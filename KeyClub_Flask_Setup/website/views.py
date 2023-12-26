from flask import Blueprint, redirect, url_for, render_template
from website.fetching import fetch, requests_map
from flask import Flask, request


views = Blueprint('views', __name__)

#FOR DEBUGGING PURPOSES
@views.route('base')
def base():
    return render_template("base.html")    

@views.route('')
def default():
    events = fetch("events",n=4)
    images = fetch("images",n=8,interval=30)
    cabinet = fetch("Sheets",json_name="cabinet_info",override=True,
        name="Cabinet Display",
        n=4)

    return render_template("index.html", images=images, events=events, cabinet=cabinet)


@views.route('landing')
def landing():
    return redirect(url_for("views.default"))

@views.route('home')
def home():
    return redirect(url_for("views.default"))

@views.route("about-division")
def about_division():
    service = fetch("tracker",json_name = "service_tracker",interval=30,name="Service Tracker",n=1) 
    funds = fetch("tracker",json_name="funds_tracker",interval=30,name="Funds Tracker",n=1) 
    return render_template("about-division.html",service=service,funds=funds) 

@views.route("about-keyclub")
def about_keyclub():
    return render_template("about-keyclub.html")

@views.route("about-leadership")
def about_leadership():
    cabinet = fetch("Sheets",json_name="cabinet_info",override=True,interval=1,name="Cabinet Display")
    return render_template("about-leadership.html", cabinet=cabinet)

@views.route("events")
def events():
    events =  fetch("events",n=4)
    images = fetch("images",n=8,interval=30)
    return render_template("events.html", events=events, images=images)

@views.route("past-events")
def past_events():
    images = fetch("past_photos",interval=1,all=True)
    return render_template("past-events.html", images=images,interval=30)

@views.route("resources-faq.html")
def faq():
    faqs = fetch("Sheets",json_name="FAQ",override=True,interval=2,
        name="FAQ",
        all=True
    )
    return render_template("resources-faq.html", faqs=faqs)

@views.route("resources-misc.html")
def misc():
    misc = fetch("Misc",override=True)
    print(misc)
    return render_template("resources-misc.html",misc=misc)

@views.route("resources-newsletters.html")
def newsletters():
    return render_template("resources-newsletters.html")

@views.route("api/fetch")
def fetchResources():
    args = request.args
    return fetch(**args)