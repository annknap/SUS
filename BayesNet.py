class BayesNet:
    def __init__(self, vertices):
        self.net = {}

        for vertex in vertices:
            self.net[vertex] = {'possible_values': [],
                                'children': [],
                                'parents': [],
                                'probabilities': []}

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
