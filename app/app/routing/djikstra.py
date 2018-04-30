import pandas as pd
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from app.app.routing.queue import PriorityDict
from app.app.routing.graph import Graph
from app.app.routing.route import Route


def shortest_path(graph, start, end):
    """ Shortest Path by David Eppstein, UC Irvine, 8 Mar 2002 """
    distances, predecessors = dijkstra(graph.graph, start, end)
    path = []
    g = graph.graph
    while True:
        path.append(g[end])
        if end == start:
            break
        end = predecessors[end]
    path.reverse()
    return Route(path)

def dijkstra(graph, start, end=None):
    """ Dijkstra by David Eppstein, UC Irvine, 8 Mar 2002 """
    distances, predecessors = {}, {}
    priority_dict = PriorityDict()
    priority_dict[start] = 0

    for v in priority_dict:
        distances[v] = priority_dict[v]
        if v == end:
            break

        for w in graph[v].neighbors:
            distance = distances[v] + graph[v].neighbors[w]
            if w in distances:
                if distance < distances[w]:
                    raise ValueError("Dijkstra: found better path to already-final vertex")
            elif w not in priority_dict or distance < priority_dict[w]:
                priority_dict[w] = distance
                predecessors[w] = v

    return distances, predecessors


if __name__ == '__main__':
    node_data = [['1', 52.3, 13.4], ['2', 52.4, 13.4], ['3', 52.4, 13.3], ['4', 52.3, 13.3]]
    edge_data = [['1', '2', 30], ['2', '3', 20], ['3', '4', 20], ['4', '1', 25]]
    nodes_df = pd.DataFrame(node_data, columns=['id', 'lat', 'lon'])
    nodes_df.set_index('id', inplace=True)
    edges_df = pd.DataFrame(edge_data, columns=['node1', 'node2', 'distance'])
    g = Graph(nodes_df, edges_df)

    shortest = shortest_path(g, '1', '3')
    print(shortest)
