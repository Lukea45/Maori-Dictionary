from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def render_homepage():
    return render_template("home.html")

@app.route('/action')
def render_action_page():
    return render_template("action.html")

@app.route('/animals')
def render_animals_page():
    return render_template("animals.html")

@app.route('/clothing')
def render_clothing_page():
    return render_template("clothing.html")

@app.route('/culture')
def render_culture_page():
    return render_template("culture.html")

@app.route('/descriptive')
def render_descriptive_page():
    return render_template("descriptive.html")

@app.route('/edibles')
def render_edibles_page():
    return render_template("edibles.html")

@app.route('/emotions')
def render_emotions_page():
    return render_template("emotions.html")

@app.route('/garbage')
def render_garbage_page():
    return render_template("garbage.html")

@app.route('/number')
def render_number_page():
    return render_template("number.html")

@app.route('/outdoors')
def render_outdoors_page():
    return render_template("outdoors.html")

@app.route('/people')
def render_people_page():
    return render_template("people.html")

@app.route('/places')
def render_places_page():
    return render_template("places.html")

@app.route('/plants')
def render_plants_page():
    return render_template("plants.html")

@app.route('/school')
def render_school_page():
    return render_template("school.html")

@app.route('/sport')
def render_sport_page():
    return render_template("sport.html")

@app.route('/technology')
def render_technology_page():
    return render_template("technology.html")

@app.route('/time')
def render_time_page():
    return render_template("time.html")






app.run(host='0.0.0.0', debug=True)
