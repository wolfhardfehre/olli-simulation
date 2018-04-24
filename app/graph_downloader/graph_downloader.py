import requests
import pandas as pd
from app.tools.geo_tools import meters


DEFAULT_URL = 'https://www.overpass-api.de/api/interpreter'
QUERY_TEMPLATE = '[out:json];way[highway]({:f},{:f},{:f},{:f});out geom;'


def fetch_geometries(bounding_box, url=DEFAULT_URL):
    params = dict(data=QUERY_TEMPLATE.format(*bounding_box))
    resp = requests.get(url=url, params=params)
    return resp.json()


class Downloader:

    def __init__(self, json):
        print("downloading overpass data...")
        self.json = json
        self.nodes = self.__nodes()
        self.edges = self.__edges()

    def __nodes(self):
        print('building nodes...')
        nodes = []
        for element in self.json['elements']:
            for nid, geom in zip(element['nodes'], element['geometry']):
                nodes.append({'id': nid, 'lat': geom['lat'], 'lon': geom['lon']})
        return self.__build_nodes(nodes)

    def __edges(self):
        print('building edges...')
        edges = []
        for element in self.json['elements']:
            for first, second in zip(element['nodes'][:-1], element['nodes'][1:]):
                edges.append({'node1': first, 'node2': second})
        return self.__build_edges(edges)

    def __build_edges(self, edge_list):
        edges = pd.DataFrame(edge_list)
        edges = edges.join(self.nodes, on='node1', rsuffix='_from')
        edges = edges.join(self.nodes, on='node2', rsuffix='_to')
        edges['distance'] = edges.apply(lambda row: self.__distance(row), axis=1)
        return edges[['node1', 'node2', 'distance']]

    @staticmethod
    def __build_nodes(node_list):
        nodes = pd.DataFrame(node_list)
        nodes.drop_duplicates('id', inplace=True)
        nodes.set_index('id', inplace=True)
        return nodes

    @staticmethod
    def __distance(row):
        return meters(row['lat'], row['lon'], row['lat_to'], row['lon_to'])

    def save(self):
        self.nodes.to_pickle("./resources/nodes.p")
        self.edges.to_pickle("./resources/edges.p")


if __name__ == '__main__':
    NORTH = 52.484421
    SOUTH = 52.479951
    WEST = 13.352029
    EAST = 13.359325

    json = fetch_geometries([SOUTH, WEST, NORTH, EAST])

    downloader = Downloader(json)
    downloader.save()
    print("*** NODES ***")
    print(downloader.nodes)
    print("*** EDGES ***")
    print(downloader.edges)
