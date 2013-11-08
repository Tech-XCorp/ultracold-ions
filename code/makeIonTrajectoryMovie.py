import numpy as np
import matplotlib.pyplot as plt

fig_width = 6.0 
fig_height = 4.0 
fig_size =  [fig_width,fig_height]

params = {'backend': 'ps',
    'axes.labelsize': 16,
    'text.fontsize': 16,
    'legend.fontsize': 6,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'text.usetex': True,
    'figure.figsize': fig_size}

plt.rcParams.update(params)

baseName = 'axialPhononRuns/run3_'
suffix = '.dat'
nMin = 0  
nMax = 2000
data = np.array([np.loadtxt(baseName + str(i) + suffix) for i in
    range(nMin, nMax)])

def rotate(xy, phase):
    return np.array([
            xy[0] * np.cos(phase) - xy[1] * np.sin(phase),
            xy[0] * np.sin(phase) + xy[1] * np.cos(phase)
            ])

dt = 5.0e-7
kHz = 1.0e3
frequency = 44 * kHz
theta0 = 0
rotatingFrameData = np.array([rotate(data[i,:2],
            -(i + nMin) * dt * 2 * np.pi * frequency - theta0) 
    for i in range(nMax - nMin)])

def makeFrame(i, di):
  plt.clf()
  [plt.plot(1.0e6 * rotatingFrameData[0:i:di,0,p], 1.0e6 *
      rotatingFrameData[0:i:di,1,p], 'k', linewidth = 1.0) 
    for p in range(127)]
  [plt.plot(1.0e6 * rotatingFrameData[0,0,p], 1.0e6 *
      rotatingFrameData[0,1,p], 'og', markersize = 5) 
    for p in range(127)]
  [plt.plot(1.0e6 * rotatingFrameData[i,0,p], 1.0e6 *
      rotatingFrameData[i,1,p], 'or', markersize = 5) 
    for p in range(127)]
  plt.xlabel(r'$x/\mu{\rm m}$')
  plt.ylabel(r'$y/\mu{\rm m}$')
  plt.gcf().subplots_adjust(left = 0.15, bottom = 0.08, top=0.99,
    right=0.98)
  plt.axes().set_aspect('equal')
  plt.xlim([-260, 260])
  plt.ylim([-160, 160])
  plt.savefig('frame_%05d.png'%(i/di))

di = 10
for i in range(nMax / di):
  makeFrame(i * di, di)


# vi sw=4 ts=4
