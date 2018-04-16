from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from secret import TOKEN
import config

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


import models


@app.route('/')
def index():
    return render("2018-02-14 13:00:00", "2018-02-14 17:00:00")


@app.route('/<start_time>/<end_time>')
def date_range(start_time, end_time):
    return render(start_time, end_time)


def render(start_time, end_time):
    results = models.VehicleStates.query.filter(models.VehicleStates.last_seen.between(start_time, end_time))
    results = models.geo_jsonify(results.all())
    return render_template('index.html', token=TOKEN, vehicle_states=results)


if __name__ == '__main__':
    app.run()
