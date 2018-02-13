from BayesNet import *
import numpy as np


class Learning:

    @staticmethod
    def log(message, debug = True):
        if debug:
            print(message)

    @staticmethod
    def hill_climbing_multiple_loops(data_set, metric = 'AIC', debug = False):
        bayes_net = BayesNet(data_set)
        score = bayes_net.score(data_set, metric)

        while True:
            max_score = score
            Learning.log('Score: ' + str(score), debug)

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
                                Learning.log(
                                    'Adding edge ' + str(node_j) + ' -> ' + str(node_i) + '. New score: ' + str(score),
                                    debug)

            for node_i in bayes_net.nodes():
                for node_j in bayes_net.pa(node_i):
                    bayes_net.delete_edge(node_j, node_i)
                    new_score = bayes_net.score(data_set, metric)
                    if new_score <= score:
                        bayes_net.add_edge(node_j, node_i)
                    else:
                        score = new_score
                        Learning.log(
                            'Deleting edge ' + str(node_j) + ' -> ' + str(node_i) + '. New score: ' + str(score),
                            debug)

            for node_i in bayes_net.nodes():
                for node_j in bayes_net.pa(node_i):
                    if not bayes_net.check_cycle(node_i, node_j, True):
                        bayes_net.reverse_edge(node_j, node_i)
                        new_score = bayes_net.score(data_set, metric)
                        if new_score <= score:
                            bayes_net.reverse_edge(node_i, node_j)
                        else:
                            score = new_score
                            Learning.log(
                                'Reversing edge ' + str(node_j) + ' -> ' + str(node_i) + '. New score: ' + str(score),
                                debug)

            if score <= max_score:
                break

        Learning.log('Learning bayes net ended. Score achieved: ' + str(score), debug)
        return bayes_net

    @staticmethod
    def hill_climbing_one_loop(data_set, metric = 'AIC', debug = False):
        bayes_net = BayesNet(data_set)
        score = bayes_net.score(data_set, metric)

        while True:
            max_score = score
            Learning.log('Score: ' + str(score), debug)

            for node_i in bayes_net.nodes():
                for node_j in bayes_net.nodes():
                    if node_i != node_j:
                        if not bayes_net.is_parent(node_j, node_i):
                            if not bayes_net.check_cycle(node_j, node_i):
                                bayes_net.add_edge(node_j, node_i)
                                new_score = bayes_net.score(data_set, metric)
                                if new_score <= score:
                                    bayes_net.delete_edge(node_j, node_i)
                                else:
                                    score = new_score
                                    Learning.log(
                                        'Adding edge ' + str(node_j) + ' -> ' + str(node_i) + '. New score: ' + str(
                                            score), debug)

                        if bayes_net.is_parent(node_j, node_i):
                            bayes_net.delete_edge(node_j, node_i)
                            new_score = bayes_net.score(data_set, metric)
                            if new_score <= score:
                                bayes_net.add_edge(node_j, node_i)
                            else:
                                score = new_score
                                Learning.log(
                                    'Deleting edge ' + str(node_j) + ' -> ' + str(node_i) + '. New score: ' + str(
                                        score), debug)

                        if bayes_net.is_parent(node_j, node_i):
                            if not bayes_net.check_cycle(node_i, node_j, True):
                                bayes_net.reverse_edge(node_j, node_i)
                                new_score = bayes_net.score(data_set, metric)
                                if new_score <= score:
                                    bayes_net.reverse_edge(node_i, node_j)
                                else:
                                    score = new_score
                                    Learning.log(
                                        'Reversing edge ' + str(node_j) + ' -> ' + str(node_i) + '. New score: ' + str(
                                            score), debug)

            if score <= max_score:
                break

        Learning.log('Learning bayes net ended. Score achieved: ' + str(score), debug)
        return bayes_net

    @staticmethod
    def learn(data_set, metric = 'AIC', algorithm = 'HC_O', debug = False):
        if algorithm == 'HC_M':
            return Learning.hill_climbing_multiple_loops(data_set, metric, debug)
        if algorithm == 'HC_O':
            return Learning.hill_climbing_one_loop(data_set, metric, debug)
        elif algorithm == 'TAN':
            return Learning.TAN(data_set, metric, debug)
        else:
            return 0

    @staticmethod
    def TAN(data_set, metric = '', debug = True):

        Learning.log('TAN: Learning bayes net started.', debug)
        data_set_1 = np.array(data_set)
        class_values = data_set_1[:, len(data_set[0]) - 1]

        data_set = data_set_1[:, :len(data_set[0]) - 1]

        bayes_net = BayesNet(data_set)

        possible_class_values = []
        for x in class_values:
            if x not in possible_class_values:
                possible_class_values.append(x)

        n = bayes_net.get_data_set_rows_number(data_set)
        weights = {}
        l = float(len(class_values))

        Learning.log('TAN: Mutual information calculating in progress.', debug)
        for node_i in bayes_net.nodes():
            weights[node_i] = {}
            for node_j in bayes_net.nodes():

                already_included = False
                if node_j in weights.keys():
                    if node_i in weights[node_j].keys():
                        weights[node_i][node_j] = weights[node_j][node_i]
                        already_included = True

                if node_i != node_j and not already_included:

                    values_i = list(bayes_net.net[node_i]['possible_values'])
                    values_j = list(bayes_net.net[node_j]['possible_values'])

                    mutual_information = 0
                    xxx = 0

                    for k in range(0, len(possible_class_values)):
                        for i in range(0, len(values_i)):
                            for j in range(0, len(values_j)):
                                count_i = float(bayes_net.data[node_i].count(values_i[i]))
                                count_j = float(bayes_net.data[node_j].count(values_j[j]))
                                count_k = float(np.count_nonzero(class_values == possible_class_values[k]))

                                count_x = 0.0
                                count_z = 0.0
                                for index in range(0, len(bayes_net.data[node_i])):
                                    if bayes_net.data[node_i][index] == values_i[i]:
                                        if class_values[index] == possible_class_values[k]:
                                            count_z += 1.0
                                            if bayes_net.data[node_j][index] == values_j[j]:
                                                count_x += 1.0

                                count_y = 0.0
                                for index in range(0, len(bayes_net.data[node_j])):
                                    if bayes_net.data[node_j][index] == values_j[j]:
                                        if class_values[index] == possible_class_values[k]:
                                            count_y += 1.0

                                Pi = float(count_i/l)
                                Pj = float(count_j/l)
                                Pk = float(count_k/l)

                                Pijk = Pi*Pj*Pk

                                Px = float(count_x/count_k)

                                Pz = float(count_z/count_k)
                                Py = float(count_y/count_k)

                                if Pz != 0.0 and Py != 0 and Px != 0:

                                    mutual_information = mutual_information + Pijk*log(float(Px/(Pz*Py)))

                    weights[node_i][node_j] = mutual_information
                    Learning.log('TAN: Mutual information for nodes: ' + str(node_i) + " " + str(node_j) + ' : ' + str(
                        weights[node_i][node_j]), debug)

        Learning.log('TAN: Mutual informations calculating done.', debug)
        print weights
        edges = {}
        possible_edges_num = len(bayes_net.net.keys())*(len(bayes_net.net.keys()) - 1)/2

        Learning.log('TAN: Tree building in progress.', debug)
        while possible_edges_num > 0:
            causing_cycle = False
            check_next = True
            i = 0
            create_edge = False
            max_weight = -100000

            vertex_1 = None
            vertex_2 = None

            not_to_be_checked = {}
            while check_next:
                max_weight = -100000
                for node_i in bayes_net.nodes():
                    for node_j in bayes_net.nodes():

                        to_pass = False
                        if node_i not in not_to_be_checked.keys():
                            if node_j not in not_to_be_checked.keys():
                                to_pass = True
                            elif node_i not in not_to_be_checked[node_j]:
                                to_pass = True
                        elif node_j not in not_to_be_checked[node_i]:
                            to_pass = True

                        if to_pass:
                            if (node_i not in edges.keys() or
                                node_j not in edges.keys() or
                                node_j not in edges[node_i].keys() or
                                node_i not in edges[node_j].keys())\
                                    and node_i != node_j:
                                if weights[node_i][node_j] > max_weight:
                                    max_weight = weights[node_i][node_j]

                                    vertex_1 = node_i
                                    vertex_2 = node_j
                causing_cycle = bayes_net.check_cycles_no_directions(edges, vertex_1, vertex_2)

                if causing_cycle:
                    create_edge = True
                    causing_cycle = False
                    check_next = False
                    # possible_edges_num -= 1
                    # break
                else:
                    i += 1
                    if vertex_1 not in not_to_be_checked.keys():
                        not_to_be_checked[vertex_1] = []
                    if vertex_2 not in not_to_be_checked.keys():
                        not_to_be_checked[vertex_2] = []

                    not_to_be_checked[vertex_1].append(vertex_2)
                    not_to_be_checked[vertex_2].append(vertex_1)

                if i == possible_edges_num:
                    check_next = False
                    i = 0

            if create_edge:
                edges = bayes_net.add_edge_no_directions(vertex_1, vertex_2, edges, max_weight)
            possible_edges_num -= 1

        print edges
        Learning.log('TAN: Tree building in progress - adding directions.', debug)

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

            l = len(possible)

        Learning.log('TAN: Tree building done.', debug)

        Learning.log('TAN: Adding class as a root and linking it to all other nodes.', debug)

        for node in bayes_net.nodes():
            bayes_net.net[node]['parents'].append('root')

        bayes_net.vertexes = bayes_net.vertexes[:-1]
        bayes_net.vertexes.append('root')

        root_children = bayes_net.net.keys()
        bayes_net.net['root'] = {}
        bayes_net.net['root']['possible_values'] = possible_class_values
        bayes_net.net['root']['children'] = root_children
        bayes_net.net['root']['parents'] = []
        bayes_net.net['root']['probabilities'] = []

        for node in bayes_net.net.keys():
            print "node: ", node, " parents: ", bayes_net.net[node]['parents'], " children: ", bayes_net.net[node][
                'children']

        Learning.log('TAN: Creating TAN tree done.', debug)
        score = bayes_net.score(data_set, metric)
        Learning.log('TAN: Score: ' + str(score), debug)

        return bayes_net
