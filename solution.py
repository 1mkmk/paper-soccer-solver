import csv
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os

# Tworzenie grafu
G = nx.Graph()

# Dodawanie wierzchołków
sizeX = 5
sizeY = 5

for x in range(0, sizeX):
    for y in range(0, sizeY):
        G.add_node((x, y))

# Dodawanie krawędzi
for x in range(0, sizeX - 1):
    for y in range(0, sizeY - 1):
        if y > 0:
            G.add_edge((x, y), (x + 1, y))  # krawędź pozioma
        if x > 0:
            G.add_edge((x, y), (x, y + 1))  # krawędź pionowa
        G.add_edge((x, y), (x + 1, y + 1))  # krawędź przekątna (góra-prawo)
        G.add_edge((x + 1, y), (x, y + 1))  # krawędź przekątna (dół-prawo)

# Znajdowanie najkrótszej ścieżki między wierzchołkiem (0, 0) a wierzchołkiem (10, 8)
start = (0, 0)
end = (10, 8)

# Tworzenie wykresu
fig, ax = plt.subplots()

# Rysowanie wykresu z wierzchołkami
pos = {node: node for node in G.nodes()}
nx.draw(G, pos=pos, with_labels=True)  # Set with_labels to True to display node labels

# Zmienna przechowująca ścieżkę
path = []


# Funkcja rysująca graf z podaną ścieżką
def draw_graph_with_path(path,path_color,i ):
    plt.pause(0.05)
    # Clear the previous plot
    ax.clear()
    nx.draw(G, pos=pos, with_labels=True)
    # Draw the path
    if path:
        for p in range(0, len(path)):
            edges = [(path[p][i], path[p][i + 1]) for i in range(len(path[p]) - 1)]
            print(path_color[p])
            # segment = p[0]
            # color = p[1]
            # print(p)
            # print(path[p])
            nx.draw_networkx_edges(G, pos=pos, edgelist=edges, edge_color=path_color[p], width=4.0)

        # if (j // 2) % 2 == 0:
        #     color = 'red'  # Kolor dla parzystej rundy
        # else:
        #     color = 'green'  # Kolor dla nieparzystej rundy

    plt.savefig(f'{output_dir}/image_{i}.png')
    plt.close(fig)


# Funkcja czytająca ścieżkę z pliku CSV
def read_path_from_csv(file_path, endingIterator=0):
    path = []
    iterator = 0
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if iterator < endingIterator:
                indices = [int(index) for index in row]
                nodes = [(index // sizeY, index % sizeY) for index in indices]  # Exclude indices equal to 0
                path.append(nodes)
                iterator += 1
            else:
                break
    return path


# Specify the path CSV file path
trasa = 'path_data.csv'

# Read the path from CSV
path = read_path_from_csv(trasa, 100)

# Create a directory to store the images
output_dir = 'path_images'
os.makedirs(output_dir, exist_ok=True)

# Save each plot as an image
new_path = []
path_color = []
for i, p in enumerate(path):
    if i % 2 == 0:
        color = 'red'  # Kolor dla parzystej rundy
    else:
        color = 'green'  # Kolor dla nieparzystej rundy
    new_path.append(p)
    path_color.append(color)
    draw_graph_with_path(new_path,path_color, i)

# Create an animation from the saved images
import glob
from PIL import Image

images = sorted(glob.glob(f'{output_dir}/*.png'))
frames = [Image.open(image) for image in images]
frames[0].save('animation.gif', format='GIF', append_images=frames[1:], save_all=True, duration=500, loop=0)
#
# # Remove the temporary image files
# for image in images:
#     os.remove(image)
