import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import csv

import pandas as pandas
import pandas as pd

# stwórz graf
G = nx.Graph()


sizeX = 5
sizeY = 5



# dodaj wierzchołki
for x in range(0, sizeX):
    for y in range(0, sizeY):
        G.add_node((x, y))

# dodaj krawędzie
for x in range(0, sizeX-1):
    for y in range(0, sizeY-1):

        if y>0:
            G.add_edge((x, y), (x+1, y))  # krawędź pozioma
        if x>0:
            G.add_edge((x, y), (x, y+1))  # krawędź pionowa
        G.add_edge((x, y), (x+1, y+1))  # krawędź przekątna (góra-prawo)
        G.add_edge((x+1, y), (x, y+1))  # krawędź przekątna (dół-prawo)

num_edges = G.number_of_edges()
print("Liczba krawędzi:", num_edges)
# znajdź najkrótszą ścieżkę między wierzchołkiem (0, 0) a wierzchołkiem (10, 8)
start = (0, 0)
end = (10, 8)

# path_data = []
# with open('path_data.csv', 'r') as file:
#     reader = csv.reader(file)
#     for row in reader:
#         path_data.append((int(row[0]), int(row[1])))
#
# path = [data[1] for data in path_data]





# path = nx.shortest_path(G, source=start, target=end)
# print(path)
# #
# G.remove_edges_from(G.edges())
#
# # add edges in the path to the graph
# for i in range(len(path)-1):
#     G.add_edge(path[i], path[i+1])
#
A = nx.to_numpy_array(G)
A = A.astype(int)
pos = {}
for x in range(0, sizeX):
    for y in range(0, sizeY):
        pos[(x, y)] = (x, y)



def save_graph_as_adjacency_csv(graph, file_path):
    num_nodes = len(graph.nodes)
    adjacency_matrix = np.zeros((num_nodes, num_nodes))

    for node in graph.nodes:
        neighbors = list(graph.neighbors(node))
        node_index = node[0] * sizeY + node[1]
        print(node_index)
        for neighbor in neighbors:
            neighbor_index = neighbor[0] * sizeY + neighbor[1]
            if node_index != neighbor_index:  # Skip creating edge if neighbor is the same as current node
                adjacency_matrix[node_index][neighbor_index] = 1
                adjacency_matrix[neighbor_index][node_index] = 1

    # Create a DataFrame from the adjacency matrix
    df = pd.DataFrame(adjacency_matrix, index=range(num_nodes), columns=range(num_nodes))

    # Save the DataFrame as a CSV file
    df.to_csv(file_path, index=False, header=None)

save_graph_as_adjacency_csv(G, "graph_adjacency.csv")

# save adjacency matrix to CSV file
# with open('adjacency_matrix.csv', mode='w', newline='') as file:
#     writer = csv.writer(file)
#     for row in A:
#         writer.writerow(row)
save_graph_as_adjacency_csv(G, 'adjacency_matrix.csv')

nx.draw(G, pos=pos, with_labels=True)

# dodaj ścieżkę
# path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
# print(path_edges)
# nx.draw_networkx_edges(G, pos=pos, edgelist=path_edges, edge_color='r', width=2.0)

# pokaż wykres
plt.show()

# show plot
# plt.show()
