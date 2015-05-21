import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def get_data(i):
    return np.load('ptcls' + str(i) + '.npy')

def in_range(lx, position):
    return position[0] < lx and position[0] > -lx and position[1] < lx and position[1] > -lx and position[2] < lx and position[2] > -lx


def plot_data_3d(i, lx = 2.0e-4, show_electrons=False):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim3d(-lx, lx)
    ax.set_ylim3d(-lx, lx)
    ax.set_zlim3d(-lx, lx)
    data = get_data(i)
    n_ions = data.shape[1]/2
    ions = data[0:3,n_ions:]
    ions_in_range = ions[:,np.where([in_range(lx, ions[:,i]) for i in range(n_ions)])]
    electrons = data[0:3,n_ions:]
    electrons_in_range = electrons[:,np.where([in_range(lx, electrons[:,e]) for e in range(n_ions)])]
    if show_electrons:
        ax.scatter(electrons_in_range[0],electrons_in_range[1],electrons_in_range[2],c='r',marker='.',s=5,lw=0)
    ax.scatter(ions_in_range[0],ions_in_range[1],ions_in_range[2],c='b',marker='.',s=10,lw=0)
    plt.show()

def plot_data(i, lx = 2.0e-4, show_electrons=False):
    data = get_data(i)
    n_ions = data.shape[1]/2
    ions = data[0:3,:n_ions]
    #ions_in_range = ions[:,np.where([in_range(lx, ions[:,i]) for i in range(n_ions)])]
    ions_in_range = ions
    electrons = data[0:3,n_ions:]
    electrons_in_range = electrons[:,np.where([in_range(lx, electrons[:,e]) for e in range(n_ions)])]
    if show_electrons:
        plt.plot(electrons_in_range[0],electrons_in_range[1],c='r',marker='.',ms=5,lw=0)
    plt.plot(ions_in_range[0],ions_in_range[1],c='b',marker='.',ms=10,lw=0)
    plt.show()

