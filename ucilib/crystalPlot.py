import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig_width_pt = 8.0*72/2.54  # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = fig_width * 1.5 # height in inches
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

data = 1.0e3 * np.loadtxt('crystal.dat')

plt.figure(1)
plt.subplot(211)
plt.plot(data[0], data[1], 'bo', ms=2)
plt.xlabel(r'$x/{\rm mm}$')
plt.ylabel(r'$y/{\rm mm}$')
plt.subplot(212)
plt.plot(data[0], data[2], 'bo', ms=2)
plt.xlabel(r'$x/{\rm mm}$')
plt.ylabel(r'$z/{\rm mm}$')
plt.subplots_adjust(left=0.22, bottom=0.08, right = 0.95, top = 0.95)
plt.savefig("crystal.pdf")

