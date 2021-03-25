class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """
        if v not in self.adj_list:
            self.adj_list[v] = []

    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """
        # edge cannot be created if vertices are the same
        if u == v:
            return

        # adds the vertex arguments to graph if they do not exist
        if u not in self.adj_list:
            self.add_vertex(u)
        if v not in self.adj_list:
            self.add_vertex(v)

        # returns if edge already exists between the vertices
        if v in self.adj_list[u] or u in self.adj_list[v]:
            return

        # creates edge between the two vertices
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """
        # returns if either vertex does not exist in the graph
        if u not in self.adj_list or v not in self.adj_list:
            return

        # returns if vertices are equal or if edge already exists between them
        if u == v or v not in self.adj_list[u] or u not in self.adj_list[v]:
            return

        # removes edge between the two vertices
        self.adj_list[u].remove(v)
        self.adj_list[v].remove(u)

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        if v in self.adj_list:

            # gets list of vertices that are adjacent to v
            adj = []
            for vertex in self.adj_list[v]:
                adj.append(vertex)

            # removes all edges connected to v
            for vertex in adj:
                self.remove_edge(v, vertex)

            # deletes v
            del self.adj_list[v]

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        vert_list = []
        for vertex in self.adj_list:
            vert_list.append(vertex)
        return vert_list

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        # creates list of lists that each represent all edges in the graph
        edge_list = []
        vert_list = self.get_vertices()
        for vertex in vert_list:
            for item in self.adj_list[vertex]:
                edge_list.append([vertex, item])

        # removes duplicates from list (list contains edges from every vertex
        # so each edge is included twice), and converts inner lists to tuples
        test = list(set(tuple(sorted(item)) for item in edge_list))
        return test

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        # empty path is considered valid
        if not path:
            return True

        # path is invalid if any vertex in the path does not exist
        for vertex in path:
            if vertex not in self.adj_list:
                return False

        # creates list of tuples representing all edges (including duplicates)
        edge_list = []
        vert_list = self.get_vertices()
        for vertex in vert_list:
            for item in self.adj_list[vertex]:
                edge_list.append((vertex, item))

        # determines if path exists by checking if edge_list
        # contains each edge that makes up the argument path
        for i in range(len(path) - 1):
            if (path[i], path[i + 1]) not in edge_list:
                return False
        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS
        Vertices are prioritized by alphabetical order when multiple
        options are available for the next vertex in the search
        """
        if v_start not in self.adj_list:
            return []

        visited = []
        temp_list = []
        stack = [v_start]

        # dfs loop
        while stack:
            vertex = stack.pop()

            # appends vertex and returns visited list
            # if the specified end vertex is found
            if vertex == v_end:
                visited.append(vertex)
                return visited

            if vertex not in visited:
                visited.append(vertex)
                # appends adjacent vertices to temp_list
                for item in self.adj_list[vertex]:
                    temp_list.append(item)
                # sorts reversed in descending order
                temp_list.sort(reverse=True)
                # pushes vertices from temp_list to the stack so that they are alphabetically sorted
                for item in temp_list:
                    stack.append(item)

                temp_list = []

        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS
        Vertices are picked in alphabetical order
        """

        if v_start not in self.adj_list:
            return []

        visited = []
        temp_list = []
        queue = [v_start]

        # bfs loop
        while queue:
            vertex = queue.pop()

            if vertex == v_end:
                visited.append(vertex)
                return visited
            if vertex not in visited:
                visited.append(vertex)
            # appends adjacent vertices to temp_list
            for item in self.adj_list[vertex]:
                if item not in visited:
                    temp_list.append(item)
            # sorts temp list
            temp_list.sort()
            # inserts temp_list vertices into the queue
            for item in temp_list:
                queue.insert(0, item)

            temp_list = []

        return visited

    def count_connected_components(self):
        """
        Return number of connected components in the graph
        """
        vert_list = self.get_vertices()
        a_list = []
        for vertex in vert_list:
            a_list.append(self.bfs(vertex))

        test = list(set(tuple(sorted(item)) for item in a_list))
        return len(test)

    def has_cycle(self):
        """
        Returns True if at least one cycle
        exists in the graph, False otherwise
        """
        visited = set()
        # performs dfs search
        for vert in self.get_vertices():
            if vert not in visited:
                result = self.rec_has_cycle(vert, None, visited)
                if result:
                    return True
        return False

    def rec_has_cycle(self, v_start, parent, visited):
        """
        Helper method for has_cycle
        """
        visited.add(v_start)
        for vert in self.adj_list[v_start]:
            # parent tracking allows for cycle detection
            if vert == parent:
                continue
            if vert in visited:
                return True
            if self.rec_has_cycle(vert, v_start, visited):
                return True
        return False


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)

    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)

    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')

    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))

    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')

    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()

    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())

    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """


    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()
        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)


    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'


    # ------------------------------------------------------------------ #
