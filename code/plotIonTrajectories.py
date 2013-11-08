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

baseName = 'axialPhononRuns/run3_'
suffix = '.dat'
nMin = 0  
nMax = 10000
di = 100
data = np.array([np.loadtxt(baseName + str(i) + suffix) for i in
    range(nMin, nMax)])

def rotate(xy, phase):
    return np.array([
            xy[0] * np.cos(phase) - xy[1] * np.sin(phase),
            xy[0] * np.sin(phase) + xy[1] * np.cos(phase)
            ])

dt = 1.0e-6
kHz = 1.0e3
frequency = 44.00 * kHz
#theta0 = frequency * 2 * np.pi * dt
theta0 = 0
rotatingFrameData = np.array([rotate(data[i,:2],
            -(i + nMin) * dt * 2 * np.pi * frequency - theta0) 
    for i in range(nMax - nMin)])

plt.clf()
[plt.plot(1.0e6 * rotatingFrameData[0:-1:di,0,p], 1.0e6 *
    rotatingFrameData[0:-1:di,1,p], 'k', linewidth = 0.5) 
  for p in range(127)]
[plt.plot(1.0e6 * rotatingFrameData[0,0,p], 1.0e6 *
    rotatingFrameData[0,1,p], 'og', markersize = 1) 
  for p in range(127)]
[plt.plot(1.0e6 * rotatingFrameData[-1,0,p], 1.0e6 *
    rotatingFrameData[-1,1,p], 'or', markersize = 1.5) 
  for p in range(127)]

#plt.plot([-300,300],[0,0],'k--')


plt.xlabel(r'$x/\mu{\rm m}$')
plt.ylabel(r'$y/\mu{\rm m}$')
plt.gcf().subplots_adjust(left = 0.2, bottom = 0.2, top=0.99,
  right=0.98)
plt.axes().set_aspect('equal')
plt.xlim([-260, 260])
plt.ylim([-260, 260])

plt.savefig('tmp.pdf')

#baseName = 'runs/run2_'
#suffix = '.dat'
#nMin = 505
#nMax = 507
#data = np.array([np.loadtxt(baseName + str(i) + suffix) for i in
#    range(nMin, nMax)])
#
#def rotate(xy, phase):
#    return np.array([
#            xy[0] * np.cos(phase) - xy[1] * np.sin(phase),
#            xy[0] * np.sin(phase) + xy[1] * np.cos(phase)
#            ])
#
#dt = 1.0e-5
#kHz = 1.0e3
#frequency = 44.10875 * kHz
#rotatingFrameData = np.array([rotate(data[i,:2],
#            -i * dt * 2 * np.pi * frequency) for i in range(nMax - nMin)])
#
#plt.clf()
#[plt.plot(1.0e6 * rotatingFrameData[0,0,p], 1.0e6 *
#    rotatingFrameData[0,1,p], 'ok', markersize = 2.5) 
#  for p in range(127)]
#[plt.plot(1.0e6 * rotatingFrameData[-1,0,p], 1.0e6 *
#    rotatingFrameData[-1,1,p], 'or', markersize = 2.5) 
#  for p in range(127)]
#[plt.plot(1.0e6 * rotatingFrameData[:,0,p], 1.0e6 *
#    rotatingFrameData[:,1,p], 'b', linewidth = 1.0) 
#  for p in range(127)]
#
#
#plt.xlabel(r'$x/\mu{\rm m}$')
#plt.ylabel(r'$y/\mu{\rm m}$')
#plt.gcf().subplots_adjust(left = 0.2, bottom = 0.20, top=0.95,
#  right=0.95)
#plt.axes().set_aspect('equal')
#
#plt.savefig('rearrangement.pdf')

#baseName = 'runs/run1_'
#suffix = '.dat'
#nMax = 800
#data = np.array([np.loadtxt(baseName + str(i) + suffix) for i in
#    range(nMax)])
#
#def rotate(xy, phase):
#    return np.array([
#            xy[0] * np.cos(phase) - xy[1] * np.sin(phase),
#            xy[0] * np.sin(phase) + xy[1] * np.cos(phase)
#            ])
#
#dt = 1.0e-5
#kHz = 1.0e3
#frequency = 44.115* kHz
#rotatingFrameData = np.array([rotate(data[i,:2],
#            -i * dt * 2 * np.pi * frequency) for i in range(nMax)])
#
#plt.clf()
#tstart=500
#tend=600
#[plt.plot(1.0e6 * rotatingFrameData[tstart,0,p], 1.0e6 *
#    rotatingFrameData[tstart,1,p], 'ok', markersize = 2.5) 
#  for p in range(127)]
#[plt.plot(1.0e6 * rotatingFrameData[tstart:tend,0,p], 1.0e6 *
#    rotatingFrameData[tstart:tend,1,p], 'b', linewidth = 0.3) 
#  for p in range(127)]
#
#
#plt.xlabel(r'$x/\mu{\rm m}$')
#plt.ylabel(r'$y/\mu{\rm m}$')
#plt.gcf().subplots_adjust(left = 0.2, bottom = 0.20, top=0.95,
#  right=0.95)
#plt.axes().set_aspect('equal')
#
#plt.savefig('rearrangement.pdf')

# vi sw=4 ts=4
