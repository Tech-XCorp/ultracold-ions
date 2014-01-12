import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig_width_pt = 8.0*72/2.54  # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = fig_width 
fig_size =  [fig_width,fig_height]

params = {'backend': 'ps',
    'axes.labelsize': 10,
    'text.fontsize': 10,
    'legend.fontsize': 6,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'text.usetex': True,
    'figure.figsize': fig_size}

plt.rcParams.update(params)

baseName = 'runs/run12_'
suffix = '.dat'

def rotate(xy, phase):
    return np.array([
            xy[0] * np.cos(phase) - xy[1] * np.sin(phase),
            xy[0] * np.sin(phase) + xy[1] * np.cos(phase)
            ])

def computeMobility(t, dphi, base, suff):
  data0 = np.loadtxt(base + str(t) + suff)
  data1 = np.loadtxt(base + str(t + 1) + suff)
  rdata1 = rotate(data1, -dphi)
  dxy = np.linalg.norm(rdata1[:2] - data0[:2])
  dz = np.linalg.norm(data1[2] - data0[2])
  return np.sqrt((dxy**2 + dz**2) / data0.shape[1])

def computeMobilityZ(t, base, suff):
  data0 = np.loadtxt(base + str(t) + suff)
  data1 = np.loadtxt(base + str(t + 1) + suff)
  return np.linalg.norm(data0[2] - data1[2]) / np.sqrt(data0.shape[1])

def computeMobilityXY(t, dphi, base, suff):
  data0 = np.loadtxt(base + str(t) + suff)
  data1 = np.loadtxt(base + str(t + 1) + suff)
  rdata1 = rotate(data1, -dphi)
  return np.linalg.norm(data0[:2] - rdata1[:2]) / np.sqrt(data0.shape[1])

dt = 1.0e-5
kHz = 1.0e3
frequency = 44 * kHz
dphi = dt * frequency * 2 * np.pi
nMin = 0
nMax = 2
di = 1
plt.plot(1.0e3 * dt * np.arange(nMin, nMax, di),
    [1.0e6*computeMobilityXY(t, dphi, baseName, suffix) 
    for t in range(nMin, nMax, di)])
plt.plot(1.0e3 * dt * np.arange(nMin, nMax, di),
    [1.0e6*computeMobilityZ(t, baseName, suffix) 
    for t in range(nMin, nMax, di)])
plt.xlabel(r'$t/{\rm ms}$')
plt.ylabel(r'$\sqrt{\Delta x^2 + \Delta y^2}/\mu{\rm m},\,\Delta y/\mu{\rm m}$')
plt.gcf().subplots_adjust(left = 0.2, bottom = 0.20, top=0.95,
  right=0.95)
plt.savefig('mobilities2.pdf') 

# vi sw=4 ts=4
