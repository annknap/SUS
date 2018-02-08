from BayesNet import *
import math

class Learning:

    @staticmethod
    def log(message, debug = True):
        if debug:
            print(message)

    @staticmethod
    def hill_climbing(data_set, metric = 'AIC', debug = False):
        bayes_net = BayesNet(data_set)
        score = bayes_net.score(data_set, metric)

        while True:
            max_score = score
            Learning.log('Score: ' + score, debug)

            for node_i in bayes_net.nodes():
                for node_j in bayes_net.nodes():
                    if node_i != node_j and not bayes_net.is_parent(node_j, node_i):
                        if not bayes_net.check_cycle(node_j, node_i):
                            bayes_net.add_edge(node_j, node_i)
                            new_score = bayes_net.score(data_set, metric)
                            if new_score <= score:
                                bayes_net.delete_edge(node_j, node_i)
                            else:
                                score = new_score
                                Learning.log('Adding edge ' + node_j + ' -> ' + node_i + '. New score: ' + score, debug)

            for node_i in bayes_net.nodes():
                for node_j in bayes_net.pa(node_i):
                    bayes_net.delete_edge(node_j, node_i)
                    new_score = bayes_net.score(data_set, metric)
                    if new_score <= score:
                        bayes_net.add_edge(node_j, node_i)
                    else:
                        score = new_score
                        Learning.log('Deleting edge ' + node_j + ' -> ' + node_i + '. New score: ' + score, debug)

            for node_i in bayes_net.nodes():
                for node_j in bayes_net.pa(node_i):
                    if bayes_net.check_cycle(node_i, node_j, True):
                        bayes_net.reverse_edge(node_j, node_i)
                        new_score = bayes_net.score(data_set, metric)
                        if new_score <= score:
                            bayes_net.reverse_edge(node_j, node_i)
                        else:
                            score = new_score
                            Learning.log('Reversing edge ' + node_j + ' -> ' + node_i + '. New score: ' + score, debug)

            if score < max_score:
                break

        Learning.log('Learning bayes net ended. Score achieved: ' + score, debug)
        return bayes_net

    @staticmethod
    def learn(data_set, metric = 'AIC', algorithm = 'HC', debug = False):
        if algorithm == 'HC':
            return Learning.hill_climbing(data_set, metric, debug)
        elif algorithm == 'TAN':
            return Learning.TAN(data_set, metric, debug)
        else:
            return 0

    @staticmethod
    def TAN(data_set, metric = '', debug = False):

        
        bayes_net = BayesNet(data_set)

        n = bayes_net.get_data_set_rows_number(data_set)
        weights = {}
        for node_i in bayes_net.nodes():
            weights[node_i] = {}
            for node_j in bayes_net.nodes():

                if node_i != node_j:
                    values_i = bayes_net.net[node_i]['possible_values']
                    values_j = bayes_net.net[node_j]['possible_values']

                    mutual_information = 0

                    for i in values_i:
                        for j in values_j:
                            Pi = 0
                            Pj = 0
                            Pi = bayes_net.data[node_i].count(i)
                            Pj = bayes_net.data[node_j].count(j)

                            l = float(len(bayes_net.data[node_i]))
                            Pij = float((Pi + Pj)/l)
                            Pi = float(Pi/l)
                            Pj = float(Pj/l)

                            mutual_information += Pij*math.log(Pij/(Pi*Pj))

                    weights[node_i][node_j] = mutual_information
        edges = {}
        no_cycles = True
        possible_edges_num = len(bayes_net.net.keys())*(len(bayes_net.net.keys()) - 1)/2

        while possible_edges_num > 0:
            causing_cycle = False
            check_next = True
            i = 0
            create_edge = False
            max_weight = 0

            vertex_1 = None
            vertex_2 = None

            while check_next:
                max_weight = 0
                for node_i in bayes_net.nodes():
                    for node_j in bayes_net.nodes():

                        if (node_i not in edges.keys() or node_j not in edges.keys() or node_j not in edges[node_i].keys() or node_i not in edges[node_j].keys()) and node_i != node_j:
                            if weights[node_i][node_j] > max_weight:
                                max_weight = weights[node_i][node_j]
                                vertex_1 = node_i
                                vertex_2 = node_j
                causing_cycle = bayes_net.check_cycles_no_directions(edges, vertex_1, vertex_2)

                if causing_cycle:
                    create_edge = True
                    causing_cycle = False
                    check_next = False
                    break
                else:
                    i += 1

                if i == possible_edges_num:
                    check_next = False
                    i = 0

            if create_edge:
                edges = bayes_net.add_edge_no_directions(vertex_1, vertex_2, edges, max_weight)
            possible_edges_num -= 1

        root = bayes_net.net.keys()[0]

        possible = []
        l = len(edges.keys())
        while l > 0:
            copy_dict = copy.deepcopy(edges)
            if root in copy_dict.keys():
                for child in copy_dict[root].keys():
                    bayes_net.add_edge(root, child)
                    del edges[root][child]
                    del edges[child][root]
                    possible.append(child)

            if len(possible) > 0:

                root = possible[0]
                del possible[0]

            l = len (possible)


        return bayes_net
