import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig_width_pt = 8.0*72/2.54  # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (np.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = fig_width*golden_mean      # height in inches
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

vz = np.loadtxt('vzOfT.dat')
t = np.linspace(0, 499*1.0e-6*10, 500)
for v in np.transpose(vz):
  plt.plot(t, v)
plt.xlabel(r'$t/s$')
plt.ylabel(r'$v_z/({\rm m}/{\rm s})$')
plt.gcf().subplots_adjust(left = 0.15, bottom = 0.20, top=0.95,
  right=0.95)
plt.savefig('freeSpaceCooling.pdf')


