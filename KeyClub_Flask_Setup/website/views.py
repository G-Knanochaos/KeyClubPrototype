from flask import Blueprint, redirect, url_for, render_template, request, jsonify, flash


views = Blueprint('views', __name__)

#FOR DEBUGGING PURPOSES
@views.route('base')
def base():
    return render_template("base.html")




@views.route('')
def default():
    return render_template("index.html")

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

