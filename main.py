from BayesNet import *

if __name__ == '__main__':
    data = [['1', '2', '3', '4', '5', '6'], ['2', '3', '4', '5', '6', '7'], ['3', '4', '5', '6', '7', '8']]
    bn = BayesNet(data)

    print(bn)
