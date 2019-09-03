import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Plot3D:
    def __init__(self,f : np.ndarray):
        self.t = 0
        self.f = f
        self.fig = plt.figure()
        self.ax = plt.axes(projection="3d")

    def onclick(self,event):
        nt = 0
        try:
            nt = int(event.key)
        except Exception :
            return
        plt.cla()
        print(self.t)
        self.t = int((nt/10.0) * self.f.shape[0])
        z_line = self.f[self.t]
        X = np.array(range(0,self.f.shape[1]))
        Y = np.array(range(0,self.f.shape[2]))
        X, Y = np.meshgrid(X, Y)
        self.ax.plot_surface(X, Y, z_line)
        plt.draw()
        



    
    def Draw(self):
        self.e = self.fig.canvas.mpl_connect('key_press_event', self.onclick)
        plt.show()