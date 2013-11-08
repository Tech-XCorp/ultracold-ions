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

scanNumber = 2

dOmega = 0.1e3 * 2 * np.pi
omegaMax = 55.0e3 * 2 * np.pi
omegaMin = 41.1e3 * 2 * np.pi
omegas = np.arange(omegaMin, omegaMax, dOmega)
def loadPtcls(filename):
    return np.loadtxt(filename)

def buildFileName(path, basename, omega, suffix):
    return path + basename + str(omega / 2 / np.pi) + suffix

directory='frequencyScan/nptcls127/'
baseName='scan'+str(scanNumber)+'_'
suffix='.dat'
dataSets=[loadPtcls(buildFileName(directory, baseName, omega, suffix)) for omega in omegas]

def thickness(ptcls):
    return np.std(ptcls[2])

plt.clf()
#plt.plot(1.0e-3 * omegas / 2.0 / np.pi, 1.0e6 * np.array(map(thickness, dataSets)))
plt.xlabel(r"$\Omega/(2\pi \times {\rm kHz})$")
plt.ylabel(r"$\Delta z/\mu {\rm m}$")
plt.gcf().subplots_adjust(left = 0.15, bottom = 0.2, top=0.95, right=0.95)

#scanNumber = 1
#directory='frequencyScan/nptcls127/'
#baseName='scan'+str(scanNumber)+'_'
#suffix='.dat'
#dOmega = 0.1e3 * 2 * np.pi
#omegaMax = 55.0e3 * 2 * np.pi
#omegaMin = 42.0e3 * 2 * np.pi
#omegas = np.arange(omegaMin, omegaMax, dOmega)
#dataSets=[loadPtcls(buildFileName(directory, baseName, omega, suffix)) for omega in omegas]
#plt.plot(1.0e-3 * omegas / 2.0 / np.pi, 1.0e6 * np.array(map(thickness, dataSets)))
#
#scanNumber = 3
#directory='frequencyScan/nptcls127/'
#baseName='scan'+str(scanNumber)+'_'
#suffix='.dat'
#dOmega = 0.1e3 * 2 * np.pi
#omegaMax = 55.0e3 * 2 * np.pi
#omegaMin = 41.5e3 * 2 * np.pi
#omegas = np.arange(omegaMin, omegaMax, dOmega)
#dataSets=[loadPtcls(buildFileName(directory, baseName, omega, suffix)) for omega in omegas]
#plt.plot(1.0e-3 * omegas / 2.0 / np.pi, 1.0e6 * np.array(map(thickness, dataSets)))
#
#scanNumber = 4
#directory='frequencyScan/nptcls127/'
#baseName='scan'+str(scanNumber)+'_'
#suffix='.dat'
#dOmega = 0.1e3 * 2 * np.pi
#omegaMax = 55.0e3 * 2 * np.pi
#omegaMin = 41.5e3 * 2 * np.pi
#omegas = np.arange(omegaMin, omegaMax, dOmega)
#dataSets=[loadPtcls(buildFileName(directory, baseName, omega, suffix)) for omega in omegas]
#plt.plot(1.0e-3 * omegas / 2.0 / np.pi, 1.0e6 * np.array(map(thickness, dataSets)))

scanNumber = 5
directory='frequencyScan/nptcls127/'
baseName='scan'+str(scanNumber)+'_'
suffix='.dat'
dOmega = 0.1e3 * 2 * np.pi
omegaMax = 55.0e3 * 2 * np.pi
omegaMin = 41.5e3 * 2 * np.pi
omegas = np.arange(omegaMin, omegaMax, dOmega)
dataSets=[loadPtcls(buildFileName(directory, baseName, omega, suffix)) for omega in omegas]
plt.plot(1.0e-3 * omegas / 2.0 / np.pi, 1.0e6 * np.array(map(thickness, dataSets)))
plt.ylim([-0.5,8])

plt.savefig("thicknessVsOmega.pdf")

