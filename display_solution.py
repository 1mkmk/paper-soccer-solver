import csv
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os
from PIL import Image
import glob


class GraphVisualizer:
    def __init__(self, sizeX, sizeY):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.G = nx.Graph()
        self.fig, self.ax = plt.subplots()
        self.pos = {}

    def create_graph(self):
        for x in range(0, self.sizeX):
            for y in range(0, self.sizeY):
                self.G.add_node((x, y))

        for x in range(0, self.sizeX - 1):
            for y in range(0, self.sizeY - 1):
                if y > 0:
                    self.G.add_edge((x, y), (x + 1, y))
                if x > 0:
                    self.G.add_edge((x, y), (x, y + 1))
                self.G.add_edge((x, y), (x + 1, y + 1))
                self.G.add_edge((x + 1, y), (x, y + 1))

        self.pos = {node: node for node in self.G.nodes()}

    def draw_graph(self):
        plt.pause(0.05)
        self.ax.clear()
        nx.draw(self.G, pos=self.pos, with_labels=True)

    def draw_path(self, path, path_color):
        for p in range(0, len(path)):
            edges = [(path[p][i], path[p][i + 1]) for i in range(len(path[p]) - 1)]
            nx.draw_networkx_edges(self.G, pos=self.pos, edgelist=edges, edge_color=path_color[p], width=4.0)

    def save_graph_image(self, output_dir, image_filename):
        plt.savefig(os.path.join(output_dir, image_filename))
        plt.close(self.fig)


class PathReader:
    def __init__(self, sizeX, sizeY):
        self.sizeX = sizeX
        self.sizeY = sizeY

    def read_path_from_csv(self, file_path, endingIterator=0):
        path = []
        iterator = 0
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if iterator < endingIterator:
                    indices = [int(index) for index in row]
                    nodes = [(index // self.sizeY, index % self.sizeY) for index in indices]
                    path.append(nodes)
                    iterator += 1
                else:
                    break
        return path


class GraphAnimator:
    def __init__(self, graph_visualizer, path_reader):
        self.graph_visualizer = graph_visualizer
        self.path_reader = path_reader

    def animate_graph(self, trasa, output_dir):
        path = self.path_reader.read_path_from_csv(trasa, 100)

        os.makedirs(output_dir, exist_ok=True)

        new_path = []
        path_color = []
        for i, p in enumerate(path):
            if i % 2 == 0:
                color = 'red'
            else:
                color = 'green'
            new_path.append(p)
            path_color.append(color)

            self.graph_visualizer.draw_graph()
            self.graph_visualizer.draw_path(new_path, path_color)
            image_filename = f'image_{i}.png'
            self.graph_visualizer.save_graph_image(output_dir, image_filename)

        images = sorted(glob.glob(f'{output_dir}/*.png'))
        frames = [Image.open(image) for image in images]
        frames[0].save('animation.gif', format='GIF', append_images=frames[1:], save_all=True, duration=500, loop=0)

        for image in images:
            os.remove(image)


# Usage
sizeX = 5
sizeY = 5

graph_visualizer = GraphVisualizer(sizeX, sizeY)
graph_visualizer.create_graph()

path_reader = PathReader(sizeX, sizeY)

graph_animator = GraphAnimator(graph_visualizer, path_reader)
graph_animator.animate_graph('path_data.csv', 'data/path_images')
