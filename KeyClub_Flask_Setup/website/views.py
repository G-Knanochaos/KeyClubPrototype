from flask import Blueprint, redirect, url_for, render_template
from website.fetching import fetch

views = Blueprint('views', __name__)

#FOR DEBUGGING PURPOSES
@views.route('base')
def base():
    return render_template("base.html")    

@views.route('')
def default():
    events = fetch("events")
    images = fetch("images",payload={"n":8})
    cabinet = fetch("Sheets",payload={
        "name":"Cabinet Display",
        "n":4
    },json_name="cabinet_info",override=True)
    return render_template("index.html", images=images, events=events, cabinet=cabinet)


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
    cabinet = fetch("Sheets",payload={
        "name":"Cabinet Display",
        "all":True
    },json_name="cabinet_info",override=True)
    return render_template("about-leadership.html", cabinet=cabinet)

@views.route("events")
def events():
    return render_template("events.html")

@views.route("past-events")
def past_events():
    return render_template("past-events.html")

@views.route("resources-faq.html")
def faq():
    faqs = fetch("Sheets",payload={
        "name":"FAQ",
        "all":True
    },json_name="FAQ",override=True)
    return render_template("resources-faq.html", faqs=faqs)

@views.route("resources-misc.html")
def misc():
    misc = fetch("Misc",override=True)
    print(misc)
    return render_template("resources-misc.html",misc=misc)

@views.route("resources-newsletters.html")
def newsletters():
    return render_template("resources-newsletters.html")

