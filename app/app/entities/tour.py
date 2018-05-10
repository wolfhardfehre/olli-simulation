from app.app.entities.routes import Routes
from app.app.entities.transport_stations import TransportStations
from app.app.entities.charge_stations import ChargeStations


class Tour:

    def __init__(self, graph, velocity, battery):
        self.graph = graph
        self.battery = battery
        self.transport_stations = TransportStations(self, graph)
        self.charge_stations = ChargeStations(self, graph, velocity, battery)
        self.routes = Routes(self, graph, self.transport_stations.stations, velocity)
        self.route = self.routes.get_next()
        self.story = self.route
        self.__has_low_battery = False

        self.total_distance = 0
        self.speed = 0
        self.position = None
        self.azimuth = 0
        self.door_status = 'closed'
        self.is_low_battery_route = False

    @property
    def battery_status(self):
        return self.battery.status

    def change_speed(self, speed):
        self.speed = speed

    def change_doors(self, doors):
        self.door_status = doors

    def change_position(self, position):
        self.position = position

    def change_meters(self, meters):
        self.total_distance += meters
        self.battery.update(meters)

    def change_azimuth(self, azimuth):
        self.azimuth = azimuth

    def update(self, time):
        self.story.update(time)
        if self.story.has_ended():
            self.next_story()

    def next_story(self):
        if self.story.get_type() == 'Route':
            if self.is_low_battery_route:
                self.is_low_battery_route = False
                self.story = self.charge_stations.get_target_station()
            else:
                self.story = self.transport_stations.get_next()
        elif self.story.get_type() == 'TransportStation':
            if self.battery.low_battery():
                self.is_low_battery_route = True
                self.story = self.charge_stations.get_route_to_closest(self.story.node_id)
            else:
                self.story = self.routes.get_next()
        elif self.story.get_type() == 'ChargeStation':
            # TODO: route to next staion and skip next route
            self.story = self.routes.get_next()

    def to_geojson(self):
        return self.transport_stations.to_geojson() + \
               self.charge_stations.to_geojson() + \
               [self.story.highlight()]
