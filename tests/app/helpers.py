import pandas as pd
from app.app.routing.graph import Graph


def get_test_graph():
    node_dict = {
        'id': ['N1', 'N2', 'N3', 'N4'],
        'lat': [52.3, 52.4, 52.4, 52.3],
        'lon': [13.4, 13.4, 13.3, 13.3]
    }
    edge_dict = {
        'node1': ['N1', 'N2', 'N3', 'N4'],
        'node2': ['N2', 'N3', 'N4', 'N1'],
        'distance': [30, 20, 20, 25]
    }
    nodes = pd.DataFrame.from_dict(node_dict)
    nodes.set_index('id', inplace=True)
    edges = pd.DataFrame(edge_dict)
    return Graph(nodes, edges)
