__author__ = 'Kyle V. Lopin'

import usb.core
import usb.util



class amp_usb(object):
    """
    Generic class that deals with the usb communication to an PSOC configured as an amperometric device
    """
    def __init__(self, vendor_id=None, product_id=None):
        """
        Initialize a communication channel to a PSOC with a USBFS module.  The default example for the USBFS HID example
        is set if no vendor or product id are inputted

        :param vendor_id: the USB vendor id, used to identify the proper device connected to the computer
        :param product_id: the USB product id
        :return:
        """
        if not vendor_id:
            vendor_id = 0x04B4
        if not product_id:
            product_id = 0xE177
        self.connect_usb(vendor_id, product_id)





    def connect_usb(self, _vendor_id, _product_id):
        """
        Attempt to connect to the PSoC device with a USBFS module
        If the device is not found return None

        This method uses the pyUSB module, see the tutorial example at:
        https://github.com/walac/pyusb/blob/master/docs/tutorial.rst
        for more details

        TODO: print statements to a log file with time stamps

        :return:
        """
        # attempt to find the PSoC amperometry device
        amp_device = usb.core.find(idVendor=_vendor_id, idProduct=_product_id)

        # if no device is found, print a warning to the output
        if amp_device is None:
            print ValueError("Device not found")
            return None
        else:  # if a device is found print that it was found
            print "PSoC amp found"

        # set the active configuration.  they pyUSB module deals with the details
        amp_device.set_configuration()

        # with the device active, get the endpoints.
        # See Cypress's document AN57294 - USB 101: An Introduction to Universal Serial Bus 2.0 for details about
        # general USB protocols
        cfg = amp_device.get_active_configuration()
        intf = cfg[(0,0)]

        ep_out = usb.util.find_descriptor(intf, custom_match=
                                          lambda e: usb.util.endpoint_direction(e.bEndpointAddress) ==
                                          usb.util.ENDPOINT_OUT)

        ep_in = usb.util.find_descriptor(intf, custom_match=
                                         lambda e: usb.util.endpoint_direction(e.bEndpointAddress) ==
                                         usb.util.ENDPOINT_IN)
        # return the device and endpoints if the exist or None if no device is found
        return amp_device, ep_out, ep_in
