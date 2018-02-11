import csv
from Tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from BayesNet import BayesNet
from tkFileDialog import askopenfilename, asksaveasfilename
from Learning import *
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as pyplot


class Application(Tk):
    metric = "AIC"
    algorithm = "HC_O"
    debug = True

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.file_name = ""
        self.save_file_name = ""
        self.actual_figure = None
        self.data_set = None
        self.bayes_net = None

        Tk.wm_title(self, "Bayes Net learning")
        Tk.configure(self)
        Tk.resizable(self, 0, 0)

        menu_container = Frame(self)
        menu_container.grid(column = 0, row = 0, sticky = N, padx = 5, pady = 10)

        self.file_name_label = Label(menu_container)
        self.file_name_label.grid(column = 0, row = 0, columnspan = 3, pady = 10)

        choose_container = Frame(menu_container)
        choose_container.grid(column = 1, row = 1, sticky = N, padx = 5, pady = 10)

        choose_metric_container = Frame(choose_container)
        choose_metric_container.grid(column = 0, row = 0, sticky = W, padx = 10)

        choose_algorithm_container = Frame(choose_container)
        choose_algorithm_container.grid(column = 1, row = 0, sticky = W, padx = 10)

        chart_container = Frame(self)
        chart_container.grid(column = 0, row = 1, sticky = W)

        open_file_button = Button(menu_container, text = "Choose file", command = self.choose_file)
        open_file_button.grid(column = 0, row = 1, sticky = E, padx = 15)

        self.selected_metric = StringVar()
        AIC_radio_button = Radiobutton(choose_metric_container, text = "AIC", variable = self.selected_metric,
                                       value = "AIC", command = self.change_metric)
        AIC_radio_button.select()
        AIC_radio_button.pack(side = "top", anchor = W)
        MDL_radio_button = Radiobutton(choose_metric_container, text = "MDL", variable = self.selected_metric,
                                       value = "MDL", command = self.change_metric)
        MDL_radio_button.pack(side = "top", anchor = W)

        self.selected_algorithm = StringVar()
        HC_O_radio_button = Radiobutton(choose_algorithm_container, text = "Hill Climbing with one loops",
                                        variable = self.selected_algorithm, value = "HC_O",
                                        command = self.change_algorithm)
        HC_O_radio_button.select()
        HC_O_radio_button.pack(side = "top", anchor = W)
        HC_M_radio_button = Radiobutton(choose_algorithm_container, text = "Hill Climbing with multiple loop",
                                        variable = self.selected_algorithm, value = "HC_M",
                                        command = self.change_algorithm)
        HC_M_radio_button.pack(side = "top", anchor = W)
        TAN_radio_button = Radiobutton(choose_algorithm_container, text = "TAN", variable = self.selected_algorithm,
                                       value = "TAN",
                                       command = self.change_algorithm)
        TAN_radio_button.pack(side = "top", anchor = W)

        learn_button = Button(menu_container, text = "Learn", command = self.learn)
        learn_button.grid(column = 2, row = 1, sticky = E, padx = 15)

        # save_button = Button(menu_container, text = "Save chart", command = self.save_file)
        # save_button.grid(column = 2, row = 2, sticky = E, padx = 15)

        self.metric_label = Label(menu_container)
        self.metric_label.grid(column = 1, row = 2)

        self.chart = pyplot.Figure(figsize = (5, 5), dpi = 100)
        self.sub_chart = self.chart.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.chart, chart_container)

        self.toolbar = NavigationToolbar2TkAgg(self.canvas, chart_container)
        self.toolbar.update()

    def change_metric(self):
        self.metric = self.selected_metric.get()

    def change_algorithm(self):
        self.algorithm = self.selected_algorithm.get()

    def choose_file(self):
        self.file_name = askopenfilename()
        self.file_name_label.configure(text = self.file_name)
        self.data_set = Application.load_from_csv(self.file_name)
        self.bayes_net = BayesNet(self.data_set)

    def save_file(self):
        self.save_file_name = asksaveasfilename(initialdir = self.file_name, title = "Save",
                                                filetypes = (("PNG files", "*.png"), ("all files", "*.*")))
        pyplot.savefig(self.save_file_name, bbox_inches = 'tight')

    def learn(self):
        if self.data_set is not None:
            self.sub_chart.cla()
            pyplot.axis('off')
            self.bayes_net = Learning.learn(self.data_set, self.metric, self.algorithm, self.debug)
            self.bayes_net.draw_graph(self.sub_chart)
            self.metric_label.configure(text = str(self.bayes_net.score(self.data_set, self.metric)))
            self.canvas.show()
            self.toolbar.update()
            self.canvas.get_tk_widget().pack(side = 'bottom', fill = 'both', expand = True)

    @staticmethod
    def load_from_csv(file_name):
        rows = csv.reader(open(file_name, "rb"))
        data_set = list(rows)

        for i in range(len(data_set)):
            data_set[i] = [float(x) for x in data_set[i]]

        return data_set

    def _quit(self):
        self.quit()
        self.destroy()
