import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig_width_pt = 8.0*72/2.54  # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = 0.6 * fig_width 
fig_size =  [fig_width,fig_height]

params = {'backend': 'ps',
    'axes.labelsize': 10,
    'text.fontsize': 8,
    'legend.fontsize': 8,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'text.usetex': True,
    'figure.figsize': fig_size}

plt.rcParams.update(params)

def getXRZData(filename):
    data = np.loadtxt(filename)
    return np.array([np.sqrt(data[0]**2+data[1]**2), data[0], data[2]])


def buildFileName(path, basename, omega, suffix):
    return path + basename + str(omega / 2 / np.pi) + suffix

scanNumber=5
path='frequencyScan/nptcls127/'
baseName='scan'+str(scanNumber)+'_'
suffix='.dat'


omegas = 2.0 * np.pi * 1.0e3 * np.arange(45.0, 55.0, 1.0)

def sideViewPlot(dataset):
    plt.plot(1.0e6*dataset[1],1.0e6*dataset[2],'o',markersize=2.5)

plt.clf()
axes=[]
for i,omega in enumerate(omegas[:6]):
    axes.append(plt.subplot(3,2,i+1))
    sideViewPlot(getXRZData(buildFileName(path, baseName,omega,suffix)))
    if (i % 2 != 0):
        plt.setp(axes[i].get_yticklabels(), visible=False)
    else:
        plt.ylabel(r'$z/\mu {\rm m}$')
    if (i / 2 != 2):
        plt.setp(axes[i].get_xticklabels(), visible=False)
    else:
        plt.xlabel(r'$x/\mu {\rm m}$')
    plt.xticks([-100,0,100])
    plt.yticks([-10,0,10])
    plt.xlim([-170,170])
    plt.ylim([-15,20])
    plt.text(0.1,0.85,r'$\Omega='+str(omega/2/np.pi/1.0e3)+r'\times 2\pi {\rm kHz}$',
        horizontalalignment='left',
        verticalalignment='center',
        transform=axes[i].transAxes,
        fontsize=8)


plt.gcf().subplots_adjust(left=0.16,bottom=0.12,top=0.95,right=0.95,wspace=0.05,hspace=0.03)
plt.gcf().set_size_inches(8/2.54, 8/2.54)

plt.savefig('sideViews.pdf')



