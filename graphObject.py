import random
from rich import print
import uuid


class Node(object):
    def __init__(self):
        self.id = uuid.uuid4()

    def __str__(self):
        return str(self.id)


nodes = [Node() for i in range(16)]
connections = []


for i, node in enumerate(nodes):
    if i >= len(nodes) - 1:
        print("dernier")
        continue
    localIterator = i % 4
    if (i + 1) % 4 > localIterator:
        connections.append((node, nodes[i + 1]))

    # vertical
    if i + 4 < len(nodes):
        connections.append((node, nodes[i + 4]))


print(connections)
print(len(connections))
