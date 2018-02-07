from BayesNet import *


class Learning:
    @staticmethod
    def log(message, debug = True):
        if debug:
            print(message)

    @staticmethod
    def read_file(file_name):
        return []

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
            return "TAN"
        else:
            return 0

    def TAN(data_set, metric='', debug=False):
        bayes_net = BayesNet(data_set)

        n = bayes_net.get_data_rows_number(bayes_net, data_set)
        weights = {}
        for node_i in bayes_net.nodes():
            weights[node_i] = {}
            for node_j in bayes_net.nodes():

                values_i = bayes_net.net[node_i]['possible_values']
                values_j = bayes_net.net[node_j]['possible_values']
                values_i.sort()
                values_j.sort()

                mutual_information = 0

                for i in values_i:
                    for j in values_j:
                        Pi = 0
                        Pj = 0
                        for value in bayes_net.data[node_i]:
                            if value == i:
                                Pi += 1
                        for value in bayes_net.data[node_j]:
                            if value == j:
                                Pj += 1
                        Pij = (Pi+Pj)/len(bayes_net.data[node_i])
                        Pi = Pi/len(bayes_net.data[node_i])
                        Pj = Pj/len(bayes_net.data[node_i])

                        mutual_information += Pij * math.log(Pij/(Pi*Pj))

                weights[node_i][node_j] = mutual_information

        edges = {}
        no_cycles = True
        possible_edges_num = len(bayes_net.nodes())*(len(bayes_net.nodes())-1)/2

        while possible_edges_num > 0:

            causing_cycle = True
            i = possible_edges_num
            while causing_cycle:
                max_weight = 0
                for node_i in bayes_net.nodes(bayes_net):
                    for node_j in bayes_net.nodes(bayes_net):

                        if node_i not in edges.keys() or node_j not in edges[node_i].keys():
                            if weights[node_i][node_j] > max_weight:
                                max_weight = weights[node_i][node_j]

                if not bayes_net.check_cycles_no_directions(bayes_net, edges, node_i, node_j):
                    create_edge = True
                    break
                else: i+=1

                if i==possible_edges_num: break

            if create_edge:
                edges = bayes_net.add_edge_no_directions(bayes_net, node_i, node_j, edges, max_weight)
            possible_edges_num -= 1

        root = bayes_net.nodes(bayes_net)[0]

        possible = []

        while len(edges.keys()) > 0:

            if root in edges.keys():
                for child in edges[root]:
                    bayes_net.add_edge(bayes_net, root, child)
                    del edges[root][child]
                    del edges[child][root]
                    possible.append(child)

            if len(possible)>0:
                root = possible[0]
                del possible[0]

        return bayes_net



