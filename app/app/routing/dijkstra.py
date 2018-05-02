import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from app.app.routing.queue import PriorityDict
from app.app.routing.graph import Graph
from app.app.routing.route import Route


def shortest_path(graph, start, end):
    """ Shortest Path by David Eppstein, UC Irvine, 8 Mar 2002 """
    distances, predecessors = dijkstra(graph, start, end)
    path = []
    while 1:
        path.append(end)
        if end == start:
            break
        end = predecessors[end]
    path.reverse()
    return Route(graph, path)


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
    g = Graph.load_default()
    shortest = shortest_path(g.graph, 27785378, 2493824077)
    print(shortest)
