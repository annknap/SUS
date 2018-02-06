from BayesNet import *

if __name__ == '__main__':
    data = [['1', '2', '3', '4', '5', '6'], ['2', '3', '4', '5', '6', '7'], ['3', '4', '5', '6', '7', '8']]
    bn = BayesNet(data)

    bn.add_edge('A','B')
    bn.add_edge('B','C')
    bn.add_edge('C','D')
    bn.add_edge('A','F')
    bn.add_edge('F','D')
    bn.add_edge('A','E')
    bn.add_edge('E','C')
    bn.add_edge('E','D')

    bn.draw_graph()

    print(bn)
