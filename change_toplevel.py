__author__ = 'Kyle Vitautas Lopin'

import Tkinter as tk

class setting_changes(tk.Toplevel):
    """
    A modified tkinter toplevel that allows the user to input new voltage ranges to measure and to set
    the frequency
    """

    def __init__(self, _master):
        """
        Initialize the window
        :param _master: tk.Frame, the main window
        :return:
        """
        tk.Toplevel.__init__(self, master=_master)

        self.title("Change Cyclic Voltammetry Settings")

        # make labels and an entry widget for a user to change the starting voltage of the triangle wave
        tk.Label(self, text="Starting Voltage: ", padx=10, pady=10).grid(row=0, column=0)
        low_volt = tk.Entry(self)  # entry widget for the user to change the voltage
        low_volt.insert(0, str(_master.operation_params['low_cv_voltage']))  # put the current value in the entry widget
        low_volt.grid(row=0, column=1)
        tk.Label(self, text="mV", padx=10, pady=10).grid(row=0, column=3)

        # make labels and an entry widget for a user to change the ending voltage of the triangle wave
        tk.Label(self, text="Ending Voltage: ", padx=10, pady=10).grid(row=1, column=0)
        high_volt = tk.Entry(self)  # entry widget for the user to change the voltage
        high_volt.insert(0, _master.operation_params['high_cv_voltage'])  # put the current value in the entry widget
        high_volt.grid(row=1, column=1)
        tk.Label(self, text="mV", padx=10, pady=10).grid(row=1, column=3)

        # make labels and an entry widget for a user to change the esweep rate of the triangle wave
        tk.Label(self, text="Sweep Rate: ", padx=10, pady=10).grid(row=2, column=0)
        freq = tk.Entry(self)  # entry widget for the user to change the voltage
        freq.insert(0, _master.operation_params['sweep_rate'])  # put the current value in the entry widget
        freq.grid(row=2, column=1)
        tk.Label(self, text="V/s", padx=10, pady=10).grid(row=2, column=3)

        # make a button that will take the entry values and call a function to properly convert them and
        # send the correct values to the amperometry microcontroller
        tk.Button(self,
                  text='Save Changes',
                  command=lambda : self.save_cv_changes(low_volt.get(),
                  high_volt.get(),
                  freq.get(),
                  _master)).grid(row=3, column=0)

        # make a button to exit the toplevel by destroying it
        tk.Button(self,
                  text='Exit',
                  command=lambda : self.destroy()).grid(row=3, column=1)


    def save_cv_changes(self, _low_volt, _high_volt, _freq, _master):
        """

        :param _low_volt: user inputted value, should be an integer that will be the lower level of the triangle wave
        :param _high_volt: user inputted value, should be an integer that will be the upper level of the triangle wave
        :param _freq: user inputted value, should be a float that will be the rate of change of the triangle wave
        :param _master: main window of the program, used so that the operational parameters of the main window
         can be changed
        :return: the parameters are updated in the main windows operational_params dictionary
        """
        #save the voltage and frequency parameters to the current instance so they don't have to passed all the time
        # to the functions
        self._low_volt = _low_volt
        self._high_volt = _high_volt
        self._freq = _freq

        changing_flag = True  # flag to turn off if for any reason the cyclic voltammetry settings should not be changed

        # try to convert the voltages to integers and sweep rate to a float
        try:
            self._low_volt = int(self._low_volt)
            self._high_volt = int(self._high_volt)
            self._freq = float(self._freq)
        except ValueError:
            print "Error in data input format"
            changing_flag = False  # if the inputted data is not correct, change the flag so that the program will
                                   # no try to send bad data to the MCU

        # check for changes to any of the values, do not bother the amplifier if there is no update
        if self.is_changed(_master.operation_params):

            #make sure the lower amplitude is lower than the high amplitude and that there were no errors from the user
            if (self._low_volt < self._high_volt) and changing_flag:
                self.send_settings()
                self.change_saved_settings(_master)
            else:
                print "no change of settings low > high"
        else:
            print "no change of settings"

        self.destroy()

    def is_changed(self, _old_params):
        """
        Check to see if any of the parameters of the cyclic voltammetry have been changed
        :param _old_params:
        :return:
        """
        if (self._low_volt != _old_params['low_cv_voltage'] or self._high_volt != _old_params['high_cv_voltage'] or
                    self._freq != _old_params['sweep_rate']):
            print "is_changed"
            return True
        else:
            return False

    def send_settings(self):
        """
        Convert the input voltages 11 bit numbers to set the parallel current digital to analog converters (PIDACs)
        version 0.1: PIDACs are running on 11 bits with a maximum of 255 uA of current through a fixed 8.2 kohms
        resistor with the output buffered by a voltage following opamp

        The voltage out of the DAC is given by the equation Vout = 8200 ohms * 255 uA * (D / 2**11)
        where D is the integer set by the microcontroller

        to set D use the equation D = (Vout * 2*11) / (8200 ohms * 255 uA)

        TODO: FIX THIS SECTION WHEN THE MCU SIDE IS MORE SET

        :param _low_volt: integer (mV), lowest voltage of the triangle sweep to be given
        :param _high_volt: integer (mV), highest voltage of the triangle
        :param _freq: float (V/s), rate that the voltage of the triangle wave changes
        :return:
        """
        resistor = 8200  # ohms
        max_current = .255  # mA
        _lower_setting = int(( (self._low_volt+1024) * 2**11) / (resistor*max_current))  # mv/(ohms*mA) = mV/mV
        _upper_setting = int(( (self._high_volt+1024) * 2**11) / (resistor*max_current))  # mv/(ohms*mA) = mV/mV
        _range = _upper_setting - _lower_setting
        _data_points = 2 * _range - 1

        # changing the DACs by 1 bit chnages the voltage by 1 mV,
        # therefor the voltage should be stepped 1000 mV/V * rate (V/s)

        _freq_setting = int(round(1000 * self._freq))  #  NOT CORRECT, FIGURE THIS OUT ON MCU SIDE

        print "sending"
        print "S|{0:04d}|{1:04d}|{2:06d}".format(_lower_setting, _upper_setting, _freq_setting)



    def change_saved_settings(self, _master):

        print "change saved settings called"

        _master.operation_params['low_cv_voltage'] = self._low_volt
        _master.operation_params['high_cv_voltage'] = self._high_volt
        _master.operation_params['sweep_rate'] = self._freq

        print _master.operation_params

