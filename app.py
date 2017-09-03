from functools import partial

from flask import Flask, render_template
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

#
# Models
#
class Continent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

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

#
# Forms
#
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

#
# Routes
#
@app.route("/")
def index():
    form = ContinentForm()
    return render_template("index.html", form=form)


#
# Local code execution
#
print("Creating database")
db.create_all()
print("Seeding database")
seed_database(db)
