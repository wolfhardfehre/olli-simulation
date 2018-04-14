import requests
import logging
import pandas as pd
from app.geo_tools import meters

logging.basicConfig(level=logging.DEBUG)

NORTH = 52.484421
SOUTH = 52.479951
WEST = 13.352029
EAST = 13.359325

bbox = [SOUTH, WEST, NORTH, EAST]

url = 'https://www.overpass-api.de/api/interpreter'
params = dict(data='[out:json];way[highway][highway=service]({:f},{:f},{:f},{:f});out geom;'.format(*bbox))

resp = requests.get(url=url, params=params)
data = resp.json()

print(data)

print('building nodes...')
nodes = []
for element in data['elements']:
    tags = element['tags']
    for nid, geom in zip(element['nodes'], element['geometry']):
        nodes.append({'id': nid, 'lat': geom['lat'], 'lon': geom['lon']}) #, 'tags': tags})

nodeFrame = pd.DataFrame(nodes)
print(nodeFrame.shape)
nodeFrame.drop_duplicates('id', inplace=True)
nodeFrame.set_index('id', inplace=True)
print(nodeFrame.shape)
#print(nodeFrame)

print('building edges')

edges = []
for element in data['elements']:
    tags = element['tags']
    for first, second in zip(element['nodes'][:-1], element['nodes'][1:]):
        edges.append({'node1': first, 'node2': second})

edgeFrame = pd.DataFrame(edges)
edgeFrame = edgeFrame.join(nodeFrame, on='node1', rsuffix='_from')
edgeFrame = edgeFrame.join(nodeFrame, on='node2', rsuffix='_to')
edgeFrame['distance'] = edgeFrame.apply(lambda row: meters(row['lat'], row['lon'], row['lat_to'], row['lon_to']), axis=1)

print(edgeFrame[['node1', 'node2']])
