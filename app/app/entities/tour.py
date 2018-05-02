from app.app.routing.dijkstra import shortest_path


class Tour:

    def __init__(self, graph, background):
        self.graph = graph
        self.route_count = 0
        self.edge_count = 0
        self.storyline = self.__build(background)
        self.route = self.storyline[self.route_count]

    def next_story(self):
        self.route = self.storyline[self.route_count]
        edge = self.route.edges[self.edge_count]
        position = edge.origin.geometry
        self.edge_count += 1
        if self.edge_count >= len(self.route.edges):
            self.route_count += 1
            self.edge_count = 0
            if self.route_count >= len(self.storyline):
                self.route_count = 0
        return position, edge

    def get_route(self):
        return self.route.to_geojson()

    def __build(self, background):
        station_ids = background.closest_station_ids
        station_ids = station_ids + [station_ids[0]]
        return [shortest_path(self.graph, o, d) for o, d in zip(station_ids[:-1], station_ids[1:])]
