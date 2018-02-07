from Tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from BayesNet import BayesNet
import Learning
import matplotlib.pyplot as pyplot
import matplotlib

matplotlib.use("TkAgg")


class Application(Tk):
    metric = "AIC"
    algorithm = "HC"
    debug = True

    def __init__(self, data_set, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.data_set = data_set
        self.bayes_net = BayesNet(self.data_set)

        if self.debug:  # section to delete
            self.bayes_net.add_edge('A', 'B')
            self.bayes_net.add_edge('B', 'C')
            self.bayes_net.add_edge('C', 'D')
            self.bayes_net.add_edge('A', 'F')
            self.bayes_net.add_edge('F', 'D')
            self.bayes_net.add_edge('A', 'E')
            self.bayes_net.add_edge('E', 'C')
            self.bayes_net.add_edge('E', 'D')

        Tk.wm_title(self, "Bayes Net learning")
        Tk.configure(self)
        Tk.resizable(self, 0, 0)

        menu_container = Frame(self)
        menu_container.grid(column = 0, row = 0, sticky = N, padx = 5, pady = 10)

        choose_container = Frame(menu_container)
        choose_container.grid(column = 1, row = 0, sticky = N, padx = 5, pady = 10)

        choose_metric_container = Frame(choose_container)
        choose_metric_container.grid(column = 0, row = 0, sticky = W, padx = 10)

        choose_algorithm_container = Frame(choose_container)
        choose_algorithm_container.grid(column = 1, row = 0, sticky = W, padx = 10)

        chart_container = Frame(self)
        chart_container.grid(column = 0, row = 1, sticky = W)

        open_file_button = Button(menu_container, text = "Choose file", command = self.learn)
        open_file_button.grid(column = 0, row = 0, sticky = E, padx = 15)

        self.selected_metric = StringVar()
        AIC_radio_button = Radiobutton(choose_metric_container, text = "AIC", variable = self.selected_metric,
                                       value = "AIC", command = self.change_metric)
        AIC_radio_button.select()
        AIC_radio_button.pack(side = "top", anchor = W)
        MDL_radio_button = Radiobutton(choose_metric_container, text = "MDL", variable = self.selected_metric,
                                       value = "MDL", command = self.change_metric)
        MDL_radio_button.pack(side = "top", anchor = W)

        self.selected_algorithm = StringVar()
        HC_radio_button = Radiobutton(choose_algorithm_container, text = "Hill Climbing",
                                      variable = self.selected_algorithm, value = "HC",
                                      command = self.change_algorithm)
        HC_radio_button.select()
        HC_radio_button.pack(side = "top", anchor = W)
        TAN_radio_button = Radiobutton(choose_algorithm_container, text = "TAN", variable = self.selected_algorithm,
                                       value = "TAN",
                                       command = self.change_algorithm)
        TAN_radio_button.pack(side = "top", anchor = W)

        learn_button = Button(menu_container, text = "Learn", command = self.learn)
        learn_button.grid(column = 2, row = 0, sticky = E, padx = 15)

        chart = pyplot.Figure(figsize = (6, 6), dpi = 100)
        self.sub_chart = chart.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(chart, chart_container)

    def change_metric(self):
        self.metric = self.selected_metric.get()

    def change_algorithm(self):
        self.algorithm = self.selected_algorithm.get()

    def learn(self):
        self.sub_chart.cla()
        pyplot.axis('off')
        # Learning.learn(self.data_set, self.metric, self.algorithm, self.debug)
        self.bayes_net.draw_graph(self.sub_chart)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side = 'bottom', fill = 'both', expand = True)

    def _quit(self):
        self.quit()
        self.destroy()
