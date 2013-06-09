from priority_dict import priority_dict


class Node(str):
    def __init__(self, name):
        self.name = str(name)
        self.neighbors = set()

    def __repr__(self):
        return self.name

    def __str__(self):
        return "Node(" + self.name + ", " + "".join(self.neighbors) + ")"


def djikstra(graph, start, end=None):
    """ Djikstra's algorithm for finding shortest paths.

    Finds shortest paths from a start node in a graph of Node objects with
    graph edges represented as an adjacency list in Node.neighbors. If end is
    not None, the algorithm stops when a path to the end node is found.
    Otherwise, it continues until a path to all nodes is found.

    graph: dict of dicts -- graph[v][k] is weight of edge from nodes v to k
    start: start node
    end: end node -- if None, paths will be calculated to all reachable nodes
    """
    predecessors = {}
    distances = {}

    queue = priority_dict()
    queue[start] = 0

    for (dist, node) in queue.sorted_iter():
        distances[node] = dist
        if node == end:
            break
        for neigh in graph[node]:
            new_dist = dist + graph[node][neigh]
            if (neigh not in distances
               and (neigh not in queue or new_dist < queue[neigh])):
                queue[neigh] = new_dist
                predecessors[neigh] = node

    return (distances, predecessors)


def djikstra_path(graph, start, end):
    (distances, predecessors) = djikstra(graph, start, end)
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
    edgelist = [[1, 2],
                [0, 4],
                [0, 3],
                [2, 4],
                [1, 3]]
    graph = {}
    # graph[v][k] is weight of edge from nodes v to k
    for n, edges in zip(nodes, edgelist):
        graph[n] = dict.fromkeys((nodes[e] for e in edges), 1.0)
    for n in graph:
        print n, graph[n]

    start = nodes[0]
    end = nodes[4]
    (distances, predecessors) = djikstra(graph, start, end)
    print distances[end]

    print djikstra_path(graph, start, end)

if __name__ == "__main__":
    ret = main()
