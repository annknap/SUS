import math

class BayesNet:
    def __init__(self, data_set, has_column_names = False):
        self.net = {}
        self.has_column_names = has_column_names

        column_names = data_set[0]


        if has_column_names is False:
            column_names = []
            column_name = 'A'

            for column in data_set[0]:
                column_names.append(column_name)
                column_name = chr(ord(column_name) + 1)

        self.vertexes = column_names

        for vertex in column_names:
            self.net[vertex] = {'possible_values': [],
                                'children': [],
                                'parents': [],
                                'probabilities': []}

    def add_edge(self, vertex, new_child):
        if vertex not in self.net:
            print('Vertex ' + vertex + ' does not exist. Can\'t create edge ' + vertex + ' -> ' + new_child)
        elif new_child not in self.net:
            print('Vertex ' + new_child + ' does not exist. Can\'t create edge ' + vertex + ' -> ' + new_child)
        elif vertex in self.net[new_child]['parents'] and new_child in self.net[vertex]['children']:
            print('Edge ' + vertex + ' -> ' + new_child + ' already exists')
        elif vertex not in self.net[new_child]['parents'] and new_child in self.net[vertex]['children']:
            print('Wrong net structure. Vertex ' + vertex + ' is not a parent of vertex ' + new_child +
                  ' but vertex ' + new_child + ' is a child of vertex ' + vertex)
        elif vertex in self.net[new_child]['parents'] and new_child not in self.net[vertex]['children']:
            print('Wrong net structure. Vertex ' + new_child + ' is not a child of vertex ' + vertex +
                  ' but vertex ' + vertex + ' is a parent of vertex ' + new_child)
        elif self.check_cycle(vertex, new_child) > 0:
            print('Adding edge ' + vertex + ' -> ' + new_child + ' will create a cycle')
        elif vertex not in self.net[new_child]['parents'] and new_child not in self.net[vertex]['children']:
            self.net[vertex]['children'].append(new_child)
            self.net[new_child]['parents'].append(vertex)
        else:
            print('Unknown error during adding edge ' + vertex + ' -> ' + new_child)

    def delete_edge(self, vertex, old_child):
        if vertex not in self.net:
            print('Vertex ' + vertex + ' does not exist. Can\'t delete edge ' + vertex + ' -> ' + old_child)
        elif old_child not in self.net:
            print('Vertex ' + old_child + ' does not exist. Can\'t delete edge ' + vertex + ' -> ' + old_child)
        elif vertex not in self.net[old_child]['parents'] and old_child not in self.net[vertex]['children']:
            print('Edge ' + vertex + ' -> ' + old_child + ' does not exist')
        elif vertex not in self.net[old_child]['parents'] and old_child in self.net[vertex]['children']:
            print('Wrong net structure. Vertex ' + vertex + ' is not a parent of vertex ' + old_child +
                  ' but vertex ' + old_child + ' is a child of vertex ' + vertex)
        elif vertex in self.net[old_child]['parents'] and old_child not in self.net[vertex]['children']:
            print('Wrong net structure. Vertex ' + old_child + ' is not a child of vertex ' + vertex +
                  ' but vertex ' + vertex + ' is a parent of vertex ' + old_child)
        elif vertex in self.net[old_child]['parents'] and old_child in self.net[vertex]['children']:
            self.net[vertex]['children'].remove(old_child)
            self.net[old_child]['parents'].remove(vertex)
        else:
            print('Unknown error during deleting edge ' + vertex + ' -> ' + old_child)

    def reverse_edge(self, parent, child):
        if parent not in self.net:
            print('Vertex ' + parent + ' does not exist. Can\'t reverse edge ' + parent + ' -> ' + child)
        elif child not in self.net:
            print('Vertex ' + child + ' does not exist. Can\'t reverse edge ' + parent + ' -> ' + child)
        elif parent not in self.net[child]['parents'] and child not in self.net[parent]['children']:
            print('Edge ' + parent + ' -> ' + child + ' does not exist')
        elif parent not in self.net[child]['parents'] and child in self.net[parent]['children']:
            print('Wrong net structure. Vertex ' + parent + ' is not a parent of vertex ' + child +
                  ' but vertex ' + child + ' is a child of vertex ' + parent)
        elif parent in self.net[child]['parents'] and child not in self.net[parent]['children']:
            print('Wrong net structure. Vertex ' + child + ' is not a child of vertex ' + parent +
                  ' but vertex ' + parent + ' is a parent of vertex ' + child)
        elif self.check_cycle(child, parent, True) > 0:
            print('Reversing edge ' + parent + ' -> ' + child + ' will create a cycle')
        elif parent in self.net[child]['parents'] and child in self.net[parent]['children']:
            self.net[parent]['children'].remove(child)
            self.net[parent]['parents'].append(child)
            self.net[child]['parents'].remove(parent)
            self.net[child]['children'].append(parent)
        else:
            print('Unknown error during reversing edge ' + parent + ' -> ' + child)

    def set_values(self, vertex, values):
        if vertex not in self.net:
            print('Vertex ' + vertex + ' does not exist. Can\'t set it\'s values')
        else:
            self.net[vertex]['possible_values'] = values

    def check_cycle(self, v, u, reversing = False):
        graph = {}

        for node in self.nodes():
            children = []

            for child in self.net[node]['children']:
                children.append(child)

            graph[node] = children

        if not reversing:
            graph[v].append(u)
        else:
            graph[u].remove(v)
            graph[v].append(u)

        cycles = [[node] + path for node in graph for path in self.dfs(graph, node, node)]

        return len(cycles) > 0

    def nodes(self):
        for node in self.net:
            yield node

    def has_node(self, vertex):
        return vertex in self.net

    def has_edge(self, v, u):
        return\
            (v in self.net[u]['parents'] and
             u in self.net[v]['children']) or\
            (v in self.net[u]['children'] and
             u in self.net[v]['parents'])

    def is_parent(self, vertex, child):
        return\
            vertex in self.net[child]['parents'] and\
            child in self.net[vertex]['children']

    def q(self, vertex):
        possible_parents_values = []

        for parent in self.pa(vertex):
            for value in self.net[parent]['possible_values']:
                possible_parents_values.append(value)

        possible_parents_values = list(set(possible_parents_values))

        return len(possible_parents_values)

    def r(self, vertex):
        possible_values = []

        for value in self.net[vertex]['possible_values']:
            possible_values.append(value)

        possible_values = list(set(possible_values))

        return len(possible_values)

    def pa(self, vertex):
        return self.net[vertex]['parents']

    #TODO: adjust to real data sets
    def get_data_rows_number(self, data_set):
        number = len(data_set)
        if self.has_column_names:
            number -= 1

        return number

    def get_vertex_number(self):
        number = len(self.vertexes)

        return number

    def K(self):
        parameters_count = 0

        for vertex in self.net:
            parameters_count += (self.r(vertex) - 1)*self.q(vertex)

        return parameters_count

    def H(self, data_set):
        vertex_number = self.get_vertex_number(self)

        value = 0
        for i in range(1, vertex_number):
            for j in range(1, self.q(self, self.net[self.vertexes[i]])):
                for k in range(1, self.r(self, self.net[self.vertexes[i]])):
                    N = self.get_data_rows_number(self, data_set)
                    Nij = 0
                    for row in data_set:
                        if self.pa(self, self.net[self.vertexes[i]]) == row[j]:
                            Nij += 1
                    Nijk = 0
                    for row in data_set:
                        if self.pa(self, self.net[self.vertexes[i]]) == row[j] and self.r(self, self.net[self.vertexes[i]]==row[k]):
                            Nijk += 1

                    value += Nijk/N * math.log(Nijk/Nij)

        return value

    def MDL(self, data_set):
        metric = self.H(data_set) + self.K/2 * math.log(self.get_data_rows_number(self, data_set))
        return metric

    def score(self, data_set, metric):
        if metric == 'AIC':
            return self.AIC(data_set)
        elif metric == 'MDL':
            return self.MDL(data_set)
        else:
            return 0

    def AIC(self, data_set):
        metric = self.H(data_set) - self.K
        return metric

    @staticmethod
    def dfs(graph, start, end):
        fringe = [(start, [])]

        while fringe:
            state, path = fringe.pop()

            if path and state == end:
                yield path
                continue

            for next_state in graph[state]:
                if next_state in path:
                    continue

                fringe.append((next_state, path + [next_state]))
