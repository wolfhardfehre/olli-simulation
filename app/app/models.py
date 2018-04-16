from app import db
from geoalchemy2 import Geography

db.reflect()


def geo_jsonify(vehicles_states):
    jsonified = [i.to_geojson for i in vehicles_states]
    return {"type": "FeatureCollection", "features": jsonified}


class VehicleStates(db.Model):
    __tablename__ = 'vehicle_states'

    @property
    def to_geojson(self):
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(self.longitude), float(self.latitude)]
            },
            "style": {
                "color": "#3182BD",
                "fillOpacity": 0.5,
                "weight": 2,
                "radius": 2,
                "opacity": 0.7
            },
            "properties": {
                "id": self.id
            }
        }
