from flask import render_template, request, jsonify
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app.app.app import app
from app.app.models import VehicleStates
from app.app.models import geo_jsonify
from app.app.secret import TOKEN
from app.app.generators.animate_generator import AnimateGenerator
from app.app.generators.random_generator import RandomGenerator
from app.app.generators.round_trip_generator import RoundTripGenerator
from app.app.generators.on_demand_generator import OnDemandGenerator
from app.app.routing.booking import Booking
from app.app.routing.graph import Graph
from shapely.geometry import Point


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
def animate_shuttle():
    """
    Route endpoint to show animated real shuttle data within a certain time range.

    Returns:
        rendered website displaying moving point.

    """
    return render_template('animate_index.html', token=TOKEN)


@app.route('/animate_feed')
def animate_feed():
    """
    Get GeoJson for an animation.

    Returns:
        a GeoJson.

    """
    generator = AnimateGenerator.get_instance()
    return jsonify(generator.next())


@app.route('/random')
def random_shuttle():
    """
    Route endpoint to show animated real shuttle data within a certain time range.

    Returns:
        rendered website displaying moving point.

    """
    return render_template('random_index.html', token=TOKEN)


@app.route('/random_feed')
def random_feed():
    """
    Get GeoJson for an animation.

    Returns:
        a GeoJson.

    """
    generator = RandomGenerator.get_instance()
    return jsonify(generator.next())


@app.route('/round_trip')
def round_trip():
    return render_template('round_trip_index.html', token=TOKEN)


@app.route('/on_demand')
def on_demand():
    return render_template('on_demand_index.html', token=TOKEN)


@app.route('/on_demand_feed')
def on_demand_feed():
    generator = OnDemandGenerator.get_instance()
    return jsonify(generator.next())


@app.route('/on_demand_ground_feed')
def on_demand_ground_feed():
    generator = OnDemandGenerator.get_instance()
    return jsonify(generator.current_ground_data())


@app.route('/book_trip', methods=['POST'])
def book_trip():
    generator = OnDemandGenerator.get_instance()
    g = Graph.load_default()
    raw_start_position = Point(float(request.form['start_lon']), float(request.form['start_lat']))
    raw_end_position = Point(float(request.form['end_lon']), float(request.form['end_lat']))

    start_station = g.get_closest_node(raw_start_position)
    end_station = g.get_closest_node(raw_end_position)

    booking = Booking(
        start_station,
        end_station,
        int(request.form['earliest_departure']),
        int(request.form['latest_arrival'])
    )
    generator.add_booking(booking)
    return 'OK'


@app.route('/round_trip_feed')
def round_trip_feed():
    generator = RoundTripGenerator.get_instance()
    return jsonify(generator.next())


@app.route('/round_trip_ground_feed')
def round_trip_ground_feed():
    generator = RoundTripGenerator.get_instance()
    return jsonify(generator.current_ground_data())


def render_to_static(start_time, end_time):
    results = VehicleStates.query.filter(VehicleStates.last_seen.between(start_time, end_time))
    results = geo_jsonify(results.all())
    return render_template('static_index.html', token=TOKEN, vehicle_states=results)


if __name__ == '__main__':
    app.run()
