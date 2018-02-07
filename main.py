from Application import *
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
    data = load_from_csv('pima-indians-diabetes.data.csv')

    app = Application(data)
    app.mainloop()

    quit()
