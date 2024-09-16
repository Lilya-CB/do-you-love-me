# Copyright 2024 Lilya Benladjreb BENL28549807
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask
from flask import render_template
from flask import g
from flask import request
import random
from .database import Database

app = Flask(__name__, static_url_path="", static_folder="static")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.route('/')
def index():
    database = Database()
    liste_animaux = random.sample(get_db().get_animaux(), k=5)
    return render_template('index.html', liste_animaux=liste_animaux)


@app.route('/recherche')
def recherche():
    query = request.args.get('query').lower()
    animaux = get_db().get_animaux()
    filter_animaux = _filter_animaux(animaux, query)
    return render_template('resultat.html', animaux=filter_animaux)


@app.route('/animal/<animal_id>')
def animal_id(animal_id):
    database = Database()
    animal_id = database.get_animal(animal_id)
    return render_template('animal.html', animal=animal_id)


@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/soumettreformulaire', methods=["POST"])
def soumettreformulaire():
    error = ""
    nomAnimal = request.form["nom-animal"]
    especeAnimal = request.form["espece-animal"]
    raceAnimal = request.form["race-animal"]
    ageAnimal = request.form["age-animal"]
    descriptionAnimal = request.form["description-animal"]
    emailContact = request.form["email-contact"]
    adresseContact = request.form["adresse-contact"]
    villeContact = request.form["ville-contact"]
    cpContact = request.form["cp-contact"]

    if not nomAnimal or not nomAnimal.strip():
        error = True
    elif "," in nomAnimal:
        error = True
    elif len(nomAnimal) < 3 or len(nomAnimal) > 20:
        error = True

    if not especeAnimal or not especeAnimal.strip():
        error = True
    elif "," in especeAnimal:
        error = True

    if not raceAnimal or not raceAnimal.strip():
        error = True
    elif "," in raceAnimal:
        error = True

    if not ageAnimal or not ageAnimal.strip():
        error = True
    elif int(ageAnimal) < 0 or int(ageAnimal) > 20:
        error = True

    if not descriptionAnimal or not descriptionAnimal.strip():
        error = True
    elif "," in descriptionAnimal:
        error = True

    if not emailContact or not emailContact.strip():
        error = True
    elif "," in emailContact:
        error = True

    if not adresseContact or not adresseContact.strip():
        error = True
    elif "," in adresseContact:
        error = True

    if not villeContact or not villeContact.strip():
        error = True
    elif "," in nomAnimal:
        error = True

    if not cpContact or not cpContact.strip():
        error = True
    elif "," in cpContact:
        error = True

    if error:
        return f"SVP ne pas surpasser les critères de validations", 500
    else:
        database = Database()
        database.add_animal(nomAnimal, especeAnimal, raceAnimal, ageAnimal,
                            descriptionAnimal, emailContact, adresseContact,
                            villeContact, cpContact)

    return render_template("confirmation.html", nomAnimal=nomAnimal,
                           especeAnimal=especeAnimal,
                           raceAnimal=raceAnimal,
                           ageAnimal=ageAnimal,
                           descriptionAnimal=descriptionAnimal,
                           emailContact=emailContact,
                           adresseContact=adresseContact,
                           villeContact=villeContact,
                           cpContact=cpContact)


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


def _filter_animaux(animaux, query):
    filter_animaux = []
    for animal in animaux:
        if animal['espece'].lower() in query or animal['nom'].lower() in query:
            filter_animaux.append(animal)
    return filter_animaux
