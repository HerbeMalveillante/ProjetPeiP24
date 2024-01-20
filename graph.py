# show the graph using networkx
import networkx as nx
import matplotlib.pyplot as plt
from rich import print


# On va utiliser une liste pour représenter les connexions, puis nous allons le convertir en matrice d'adjacence et utiliser networkx pour le dessiner
# Les nodes de la grille sont identifiés par un identifiant unique.

matrixSize = 4

connexions = []
for i in range(matrixSize * matrixSize):
    if i >= matrixSize * matrixSize - 1:
        continue
    localIterator = i % matrixSize
    if (i + 1) % matrixSize > localIterator:
        connexions.append((i, i + 1))

    # vertical
    if i + matrixSize < matrixSize * matrixSize:
        connexions.append((i, i + matrixSize))

print(connexions)

gridGraph = []


def drawFromAdjacencyMatrix(matrix):
    G = nx.Graph()
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 1:
                G.add_edge(i, j)

    nx.draw(G, with_labels=True)
    plt.show()


def adjacencyMatrixFromConnections(connections):
    matrix = [
        [0 for i in range(matrixSize * matrixSize)]
        for j in range(matrixSize * matrixSize)
    ]
    for connection in connections:
        matrix[connection[0]][connection[1]] = 1
        matrix[connection[1]][connection[0]] = 1
    return matrix


drawFromAdjacencyMatrix(adjacencyMatrixFromConnections(connexions))
