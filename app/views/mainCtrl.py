from flask import Response, render_template
from app.models.models import User
from app import db
from flask_login import current_user, login_required


def main():
    return render_template('main.html')


def product():
    return render_template('product.html')


def aboutUs():
    return render_template('about.html')


def contactUs():
    return render_template('contact.html')
