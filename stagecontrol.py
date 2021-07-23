import serial
import sys
import re


DEFAULT_PORT = 'COM3'


class PZT_driver(serial.Serial):
    def __init__(self, port=DEFAULT_PORT, baudrate=115200, ):
        serial.Serial.__init__(self,port, baudrate, timeout=0.1)
        #self.set_zeros()
        
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_z(self):
        return self.z

    def set_value(self, cmd, val):
        self.write(str.encode('%s%f\r'%(cmd,val)))
    
    def set_all(self, val):
        """Sets all outputs to the set voltage"""
        self.set_value('AV', val)
        self.x = val
        self.y = val
        self.x = val

    def set_x(self, val):
        """Sets the output voltage for the x axis"""
        self.set_value('XV', val)
        self.x = val

    def set_y(self, val):
        """Sets the output voltage for the y axis"""
        self.set_value('YV', val)
        self.y = val

    def set_z(self, val):
        """Sets the output voltage for the z axis"""
        self.set_value('ZV', val)
        self.z = val

    def set_zeros(self):
        """ Sets all outputs to zero"""
        self.set_all(0)
    
    def increment_x(self, shift):
        self.set_x(self.x + shift)
    
    def increment_y(self, shift):
        self.set_y(self.y + shift)
    
    def increment_z(self, shift):
        self.set_z(self.z + shift)

    x = property(get_x, set_x)
    y = property(get_y, set_y)
    z = property(get_z, set_z)
    
    all = property(lambda self:None, set_all)

    def __del__(self):
        # close the serial port before deleting the object
        self.close()

mdt = PZT_driver()
mdt.x = 20