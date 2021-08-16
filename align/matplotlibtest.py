import numpy as np
import matplotlib.pyplot as plt

x = np.arange(-10,10)
y = x**2

fig = plt.figure(3)
ax = fig.add_subplot(111)
ax.plot(x,y)

print('1')

coords = []

def onclick(event):
    global ix, iy
    ix, iy = event.xdata, event.ydata
    print ('x = %d, y = %d'%(
        ix, iy))

    global coords
    coords.append((ix, iy))

    if len(coords) == 2:
        fig.canvas.mpl_disconnect(cid)
        plt.close(3)
        print('finished')

    return coords
cid = fig.canvas.mpl_connect('button_press_event', onclick)
print(cid)
print('2')
plt.show()
print('3')
print(coords)