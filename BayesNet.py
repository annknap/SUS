from math import *
from networkx import *
import copy


class BayesNet:
    def __init__(self, data_set, has_column_names = False):
        self.net = {}
        self.has_column_names = has_column_names
        self.network_graph = DiGraph()

        column_names = data_set[0]

        if has_column_names is False:
            column_names = []
            column_name = 'A'

            for column in data_set[0]:
                column_names.append(column_name)
                column_name = chr(ord(column_name) + 1)

        self.vertexes = column_names

        self.data = {}

        for column in range(0, len(data_set[0])):
            if has_column_names:
                start = 1
            else:
                start = 0
            self.data[column_names[column]] = []
            for row in range(start, len(data_set)):
                self.data[column_names[column]].append(data_set[row][column])

        for vertex in column_names:
            self.net[vertex] = {'possible_values': [],
                                'children': [],
                                'parents': [],
                                'probabilities': []}

            values = set(self.data[vertex])
            self.set_values(vertex, values)

    def add_edge_no_directions(self, vertex_1, vertex_2, edges, weight):
        if vertex_1 not in self.net:
            print('Vertex ' + str(vertex_1) + ' does not exist. Can\'t create edge ' + str(vertex_1) + ' - ' + str(
                vertex_2))
        elif vertex_2 not in self.net:
            print('Vertex ' + str(vertex_2) + ' does not exist. Can\'t create edge ' + str(vertex_1) + ' - ' + str(
                vertex_2))
        else:
            if vertex_1 not in edges.keys():
                edges[vertex_1] = {}
            if vertex_2 not in edges.keys():
                edges[vertex_2] = {}

            edges[vertex_1][vertex_2] = weight
            edges[vertex_2][vertex_1] = weight

        return edges

    def check_cycles_no_directions(self, edges, vertex_1, vertex_2):

        new_edges = copy.deepcopy(edges)
        if vertex_1 not in new_edges.keys():
            new_edges[vertex_1] = {}

        if vertex_2 not in new_edges.keys():
            new_edges[vertex_2] = {}

        new_edges[vertex_1][vertex_2] = 0
        new_edges[vertex_2][vertex_1] = 0
        graph = {}

        for vertex in new_edges.keys():
            if vertex not in graph.keys():
                graph[vertex] = []

            for node in new_edges[vertex].keys():
                if node not in graph[vertex]:
                    graph[vertex].append(node)

        visited = []
        parent = -1
        node = vertex_1
        is_cyclic = self.cycles_undirected(graph, node, visited, parent)

        return is_cyclic

    def cycles_undirected(self, graph, node, visited, parent):
        visited.append(node)

        for i in graph[node]:
            if i not in visited:
                if not self.cycles_undirected(graph, i, visited, node):
                    return False
            elif parent != i:
                return False

        return True

    def add_edge(self, vertex, new_child):
        if vertex not in self.net:
            print('Vertex ' + str(vertex) + ' does not exist. Can\'t create edge ' + str(vertex) + ' -> ' + str(
                new_child))
        elif new_child not in self.net:
            print('Vertex ' + str(new_child) + ' does not exist. Can\'t create edge ' + str(vertex) + ' -> ' + str(
                new_child))
        elif vertex in self.net[new_child]['parents'] and new_child in self.net[vertex]['children']:
            print('Edge ' + str(vertex) + ' -> ' + str(new_child) + ' already exists')
        elif vertex not in self.net[new_child]['parents'] and new_child in self.net[vertex]['children']:
            print('Wrong net structure. Vertex ' + str(vertex) + ' is not a parent of vertex ' + str(new_child) +
                  ' but vertex ' + str(new_child) + ' is a child of vertex ' + str(vertex))
        elif vertex in self.net[new_child]['parents'] and new_child not in self.net[vertex]['children']:
            print('Wrong net structure. Vertex ' + str(new_child) + ' is not a child of vertex ' + str(vertex) +
                  ' but vertex ' + str(vertex) + ' is a parent of vertex ' + str(new_child))
        elif self.check_cycle(vertex, new_child) > 0:
            print('Adding edge ' + str(vertex) + ' -> ' + str(new_child) + ' will create a cycle')
        elif vertex not in self.net[new_child]['parents'] and new_child not in self.net[vertex]['children']:
            self.net[vertex]['children'].append(new_child)
            self.net[new_child]['parents'].append(vertex)
        else:
            print('Unknown error during adding edge ' + str(vertex) + ' -> ' + str(new_child))

    def delete_edge(self, vertex, old_child):
        if vertex not in self.net:
            print('Vertex ' + str(vertex) + ' does not exist. Can\'t delete edge ' + str(vertex) + ' -> ' + str(
                old_child))
        elif old_child not in self.net:
            print('Vertex ' + str(old_child) + ' does not exist. Can\'t delete edge ' + str(vertex) + ' -> ' + str(
                old_child))
        elif vertex not in self.net[old_child]['parents'] and old_child not in self.net[vertex]['children']:
            print('Edge ' + str(vertex) + ' -> ' + str(old_child) + ' does not exist')
        elif vertex not in self.net[old_child]['parents'] and old_child in self.net[vertex]['children']:
            print('Wrong net structure. Vertex ' + str(vertex) + ' is not a parent of vertex ' + str(old_child) +
                  ' but vertex ' + str(old_child) + ' is a child of vertex ' + str(vertex))
        elif vertex in self.net[old_child]['parents'] and old_child not in self.net[vertex]['children']:
            print('Wrong net structure. Vertex ' + str(old_child) + ' is not a child of vertex ' + str(vertex) +
                  ' but vertex ' + str(vertex) + ' is a parent of vertex ' + str(old_child))
        elif vertex in self.net[old_child]['parents'] and old_child in self.net[vertex]['children']:
            self.net[vertex]['children'].remove(old_child)
            self.net[old_child]['parents'].remove(vertex)
        else:
            print('Unknown error during deleting edge ' + str(vertex) + ' -> ' + str(old_child))

    def reverse_edge(self, parent, child):
        if parent not in self.net:
            print('Vertex ' + str(parent) + ' does not exist. Can\'t reverse edge ' + str(parent) + ' -> ' + str(child))
        elif child not in self.net:
            print('Vertex ' + str(child) + ' does not exist. Can\'t reverse edge ' + str(parent) + ' -> ' + str(child))
        elif parent not in self.net[child]['parents'] and child not in self.net[parent]['children']:
            print('Edge ' + str(parent) + ' -> ' + str(child) + ' does not exist')
        elif parent not in self.net[child]['parents'] and child in self.net[parent]['children']:
            print('Wrong net structure. Vertex ' + str(parent) + ' is not a parent of vertex ' + str(child) +
                  ' but vertex ' + str(child) + ' is a child of vertex ' + str(parent))
        elif parent in self.net[child]['parents'] and child not in self.net[parent]['children']:
            print('Wrong net structure. Vertex ' + str(child) + ' is not a child of vertex ' + str(parent) +
                  ' but vertex ' + str(parent) + ' is a parent of vertex ' + str(child))
        elif self.check_cycle(child, parent, True) > 0:
            print('Reversing edge ' + str(parent) + ' -> ' + str(child) + ' will create a cycle')
        elif parent in self.net[child]['parents'] and child in self.net[parent]['children']:
            self.net[parent]['children'].remove(child)
            self.net[parent]['parents'].append(child)
            self.net[child]['parents'].remove(parent)
            self.net[child]['children'].append(parent)
        else:
            print('Unknown error during reversing edge ' + str(parent) + ' -> ' + str(child))

    def set_values(self, vertex, values):
        if vertex not in self.net:
            print('Vertex ' + str(vertex) + ' does not exist. Can\'t set it\'s values')
        else:
            self.net[vertex]['possible_values'] = values

    def check_cycle(self, v, u, reversing = False):
        graph = {}

        for node in self.nodes():
            children = []

            for child in self.net[node]['children']:
                children.append(child)

            graph[node] = children

        if reversing and v in graph[u]:
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

    def get_data_set_rows_number(self, data_set):
        number = len(data_set)
        if self.has_column_names:
            number -= 1

        return number

    def nodes_number(self):
        number = len(self.vertexes)

        return number

    def K(self):
        parameters_count = 0

        for vertex in self.net:
            parameters_count += (self.r(vertex) - 1)*self.q(vertex)

        return parameters_count

    def H(self, data_set):
        vertex_number = self.nodes_number()
        nodes = self.net.keys()
        value = 0
        N = self.get_data_set_rows_number(data_set)
        for i in range(0, vertex_number):
            for j in range(0, len(self.net[nodes[i]]['parents'])):
                for k in range(0, len(self.net[nodes[i]]['parents'])):

                    Nij = 0
                    Nijk = 0
                    for row in data_set:

                        parent_values = []
                        for parent_value in self.net[nodes[i]]['parents'][k]:
                            parent_values.append(parent_value)

                        for parent_value in parent_values:
                            if parent_value == row[j]:
                                Nij += 1
                                possible_node_values = self.net[nodes[i]]['possible_values']
                                for possible_node_value in possible_node_values:
                                    if possible_node_value == row[k]:
                                        Nijk += 1

                    if Nij == 0.0:
                        Nij = pow(10, -20)

                    if Nijk == 0.0:
                        Nijk = pow(10, -20)

                    value += (Nijk/N)*log(Nijk/Nij)

            value *= -N
        return value

    def MDL(self, data_set):
        metric = self.H(data_set) + self.K()/2*log(self.get_data_set_rows_number(data_set))
        return metric

    def score(self, data_set, metric):
        if metric == 'AIC':
            return self.AIC(data_set)
        elif metric == 'MDL':
            return self.MDL(data_set)
        else:
            return 0

    def AIC(self, data_set):
        metric = self.H(data_set) + self.K()
        ll=self.H(data_set)
        penalty=self.K()
        return metric

    def draw_graph(self, subplot,
                   graph_layout = 'shell',
                   node_size = 800,
                   node_color = 'blue',
                   node_alpha = 0.2,
                   node_text_size = 10,
                   edge_color = 'blue',
                   edge_alpha = 0.4,
                   edge_thickness = 1,
                   text_font = 'sans-serif'):

        graph = []

        for node in self.nodes():
            for child in self.net[node]['children']:
                node_label = node
                child_label = child
                if len(self.net[node]['parents']) == 0:
                    node_label += " (root)"
                if len(self.net[node]['children']) == 0:
                    node_label = "(" + node_label + ")"
                if len(self.net[child]['parents']) == 0:
                    child_label += " (root)"
                if len(self.net[child]['children']) == 0:
                    child_label = "(" + child_label + ")"
                graph.append((node_label, child_label))

        for edge in graph:
            self.network_graph.add_edge(edge[0], edge[1])

        if graph_layout == 'spring':
            graph_pos = spring_layout(self.network_graph)
        elif graph_layout == 'shell':
            graph_pos = shell_layout(self.network_graph)
        elif graph_layout == 'spectral':
            graph_pos = spectral_layout(self.network_graph)
        elif graph_layout == 'random':
            graph_pos = random_layout(self.network_graph)
        else:
            graph_pos = shell_layout(self.network_graph)

        draw_networkx_nodes(self.network_graph, graph_pos, ax = subplot, node_size = node_size,
                            alpha = node_alpha, node_color = node_color)
        draw_networkx_edges(self.network_graph, graph_pos, ax = subplot, width = edge_thickness,
                            alpha = edge_alpha, edge_color = edge_color)
        draw_networkx_labels(self.network_graph, graph_pos, ax = subplot, font_size = node_text_size,
                             font_family = text_font)

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
