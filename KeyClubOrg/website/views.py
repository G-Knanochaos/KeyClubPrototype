from flask import Blueprint, redirect, url_for, render_template, request, jsonify, flash
from flask_login import login_required, current_user
from . import db

views = Blueprint('views', __name__)

@views.route('')
def default():
    return render_template("index.html", user=current_user)

@views.route('landing')
def landing():
    return redirect(url_for("views.default"))
    # redirects to default page for people who search url/home

@views.route('home')
def home():
    return redirect(url_for("views.default"))
    # redirects to default page for people who search url/home

@views.route('about')
def about():
    return render_template("about.html", user=current_user)

@views.route('events')
def create():
    return render_template("events.html", user=current_user)

@views.route('profile')
@login_required
def profile():
    return render_template("profile.html", user=current_user)

