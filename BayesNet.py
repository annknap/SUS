class BayesNet:
    def __init__(self, data_set, has_column_names = False):
        self.net = {}
        self.data_set = data_set

        column_names = data_set[0]

        if has_column_names is False:
            column_names = []
            column_name = 'A'

            for column in data_set[0]:
                column_names.append(column_name)
                column_name = chr(ord(column_name) + 1)

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
        elif self.check_cycle(child, parent) > 0:
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

    def check_cycle(self, vertex, new_child):
        cycles = []

        for parent in self.pa(vertex):
            if new_child in self.pa(parent) or parent is new_child:
                cycles.append(parent)

        return len(cycles)

    def nodes(self):
        for node in self.net:
            yield node

    def has_node(self, vertex):
        return vertex in self.net

    def has_edge(self, vertex, children):
        return vertex in self.net[children]['parents'] and children in self.net[vertex]['children']

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

    def K(self):
        parameters_count = 0

        for vertex in self.net:
            parameters_count += (self.r(vertex) - 1)*self.q(vertex)

        return parameters_count

    def H(self, data_set):
        """ TODO """
        return 0

    def AIC(self, data_set):
        metric = self.H(data_set) - self.K
        return metric
