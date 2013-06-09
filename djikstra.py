from priority_dict import priority_dict
import sys

INF = sys.maxint


class Node(str):
    def __init__(self, name):
        self.name = str(name)
        self.neighbors = set()

    def __repr__(self):
        return self.name

    def __str__(self):
        return "Node(" + self.name + ", " + "".join(self.neighbors) + ")"

nodes = [Node(chr(ord('A') + x)) for x in range(5)]
edges = [[1, 2],
         [0, 4],
         [0, 3],
         [2, 4],
         [1, 3]]
for n, e in zip(nodes, edges):
    n.neighbors.update(nodes[x] for x in e)

#print "\n".join(str(n) for n in nodes)

start = nodes[0]
end = nodes[4]


def djikstra(nodes, start, end):
    predecessors = dict.fromkeys(nodes, None)
    distances = dict.fromkeys(nodes, INF)
    distances[start] = 0

    queue = priority_dict()
    queue[start] = 0

    for (dist, node) in queue.sorted_iter():
        distances[node] = dist
        if node == end:
            break
        for neigh in node.neighbors:
            new_dist = dist + 1
            if neigh not in queue or new_dist < queue[neigh]:
                queue[neigh] = new_dist
                predecessors[neigh] = node

    return (distances, predecessors)

#def djikstra_path(nodes, start, end):

(distances, predecessors) = djikstra(nodes, start, end)
print distances[end]
n = end
while n != start:
    print n
    n = predecessors[n]
print n


