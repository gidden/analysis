import sys
sys.path.append('../src')

import matplotlib.pyplot as plt
import vision_data as vd
import utility as u
import queries as q 
import curves as c 
import helpers as h

filename = 'vision_low.csv'
output = vd.analyze_vision_output(filename)

dbPath = 'inpro_xlate.sqlite'    
session = u.loadSession(dbPath)
simid = 1
startMonth, endMonth = q.startMonth(session, simid), q.endMonth(session, simid)
years = h.yearIndicies(startMonth, endMonth)
years = [year + 2009 for year in years]
    
inYears = True
fac_t = "hwr_reactor"
hwrs = c.growthCurve(session, fac_t, startMonth, endMonth, inYears)
fac_t = "lwr_reactor"
lwrs = c.growthCurve(session, fac_t, startMonth, endMonth, inYears)

plt.plot(output.years[2:], output.lwrs[2:], label = "Vision LWRS")
plt.plot(output.years[2:], output.hwrs[2:], label = "Vision HWRS")
plt.plot(years, hwrs, label = "Cyclus HWRS")
plt.plot(years, lwrs, label = "Cyclus LWRS")
plt.axis([2010,2100,0,max(max(output.lwrs),max(lwrs))])
plt.legend(loc=2)
plt.title('Number of Deployed Reactors')
plt.xlabel('Year')
plt.ylabel('Quantity')
#    plt.show()
plt.savefig('rxtrs.eps')
plt.clf()
