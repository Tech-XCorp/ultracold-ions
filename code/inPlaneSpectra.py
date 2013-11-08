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
dt = 5.0e-7

plt.clf()

def rotate(xy, phase):
    return np.array([
            xy[0] * np.cos(phase) - xy[1] * np.sin(phase),
            xy[0] * np.sin(phase) + xy[1] * np.cos(phase)
            ])

dt = 0.5e-6
kHz = 1.0e3
frequency = 44.00 * kHz
theta0 = 0
nMin = 0  
nMax = 2000
di = 1

dataSets = np.array([np.loadtxt('axialPhononRuns/run3_'+str(r)+'.dat')
    for r in range(nMin,nMax,di)])
rotatingFrameData = np.array([rotate(dataSets[i,:2],
            -(i + nMin) * dt * 2 * np.pi * frequency - theta0) 
    for i in range(nMax - nMin)])
spectra = np.abs((np.fft.fft(rotatingFrameData[:,1],axis=0)))**2
psd=np.sum(spectra, axis=1)
psd=psd[:psd.size/2]+psd[:psd.size/2-1:-1]
frequencies=1.0e-6*np.arange(0,0.5/dt,0.5/dt/psd.size)
plt.semilogy(frequencies, psd)


plt.gcf().subplots_adjust(left = 0.2, bottom = 0.20, top=0.95, right=0.95)
plt.xlabel(r'$\nu/{\rm MHz}$')
plt.ylabel(r'$S_x(\nu)$')
#plt.ylim([2.0e-11,4.0e-10])
plt.savefig('inPlaneSpectra.pdf')


