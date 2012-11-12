#! /usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np

n = 10
xdata = np.linspace(0, 2*np.pi, n)
ydata = [np.sin(x) for x in xdata] 

plt.plot(xdata, ydata, label="Cyclus Total")
plt.axis([min(xdata),max(xdata),min(ydata),max(ydata)])
plt.legend(loc=2)
plt.title('Reactor Deployment Aggregated by Year')
plt.xlabel('Year')
plt.ylabel('Number of Currently Deployed Reactors')
plt.show()
plt.savefig('rxtrs.png')
plt.clf()
