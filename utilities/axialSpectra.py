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
dataSets = np.array([np.loadtxt('axialPhononRuns/run4_'+str(r)+'.dat')
    for r in range(0,2000,1)])
spectra = np.abs((np.fft.fft(dataSets[:,2],axis=0)))**2
psd=np.sum(spectra, axis=1)
psd=psd[:psd.size/2]+psd[:psd.size/2-1:-1]
frequencies=1.0e-6*np.arange(0,0.5/dt,0.5/dt/psd.size)
plt.semilogy(frequencies, psd, 'g', lw=1.0)

dataSets = np.array([np.loadtxt('axialPhononRuns/run3_'+str(r)+'.dat')
    for r in range(0,2000,1)])
spectra = np.abs((np.fft.fft(dataSets[:,2],axis=0)))**2
psd=np.sum(spectra, axis=1)
psd=psd[:psd.size/2]+psd[:psd.size/2-1:-1]
frequencies=1.0e-6*np.arange(0,0.5/dt,0.5/dt/psd.size)
plt.semilogy(frequencies, psd,'b', lw=1.5)

plt.gcf().subplots_adjust(left = 0.2, bottom = 0.20, top=0.95, right=0.95)
plt.xlabel(r'$\nu/{\rm MHz}$')
plt.ylabel(r'$S_z(\nu)$')
#plt.ylim([2.0e-11,4.0e-10])
plt.savefig('axialSpectra.pdf')


plt.clf()
dataSets = np.array([np.loadtxt('axialPhononRuns/run4_'+str(r)+'.dat')
    for r in range(0,2000,1)])
spectra = np.abs((np.fft.fft(dataSets[:,2],axis=0)))**2
psd=np.sum(spectra, axis=1)
psd=psd[:psd.size/2]+psd[:psd.size/2-1:-1]
frequencies=1.0e-6*np.arange(0,0.5/dt,0.5/dt/psd.size)
plt.semilogy(frequencies, psd, 'g', lw=1.0)

dataSets = np.array([np.loadtxt('axialPhononRuns/run3_'+str(r)+'.dat')
    for r in range(0,2000,1)])
spectra = np.abs((np.fft.fft(dataSets[:,2],axis=0)))**2
psd=np.sum(spectra, axis=1)
psd=psd[:psd.size/2]+psd[:psd.size/2-1:-1]
frequencies=1.0e-6*np.arange(0,0.5/dt,0.5/dt/psd.size)
plt.semilogy(frequencies, psd,'b', lw=1.5)

plt.gcf().subplots_adjust(left = 0.2, bottom = 0.20, top=0.95, right=0.95)
plt.xlabel(r'$\nu/{\rm MHz}$')
plt.ylabel(r'$S_z(\nu)$')
#plt.ylim([2.0e-11,4.0e-10])
plt.xlim([0.75,0.81])
plt.savefig('axialSpectraZoomedIn.pdf')

