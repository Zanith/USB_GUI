__author__ = 'Kyle V Lopin'

import Tkinter as tk
import amp_usb
import ttk
import pyplot_to_tkinter
import change_toplevel as change_top

background_color = ''
operation_params = {'low_cv_voltage' : -500, 'high_cv_voltage' : 750, 'sweep_rate' : 10}  # units: mv, mv, V/s

class AmpGUI(tk.Tk):

    def __init__(self, parent=None):

        self.operation_params = operation_params

        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.device = amp_usb


        self.init()


    def init(self):
        """
        make all the widget elements in this method
        :return:
        """
        # create a notebook to keep two tabs, one for amperometry and one for cyclic voltammetry (CV)
        self.notebook = ttk.Notebook(self)
        amp_frame = ttk.Frame(self.notebook)
        cv_frame = ttk.Frame(self.notebook)
        self.notebook.add(amp_frame, text="Amperometry")
        self.notebook.add(cv_frame, text="Cyclic Voltammetry")

        amp_plot_properties = {'xlabel' : "'time'",
                               'ylabel' : "'current'",
                               'xlim' : "[0, 200]",
                               'ylim' : "[-.1,1]",
                               'title': "'Amperometry time course'",
                               'subplots_adjust': "bottom=0.15, left=0.12"}
        CV_plot_properties = {'xlabel' : "'voltage (mV)'",
                              'ylabel' : "'current'",
                              'xlim' : "[-500, 500]",
                              'ylim' : "[-1,1]",
                              'title': "'Cyclic Voltammetry'",
                              'subplots_adjust': "bottom=0.15, left=0.12"}

        figure_amp_frame = pyplot_to_tkinter.pyplot_embed(amp_plot_properties, amp_frame)
        figure_amp_frame.pack(side='top')

        figure_CV_frame = pyplot_to_tkinter.pyplot_embed(CV_plot_properties, cv_frame)
        figure_CV_frame.pack(side='left')

        # Make a frame to display all the cyclic voltammetry settings and to allow them to be changed
        CV_option_frame = tk.Frame(cv_frame)
        CV_option_frame.pack()

        # make a label that displays the low voltage, high voltage and frequency settings for the
        # cyclic voltammetry frame
        self.low_voltage_varstr = tk.StringVar()
        self.high_voltage_varstr = tk.StringVar()
        self.freq_varstr = tk.StringVar()

        cv_low_voltage_label = tk.Label(textvariable=self.low_voltage_varstr, master= CV_option_frame)
        cv_high_voltage_label = tk.Label(textvariable=self.high_voltage_varstr, master=CV_option_frame)
        cv_freq_label = tk.Label(textvariable=self.freq_varstr, master=CV_option_frame)

        self.cv_label_update()

        cv_low_voltage_label.pack()
        cv_high_voltage_label.pack()
        cv_freq_label.pack()

        # make a button to change the cyclic voltammetry settings
        tk.Button(CV_option_frame,
                  text="Change Settings",
                  command=lambda: self.change_cv_settings()).pack(side ='bottom')

        self.notebook.pack(side='top')

        self.connect_button = tk.Button(self, command=lambda: self.connect())
        if self.device:
            self.connect_button["text"] = "Connected"
            self.connect_button.config(bg='green')
        else:
            self.connect_button["text"] = "Not Connected"
            self.connect_button.config(bg='red')

        self.connect_button.pack(side='bottom')

    def change_cv_settings(self):  # note that self here is the main window
        top = change_top.setting_changes(self)  # self will become the master of the toplevel
        self.cv_label_update()

    def save_cv_changes(self, _low_volt):
        print _low_volt

    def cv_label_update(self):
        print 'updating'
        print operation_params['low_cv_voltage']
        self.low_voltage_varstr.set('Start voltage: '+str(operation_params['low_cv_voltage'])+' mV')
        self.high_voltage_varstr.set('End voltage: '+str(operation_params['high_cv_voltage'])+' mV')
        self.freq_varstr.set('Sweep rate: '+str(operation_params['sweep_rate'])+' V/s')


    def get_message(self):
        _device, ep_out, _ = self.device
        end_pt = _device[0][(0, 0)][0]
        ep_out.write('p_req')
        print _device.read(end_pt.bEndpointAddress, 10)


    def connect(self):

        if self.device:
            pass  # If a device is already connected and someone hits the button, ignore it
        else:
            self.device = amp_usb.connect_usb()  # If no device then try to connect
            if self.device:  # If a device was just found then change the button's appearance
                self.connect_button["text"] = 'Connected'
                self.connect_button.config(bg='green')
            else:
                print "No Device detected"  # If still no device detected, warn the user

    def send_message(self, message):
        if not self.device:
            print "Device not connected"
        elif len(message) > 10:
            print "Message is too long"
        else:
            _, ep_out, _ = self.device  # seperate out the OUT ENDPOINT
            ep_out.write(message)


if __name__ == '__main__':

    app = AmpGUI()
    app.title("Amperometry Device")
    app.geometry("800x400")
    app.mainloop()