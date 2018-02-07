from time import sleep
import csv

from BayesNet import *
from Learning import *


def load_from_csv(filename):
    rows = csv.reader(open(filename, "rb"))
    dataset = list(rows)

    for i in range(len(dataset)):
        dataset[i] = [float(x) for x in dataset[i]]

    return dataset


if __name__ == '__main__':
    data = [['1', '2', '3', '4', '5', '6'], ['2', '3', '4', '5', '6', '7'], ['3', '4', '5', '6', '7', '8']]
    #bn = BayesNet(data)

    """
    bn.add_edge('A','B')
    bn.add_edge('B','C')
    bn.add_edge('C','D')
    bn.add_edge('A','F')
    bn.add_edge('F','D')
    bn.add_edge('A','E')
    bn.add_edge('E','C')
    bn.add_edge('E','D')
    """

    data = load_from_csv('pima-indians-diabetes.data.csv')
    bn = Learning.TAN(data)

    bn.draw_graph()

    print(bn)
