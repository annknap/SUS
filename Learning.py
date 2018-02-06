from BayesNet import *


class Learning:
    @staticmethod
    def read_file(file_name):
        return []

    @staticmethod
    def hill_climbing(data_set, metric = 'AIC'):
        bayes_net = BayesNet(data_set)
        score = bayes_net.score(data_set, metric)

        while True:
            max_score = score

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

            for node_i in bayes_net.nodes():
                for node_j in bayes_net.pa(node_i):
                    bayes_net.delete_edge(node_j, node_i)
                    new_score = bayes_net.score(data_set, metric)
                    if new_score <= score:
                        bayes_net.add_edge(node_j, node_i)
                    else:
                        score = new_score

            for node_i in bayes_net.nodes():
                for node_j in bayes_net.pa(node_i):
                    if bayes_net.check_cycle(node_i, node_j, True):
                        bayes_net.reverse_edge(node_j, node_i)
                        new_score = bayes_net.score(data_set, metric)
                        if new_score <= score:
                            bayes_net.reverse_edge(node_j, node_i)
                        else:
                            score = new_score

            if score < max_score:
                break

        return
