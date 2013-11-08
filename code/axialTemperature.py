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
    'text.fontsize': 10,
    'legend.fontsize': 8,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'text.usetex': True,
    'figure.figsize': fig_size}

plt.rcParams.update(params)

kz = 2.0 * 1.167e6
kB = 1.38e-23

def axialKineticEnergy(data):
    return 0.5 * data[7] * data[5]**2
def axialEnergy(data):
    return 0.5 * kz * data[6] * data[2]**2 + 0.5 * data[7] * data[5]**2

def radius(data):
    return np.sqrt(data[0]**2+data[1]**2)


def radiallySorted(radii, data):
    zippedData = np.transpose(np.array([radii, data]))
    return np.transpose(np.sort(zippedData,axis=0))

plt.clf()
r=10
data = np.loadtxt('axialPhononRuns/run5_'+str(r)+'.dat')
sortedData=radiallySorted(1.0e6*radius(data),axialKineticEnergy(data)/(1.0e-3*kB))
plt.semilogy(sortedData[0],sortedData[1],'-o',markersize=2.0)
#thePower=8
#plt.plot(sortedData[0],sortedData[0]**thePower*(5/1.8e2**thePower))
plt.gcf().subplots_adjust(left = 0.2, bottom = 0.20, top=0.95, right=0.95)
plt.xlabel(r'$r/\mu{\rm m}$')
plt.ylabel(r'$2 E_z/({\rm mK}\; k_B)$')
plt.ylim([-0.01,5.0])
plt.savefig('axialKineticTemperature.pdf')

