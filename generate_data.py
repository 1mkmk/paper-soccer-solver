import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class GraphGenerator:
    def __init__(self, sizeX, sizeY):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.G = nx.Graph()

    def generate_graph(self):
        for x in range(0, self.sizeX):
            for y in range(0, self.sizeY):
                self.G.add_node((x, y))

        for x in range(0, self.sizeX - 1):
            for y in range(0, self.sizeY - 1):
                if y > 0:
                    self.G.add_edge((x, y), (x + 1, y))  # horizontal edge
                if x > 0:
                    self.G.add_edge((x, y), (x, y + 1))  # vertical edge
                self.G.add_edge((x, y), (x + 1, y + 1))  # diagonal edge (top-right)
                self.G.add_edge((x + 1, y), (x, y + 1))  # diagonal edge (bottom-right)

    def get_num_edges(self):
        return self.G.number_of_edges()

    def get_graph(self):
        return self.G


class GraphVisualizer:
    def __init__(self, graph, sizeX, sizeY):
        self.graph = graph
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.pos = {}
        for x in range(0, self.sizeX):
            for y in range(0, self.sizeY):
                self.pos[(x, y)] = (x, y)

    def draw_graph(self):
        nx.draw(self.graph, pos=self.pos, with_labels=True)
        plt.show()


class GraphDataExporter:
    @staticmethod
    def save_adjacency_matrix(graph, file_path, sizeY):
        num_nodes = len(graph.nodes)
        adjacency_matrix = np.zeros((num_nodes, num_nodes))

        for node in graph.nodes:
            neighbors = list(graph.neighbors(node))
            node_index = node[0] * sizeY + node[1]

            for neighbor in neighbors:
                neighbor_index = neighbor[0] * sizeY + neighbor[1]
                if node_index != neighbor_index:
                    adjacency_matrix[node_index][neighbor_index] = 1
                    adjacency_matrix[neighbor_index][node_index] = 1

        df = pd.DataFrame(adjacency_matrix, index=range(num_nodes), columns=range(num_nodes))
        df.to_csv(file_path, index=False, header=None)


# Usage example
sizeX = 5
sizeY = 5

graph_generator = GraphGenerator(sizeX, sizeY)
graph_generator.generate_graph()

num_edges = graph_generator.get_num_edges()
print("Number of edges:", num_edges)

graph = graph_generator.get_graph()

data_exporter = GraphDataExporter()
data_exporter.save_adjacency_matrix(graph, "graph_adjacency.csv", sizeY)

visualizer = GraphVisualizer(graph, sizeX, sizeY)
visualizer.draw_graph()
