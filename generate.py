import json
from random import Random

import names

rand = Random()

# scale locations from 1 tot 10
locations = {
    "Eindhoven": 5,
    "Amsterdam": 2,
    "Helmond": 1
}


class Graph:
    nodes = []
    edges = []

    def __init__(self):
        self.generate_nodes(500)
        self.generate_edges(2000)

    """
    Adds a new  node to the graph
    """

    def generate_node(self, n):
        self.nodes.append(Node(n))

    """
        Generate  N nodes
    """

    def generate_nodes(self, n):
        for x in range(0, n):
            self.generate_node(x)

    def generate_edge(self, is_bidirectional=0.25):
        node1 = rand.choice(self.nodes)
        node2 = rand.choice(self.nodes)

        if node1.pk == node2.pk:
            return

        if node1.pk in [x.node_to.edges for x in node2.edges]:
            return

        bidirectional = False

        if rand.randint(0, 100) >= is_bidirectional * 100:
            bidirectional = True

        # Create edge
        edge = Edge(node1, node2)

        node2.add_edge(edge)

        if bidirectional:
            node1.add_edge(Edge(node2, node1))

        self.edges.append(edge)

    def generate_edges(self, n):
        for x in range(0, n):
            self.generate_edge()

    def describe(self):
        print("This graph contains {0} nodes and {1} edges".format(len(self.nodes), len(self.edges)))

        print("Fetching random sample")

        loc_dist = {}
        total = 0
        min_edges = 1000000
        max_edges = 0

        for node in self.nodes:
            # Calculate distribution of locations
            if node.location in loc_dist.keys():
                loc_dist[node.location] += 1
            else:
                loc_dist[node.location] = 1

            total += len(node.edges)

            if len(node.edges) > max_edges:
                max_edges = len(node.edges)
            elif len(node.edges) < min_edges:
                min_edges = len(node.edges)

        print("Average node has {0} edges".format(total / len(self.nodes)))
        print("Min edges is {0} \tMax edges is {1}".format(min_edges, max_edges))

        print(self.nodes[0].json())

        for k in loc_dist.keys():
            print("{0} - {1}".format(loc_dist[k], k))

    def save(self, path="data.json"):
        f = open(path, "w")
        f.write(json.dumps([x.json() for x in self.nodes]))
        f.close()


class Node:
    def __init__(self, pk):
        self.name = names.get_full_name()
        self.location = rand.choice(rand.choices(list(locations.keys()), weights=locations.values()))
        self.edges = []
        self.pk = pk

    def add_edge(self, edge):
        self.edges.append(edge)

    def __str__(self):
        return "{0}".format(self.name, self.location)

    def json(self):
        return {
            "pk": self.pk,
            "name": self.name,
            "location": self.location,
            "edges": [x.node_to.pk for x in self.edges]
        }


class Edge:
    node_to = None
    node_from = None

    def __init__(self, node_to, node_from):
        self.node_to = node_to
        self.node_from = node_from

    def __str__(self):
        return "Edge from {0} to {1}".format(self.node_from.pk, self.node_to.pk)

    def json(self):
        return {
            "node1": self.node_to.pk,
            "node2": self.node_from.pk
        }


if __name__ == "__main__":
    graph = Graph()

    graph.describe()
    graph.save()
