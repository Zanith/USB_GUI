__author__ = 'Kyle Vitautas Lopin'

import Tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#matplotlib.use("TkAgg")



class pyplot_embed(tk.Frame):

    def __init__(self, plt_props, _master):

        tk.Frame.__init__(self, master=_master)
        self.init(plt_props)

    def init(self, plt_props):
        self.figure_bed = plt.figure(figsize=(7, 3.5))
        self.axis = self.figure_bed.add_subplot(111)

        for key, value in plt_props.iteritems():
            eval("plt." + key + "(" + value + ")")
        # self.axis.set_axis_bgcolor('red')
        self.figure_bed.set_facecolor('white')
        self.canvas = FigureCanvasTkAgg(self.figure_bed, master=self)
        self.canvas._tkcanvas.config(highlightthickness=0)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='top')
