from priority_dict import priority_dict


class Node(str):
    def __init__(self, name):
        self.name = str(name)
        self.neighbors = set()

    def __repr__(self):
        return self.name

    def __str__(self):
        return "Node(" + self.name + ", " + "".join(self.neighbors) + ")"


def djikstra(nodes, start, end=None):
    """ Djikstra's algorithm for finding shortest paths.

    Finds shortest paths from a start node in a graph of Node objects with
    graph edges represented as an adjacency list in Node.neighbors. If end is
    not None, the algorithm stops when a path to the end node is found.
    Otherwise, it continues until a path to all nodes is found."""
    predecessors = dict()
    distances = dict()

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


def djikstra_path(nodes, start, end):
    (distances, predecessors) = djikstra(nodes, start, end)
    if end not in distances:
        return None
    path = []
    n = end
    while n != start:
        path.append(n)
        n = predecessors[n]
    path.append(n)
    path.reverse()
    return path


def main():
    # build test data
    nodes = [Node(chr(ord('A') + x)) for x in range(5)]
    edges = [[1, 2],
            [0, 4],
            [0, 3],
            [2, 4],
            [1, 3]]
    for n, e in zip(nodes, edges):
        n.neighbors.update(nodes[x] for x in e)

    start = nodes[0]
    end = nodes[4]
    (distances, predecessors) = djikstra(nodes, start, end)

    print distances[end]
    print djikstra_path(nodes, start, end)

if __name__ == "__main__":
    ret = main()
