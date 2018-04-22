from flask import render_template, request, jsonify
from app import app
from secret import TOKEN
import models
from state_generator import StateGenerator


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
    Get GeoJson for a animation.

    Returns:
        a GeoJson.

    """
    state_generator = StateGenerator.get_instance()
    longitude, latitude = state_generator.next_coordinate()
    return jsonify({
        'geometry': {
            'type': 'Point',
            'coordinates': [
                longitude, latitude
            ]
        },
        'type': 'Feature',
        'properties': {}
    })


def render_to_static(start_time, end_time):
    results = models.VehicleStates.query.filter(models.VehicleStates.last_seen.between(start_time, end_time))
    results = models.geo_jsonify(results.all())
    return render_template('static_index.html', token=TOKEN, vehicle_states=results)


if __name__ == '__main__':
    app.run()
