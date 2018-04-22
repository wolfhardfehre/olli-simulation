from flask import render_template, request
from sqlalchemy import and_

from app import app
from secret import TOKEN
from app import db
from sqlalchemy.sql import select
import models
import pandas as pd
import datetime as dt


animation_start_time = None
animation_data = None


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
    start_time = request.args.get('start_time', default='2018-02-14 13:00:00')
    end_time = request.args.get('end_time', default='2018-02-14 17:00:00')
    return render_to_animated(start_time, end_time)


@app.route('/animation_feed')
def animation_feed():
    """
    Get GeoJson for a animation.

    Returns:
        a GeoJson.

    """

    return render_to_animated(start_time, end_time)


def render_to_static(start_time, end_time):
    results = models.VehicleStates.query.filter(models.VehicleStates.last_seen.between(start_time, end_time))
    results = models.geo_jsonify(results.all())
    return render_template('static_index.html', token=TOKEN, vehicle_states=results)


def render_to_animated(start_time, end_time):
    animation_start_time = dt.datetime.now()

    query = select([models.VehicleStates])\
        .where(
            and_(
                models.VehicleStates.last_seen > start_time,
                models.VehicleStates.last_seen < end_time
            )
        )
    df = pd.read_sql_query(sql=query, con=db.engine, parse_dates=['last_seen', 'created_at'])
    animation_data = df.iterrows()
    return render_template('animated_index.html', token=TOKEN)


if __name__ == '__main__':
    app.run()
