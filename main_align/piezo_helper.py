#edit version with increment

import serial
import sys
import re
import time

DEFAULT_PORT = 'COM3'

class PZT_driver(serial.Serial):
    def __init__(self, port=DEFAULT_PORT, baudrate=115200):
        serial.Serial.__init__(self,port, baudrate, timeout=0.1)
        self.xyz = [0,0,0]
        self.set_zero()

    def set_value(self, cmd, val):
        self.write(str.encode('%s%f\r'%(cmd,val)))
        
    def mon_readline(self):
        """ Reads a line which finish by '/r' or until time out"""
        a=self.read()
        if a=='':
            return ''
        while a[-1]!='\r':
            s=self.read()
            a=a+s
            if s=='':
                break
        return a

    def read_txt(self, cmd):
        """Send a command, and return the output of the command as a string"""
        self.write(cmd+'\r')
        s = self.mon_readline()
        a1 = re.search('\[(.*)\]',s)
        a2 = re.search('\*([0-9\.]+\Z)',s)
        while a1 is None and a2 is None and s!='':
            s = self.mon_readline()
            a1 = re.search('\[(.*)\]',s)
            a2 = re.search('\*([0-9\.]+\Z)',s)
        if a1 is not None:
            return a1.group(1)
        elif a2 is not None:
            return a2.group(1)
        else:
            raise Exception('No information return from command %s'%(cmd))
    
    def read_float(self, cmd):
        """Send a command, and return the result as a float"""
        s = self.read_txt(cmd)
        return float(s)

    def get_all(self):
        """Returns list [x, y, z] of the output voltages"""
        return self.xyz

    def get_x(self):
        """Reads and returns the x axis output voltage"""
        #return self.read_float('xr?')
        return self.xyz[0]

    def get_y(self):
        """Reads and returns the y axis output voltage"""
        #return self.read_float('yr?')
        return self.xyz[1]

    def get_z(self):
        """Reads and returns the z axis output voltage"""
        #return self.read_float('zr?')
        return self.xyz[2]

    def set_all(self, val):
        """Sets all outputs to the set voltage"""
        self.xyz = [0, 0, 0]
        self.set_value('AV', val)

    def set_x(self, val):
        """Sets the output voltage for the x axis"""
        self.xyz[0] = val
        self.set_value('XV', val)

    def set_y(self, val):
        """Sets the output voltage for the y axis"""
        self.xyz[1] = val
        self.set_value('YV', val)

    def set_z(self, val):
        """Sets the output voltage for the z axis"""
        self.xyz[2] = val
        self.set_value('ZV', val)

    def set_zero(self):
        """ Sets all outputs to zero"""
        self.set_all(0)
    
    def increment_x(self, val):
        self.set_x(self.x + val)
        self.x += val

    def increment_y(self, val):
        self.set_y(self.y + val)
        self.y += val
    
    def increment_z(self, val):
        self.set_z(self.z + val)
        self.z += val

    @property
    def max_out(self):
        """returns the output voltage limit setting"""
        return self.read_float('%\r')

    def get_info(self):
        """Return the product header, firmware version, etc."""
        self.write('i\r')
        return self.readlines()[0].replace('\r','\n')
    
    def set_x_min(self, val):
        """Sets the minimum output voltage limit for the x axis"""
        self.set_value('XL',val)
        
    def set_y_min(self, val):
        """Sets the minimum output voltage limit for the y axis"""
        self.set_value('YL',val)   
        
    def set_z_min(self, val):
        """Sets the minimum output voltage limit for the z axis"""
        self.set_value('ZL',val)  
 
    def get_x_min(self):
        """Return the minimum output voltage limit for the x axis"""
        return self.read_float('xl?')

    def get_y_min(self):
        """Return the minimum output voltage limit for the y axis"""
        return self.read_float('yl?')   
   
    def get_z_min(self):
        """Return the minimum output voltage limit for the z axis"""
        return self.read_float('zl?') 

    def set_x_max(self, val):
        """Sets the maximum output voltage limit for the x axis"""
        self.set_value('xh',val)
        
    def set_y_max(self, val):
        """Sets the maximum output voltage limit for the y axis"""
        self.set_value('yh',val)   
        
    def set_z_max(self, val):
        """Sets the maximum output voltage limit for the z axis"""
        self.set_value('zh',val)
        
    def get_x_max(self):
        """Return the maximum output voltage limit for the x axis"""
        return self.read_float('xh?')

    def get_y_max(self):
        """Return the maximum output voltage limit for the y axis"""
        return self.read_float('yh?')   
   
    def get_z_max(self):
        """Return the maximum output voltage limit for the z axis"""
        return self.read_float('zh?') 


    x = property(get_x, set_x)
    y = property(get_y, set_y)
    z = property(get_z, set_z)
    
    all = property(get_all, set_all)

    x_min = property(get_x_min, set_x_min)
    y_min = property(get_y_min, set_y_min)
    z_min = property(get_z_min, set_z_min)
    
    x_max = property(get_x_max, set_x_max)
    y_max = property(get_y_max, set_y_max)
    z_max = property(get_z_max, set_z_max)
    
    def shift_pixel(self, pixels, ratio = 1):
        self.y += pixels * ratio
        print('piezo shifted ' + str(pixels * ratio))

    def __del__(self):
        # close the serial port before deleting the object
        self.close()


#test functions
if __name__ == "__main__":
    pzt = PZT_driver()
    print(pzt.all)
    time.sleep(5)
    pzt.set_x(30)
    pzt.y = 10
    print(pzt.all)
    time.sleep(5)
    pzt.increment_x(10)
    print(pzt.all)

