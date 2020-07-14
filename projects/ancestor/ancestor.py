class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise IndexError('nonexistant vert')

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        q = Queue()
        visited = set()

        q.enqueue(starting_vertex)

        while q.size() > 0:
            vert = q.dequeue()
            if vert not in visited:
                visited.add(vert)
                print(vert)
                for neighbor in self.get_neighbors(vert):
                    q.enqueue(neighbor)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        s = Stack()
        visited = set()

        s.push(starting_vertex)  # 1

        while s.size() > 0:
            vert = s.pop()

            if vert not in visited:
                visited.add(vert)
                print(vert)
                for neighbor in self.get_neighbors(vert):
                    s.push(neighbor)

    def dft_recursive(self, starting_vertex, visited=set()):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        visited = visited

        if starting_vertex not in visited:
            visited.add(starting_vertex)
            print(starting_vertex)
            for neighbor in self.get_neighbors(starting_vertex):
                self.dft_recursive(neighbor, visited)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        # Create an empty queue and enqueue A PATH TO the starting vertex ID
        q = Queue()
        q.enqueue([starting_vertex])
        # Create a Set to store visited vertices
        visited = set()
        # While the queue is not empty...
        while q.size() > 0:
            # Dequeue the first PATH
            path = q.dequeue()
            # Grab the last vertex from the PATH
            lastVert = path[-1]
            # If that vertex has not been visited...
            if lastVert not in visited:
                # CHECK IF IT'S THE TARGET
                if lastVert is destination_vertex:
                    # IF SO, RETURN PATH
                    return path
                    # Mark it as visited...
                visited.add(lastVert)
                # Then add A PATH TO its neighbors to the back of the queue
                for neighbor in self.get_neighbors(lastVert):
                    # COPY THE PATH
                    tempPath = list(path)
                    # APPEND THE NEIGHOR TO THE BACK
                    tempPath.append(neighbor)
                    q.enqueue(tempPath)

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        # Create an empty queue and enqueue A PATH TO the starting vertex ID
        s = Stack()
        s.push([starting_vertex])
        # Create a Set to store visited vertices
        visited = set()
        # While the queue is not empty...
        while s.size() > 0:
            # Dequeue the first PATH
            path = s.pop()
            # Grab the last vertex from the PATH
            lastVert = path[-1]
            # If that vertex has not been visited...
            if lastVert not in visited:
                # CHECK IF IT'S THE TARGET
                if lastVert is destination_vertex:
                    # IF SO, RETURN PATH
                    return path
                # Mark it as visited...
                visited.add(lastVert)
                # Then add A PATH TO its neighbors to the back of the queue
                for neighbor in self.get_neighbors(lastVert):
                    # COPY THE PATH
                    tempPath = list(path)
                    # APPEND THE NEIGHOR TO THE BACK
                    tempPath.append(neighbor)
                    s.push(tempPath)

    def dfs_recursive(self, starting_vertex, destination_vertex, path=[], visited=set()):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        visited = visited
        path = path
        path.append(starting_vertex)

        if starting_vertex not in visited:
            # CHECK IF IT'S THE TARGET
            if starting_vertex == destination_vertex:
                # IF SO, RETURN PATH
                return path
            visited.add(starting_vertex)

            for neighbor in self.get_neighbors(starting_vertex):
                # COPY THE PATH
                tempPath = list(path)
                # APPEND THE NEIGHOR TO THE BACK
                tempPath.append(neighbor)
            starting_vertex = tempPath[-1]
            return self.dfs_recursive(starting_vertex, destination_vertex, path, visited)


def earliest_ancestor(ancestors, starting_node):
    parentsToVisit = Stack()
    # store a path

    parentsToVisit.push(starting_node)
    # store visited
    visited = set()

    parents = []
    while parentsToVisit.size() > 0:
        cur = parentsToVisit.pop()
        if cur not in visited:
            visited.add(cur)
            # get cur's parents
            for g in get_parents(cur, ancestors):
                if g != -1:
                    # print('parents: ', g)
                    # make a list of parents
                    parents.append(g)
                    parentsToVisit.push(g)

    if len(parents) > 0:
        return min(parents)
    else:
        return -1


def get_parents(child, ancestors):
    # go through ancestor data list
    parents = set()
    for ancestor in ancestors:
        par = ancestor[0]
        ch = ancestor[1]
        if ch == child:
            # add the parent from that pair as one of 'child's' parents
            parents.add(par)
    # if no parents found
    if len(parents) == 0:
        parents.add(-1)
    return parents

    # look for any tuple that has child as 2nd spot,
    # if found,
    # 1st spot will be it's parent
    # else:
    # not found,
    # return current child


if __name__ == "__main__":
    test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7),
                      (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]

    # print(earliest_ancestor(test_ancestors, 1))  # 10
    print('')
    # print(earliest_ancestor(test_ancestors, 2))  # -1
    # print('')
    print(earliest_ancestor(test_ancestors, 3))  # 10
    # print('')
    # print(earliest_ancestor(test_ancestors, 4))  # -1
    # print('')
    # print(earliest_ancestor(test_ancestors, 5))  # 4
    # print('')
    # print(earliest_ancestor(test_ancestors, 6))  # 10
    # print('')
    # print(earliest_ancestor(test_ancestors, 7))  # 4
    # print('')
    # print(earliest_ancestor(test_ancestors, 8))  # 4
    # print('')
    # print(earliest_ancestor(test_ancestors, 9))  # 4
    # print('')
    # print(earliest_ancestor(test_ancestors, 10))  # -1
    # print('')
    # print(earliest_ancestor(test_ancestors, 11))  # -1
    print('')
