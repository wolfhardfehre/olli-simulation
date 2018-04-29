import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from flask import render_template, request, jsonify
from app.app.app import app
from app.app.models import VehicleStates
from app.app.models import geo_jsonify
from app.app.secret import TOKEN
from app.app.state_generator import StateGenerator


@app.route('/')
def static_shuttle_between():
    """
    Route endpoint to show real shuttle data within a certain time range at once.

    Returns:
        rendered website displaying all points at once.

    Example:
        http://127.0.0.1:5000/?start_time=2018-02-14%2015:40:00&end_time=2018-02-14%2016:02:00
    """
    start_time = request.args.get('start_time', default="2018-02-14 13:00:00")
    end_time = request.args.get('end_time', default="2018-02-14 17:00:00")
    return render_to_static(start_time, end_time)


@app.route('/animate')
def animate_shuttle_between():
    """
    Route endpoint to show animated real shuttle data within a certain time range.

    Returns:
        rendered website displaying moving point.

    """
    return render_template('animated_index.html', token=TOKEN)


@app.route('/animation_feed')
def animation_feed():
    """
    Get GeoJson for an animation.

    Returns:
        a GeoJson.

    """
    state_generator = StateGenerator.get_instance()
    longitude, latitude, properties = state_generator.next()
    return jsonify({
        'geometry': {
            'type': 'Point',
            'coordinates': [
                longitude, latitude
            ]
        },
        'type': 'Feature',
        'properties': properties
    })


def render_to_static(start_time, end_time):
    results = VehicleStates.query.filter(VehicleStates.last_seen.between(start_time, end_time))
    results = geo_jsonify(results.all())
    return render_template('static_index.html', token=TOKEN, vehicle_states=results)


if __name__ == '__main__':
    app.run()
