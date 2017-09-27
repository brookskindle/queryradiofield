from functools import partial

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, widgets
from wtforms.ext.sqlalchemy.fields import (
    QuerySelectField,
    QuerySelectMultipleField,
)


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"  # Use in-memory database
app.debug = True
db = SQLAlchemy(app)

QueryRadioField = partial(
    QuerySelectField,
    widget=widgets.ListWidget(prefix_label=False),
    option_widget=widgets.RadioInput(),
)
QueryCheckboxField = partial(
    QuerySelectMultipleField,
    widget=widgets.ListWidget(prefix_label=False),
    option_widget=widgets.CheckboxInput(),
)


class Continent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __init__(self, name):
        self.name = name


def seed_database(db):
    """Seed the given database with a list of continents"""
    continent_names = (
        "Asia",
        "Africa",
        "North America",
        "South America",
        "Antarctica",
        "Europe",
        "Australia",
    )
    for name in continent_names:
        continent = Continent(name=name)
        db.session.add(continent)
    db.session.commit()


class ContinentForm(Form):
    select_continents = QuerySelectField(
        "Continents",
        query_factory=lambda: Continent.query,
        get_label=lambda field: field.name,
    )
    select_multiple_continents = QuerySelectMultipleField(
        "Continents",
        query_factory=lambda: Continent.query,
        get_label=lambda field: field.name,
    )
    radio_continents = QueryRadioField(
        "Continents",
        query_factory=lambda: Continent.query,
        get_label=lambda field: field.name,
    )
    checkbox_continents = QueryCheckboxField(
        "Continents",
        query_factory=lambda: Continent.query,
        get_label=lambda field: field.name,
    )


@app.route("/", methods=["GET", "POST"])
def index():
    form = ContinentForm(request.form)
    return render_template("index.html", form=form)


print("Creating database")
db.create_all()
print("Seeding database")
seed_database(db)
