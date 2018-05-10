from app.app.routing.dijkstra import shortest_path
from app.app.entities.route import Route


class Routes:

    def __init__(self, tour, graph, stations, velocity):
        self.tour = tour
        self.graph = graph.graph
        self.stations = stations
        self.velocity = velocity
        self.route_count = 0
        self.routes = self.__build_routes()

    def get_next(self):
        route = self.routes[self.route_count]
        self.route_count += 1
        if self.route_count == len(self.routes):
            self.route_count = 0
        return route

    def __build_routes(self):
        stations = self.stations + [self.stations[0]]
        station_ids = [station.node_id for station in stations]
        paths = [shortest_path(self.graph, o, d) for o, d in zip(station_ids[:-1], station_ids[1:])]
        return [Route(self.graph, path, self.tour, self.velocity) for path in paths]
