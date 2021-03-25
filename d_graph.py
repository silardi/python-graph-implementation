class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Adds vertex to the graph and returns the number
        of vertices in the graph after the addition
        """
        # increments vertex count and adds new row to matrix which represents the vertex
        self.v_count += 1
        self.adj_matrix.append(self.v_count * [0])

        # increases the length of each matrix row
        for i in range(self.v_count - 1):
            self.adj_matrix[i].append(0)

        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Adds edge to the graph
        """
        # returns if any of the following error conditions are triggered
        if src >= self.v_count or dst >= self.v_count or weight <= 0 or src == dst:
            return

        # adds edge
        self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        Removes edge from graph
        """
        # removes edge if both vertices exist and the provided indices are >= 0
        if 0 <= src < self.v_count and 0 <= dst < self.v_count:
            self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        Returns a list of the graph's vertices
        """
        vert_list = []
        for i in range(self.v_count):
            vert_list.append(i)

        return vert_list

    def get_edges(self) -> []:
        """
        Returns a list of the graph's edges
        """
        edge_list = []
        matrix = self.adj_matrix

        # traverses matrix and adds each edge to edge_list
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] > 0:
                    edge_list.append((i, j, matrix[i][j]))

        return edge_list

    def is_valid_path(self, path: []) -> bool:
        """
        Returns True if specified path is valid and False if not
        """
        # empty path is considered valid
        if not path:
            return True

        # path is invalid if any vertex in the path does not exist
        for i in range(len(path) - 1):
            if self.adj_matrix[path[i]][path[i + 1]] == 0:
                return False

        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS
        Vertex indices are prioritized by ascending order when multiple
        options are available for the next vertex in the search (e.g., 0 before 1)
        """
        if v_start < 0 or v_start >= self.v_count:
            return []

        # initializes lists used in dfs
        visited = self.v_count * [False]
        temp_list = []
        stack = [v_start]

        # dfs loop
        while stack:
            vertex = stack.pop()

            # appends vertex to visited if it has not been visited
            # updates visited value to True
            if not visited[vertex]:
                temp_list.append(vertex)
                visited[vertex] = True

            # returns visited list if the specified end vertex is found
            if vertex == v_end:
                return temp_list

            # iteration is reversed so that vertices are ordered properly in stack
            # pushes adjacent vertices onto stack in correct order
            for i in reversed(range(self.v_count)):
                if self.adj_matrix[vertex][i] > 0 and (not visited[i]):
                    stack.append(i)

        return temp_list

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS
        Vertex indices are prioritized by ascending order when multiple
        options are available for the next vertex in the search (e.g., 0 before 1)
        """

        if v_start < 0 or v_start >= self.v_count:
            return []

        # initializes lists used in bfs
        visited = self.v_count * [False]
        vert_list = []
        queue = [v_start]

        # bfs loop
        while queue:
            vertex = queue.pop()

            # appends vertex to list if it has not been visited
            # updates visited value to True
            if not visited[vertex]:
                vert_list.append(vertex)
                visited[vertex] = True

            # returns list if the specified end vertex is found
            if vertex == v_end:
                return vert_list

            # enqueues adjacent vertices to queue
            for i in range(self.v_count):
                if self.adj_matrix[vertex][i] > 0 and (not visited[i]):
                    queue.insert(0, i)

        return vert_list

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """
        visited = [False] * self.v_count
        stack = [False] * self.v_count
        # makes call to recursive helper method if index has not been visited
        for index in range(self.v_count):
            if not visited[index]:
                if self.rec_check_cycle(index, visited, stack):
                    return True
        return False

    def rec_check_cycle(self, cur, visited, stack):
        """
        Helper method for has_cycle
        """
        # updates visited and stack lists since cur has now been visited
        visited[cur] = True
        stack[cur] = True

        # makes recursive call to determine if vertex is in stack (True signifying cycle) if
        # edge does not exist between cur and index and if the index has not been visited
        for i in range(self.v_count):
            if self.adj_matrix[cur][i] != 0:
                if not visited[i]:
                    if self.rec_check_cycle(i, visited, stack):
                        return True
                elif stack[i]:
                    return True

        # update cur index in stack if cur does not result in cycle
        stack[cur] = False
        return False

    def dijkstra(self, src: int) -> []:
        """
        Implements Dijkstra algorithm to compute the
        length of the shortest path from the given index
        to all other vertices in the graph
        """
        distance = self.v_count * [float('inf')]
        distance[src] = 0
        visited = self.v_count * [False]

        # finds index of visited vertex with smallest distance
        # and changes its value in the visited list to True
        for i in range(self.v_count):
            min_i = self.get_min_index(distance, visited)
            visited[min_i] = True

            # changes distance of adjacent vertices if conditions are met
            for v in range(self.v_count):
                if self.adj_matrix[min_i][v] > 0 and not visited[v] and \
                        distance[v] > (distance[min_i] + self.adj_matrix[min_i][v]):
                    distance[v] = distance[min_i] + self.adj_matrix[min_i][v]

        return distance

    def get_min_index(self, distance, visited):
        """
        Finds index of visited vertex with smallest distance
        """
        # initializes min distance for next vertex
        min_dist = float('inf')
        min_index = 0

        # finds index
        for v in range(self.v_count):
            if distance[v] < min_dist and not visited[v]:
                min_dist = distance[v]
                min_index = v

        return min_index


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)

    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')

    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))

    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')

    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)

    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
