__author__ = 'Kyle Vitautas Lopin'

import Tkinter as tk

class test_top(tk.Toplevel):

    def __init__(self, _master):
        tk.Toplevel.__init__(self, master=_master)

