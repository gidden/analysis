#! /usr/bin/env python

import vision_data
import cyclus_data

import matplotlib.pyplot as plt

handles = ['_low']#,'_high']
  
start_year = 2007
end_year = 2100

for handle in handles:
    folder = 'vision'+handle+'/'
    filename = folder+'vision'+handle+'.csv'
    vision_output = vision_data.analyze_vision_output(filename)
    
    folder = 'cyclus'+handle+'/'
    enr_f = folder+'enrichment'+handle+''
    trans_f = folder+'transactions'+handle
    trans_rsrcs_f = folder+'transacted_resources'+handle
    db = folder+'inpro'+handle+'.sqlite'
    cyclus_output = cyclus_data.analyze_cyclus_output(enr_f,trans_f,trans_rsrcs_f,db)
      
## Reactors
    plt.plot(vision_output.years, vision_output.lwrs, label="Vision LWRs")
    plt.plot(vision_output.years, vision_output.hwrs, label="Vision HWRs")
    plt.plot(vision_output.years, vision_output.reactors, label="Vision Total")
    plt.plot(cyclus_output.years, cyclus_output.lwrs, label="Cyclus LWRs")
    plt.plot(cyclus_output.years, cyclus_output.hwrs, label="Cyclus HWRs")
    plt.plot(cyclus_output.years, cyclus_output.reactors, label="Cyclus Total")
    plt.axis([start_year+1,end_year,0,max(max(vision_output.reactors),max(cyclus_output.reactors))])
    plt.legend(loc=2)
    plt.title('Number of Deployed Reactors')
    plt.xlabel('Year')
    plt.ylabel('Quantity')
#    plt.show()
    plt.savefig('rxtrs'+handle+'.eps')
    plt.clf()

## SWU
    plt.plot(vision_output.years, vision_output.swu, label="Vision")
    plt.plot(cyclus_output.years, cyclus_output.swu, label="Cyclus")
    plt.axis([start_year,end_year,0,max(cyclus_output.swu[-1],vision_output.swu[-1])])
    plt.legend(loc=2)
    plt.title('Total Cumulative SWU Required')
    plt.xlabel('Year')
    plt.ylabel('SWU')
#    plt.show()
    plt.savefig('swu'+handle+'.eps')
    plt.clf()
    
## Nat U
    plt.plot(vision_output.years, vision_output.natl_u, label="Vision")
    plt.plot(cyclus_output.years, cyclus_output.natl_u, label="Cyclus")
    plt.axis([start_year,end_year,0,max(cyclus_output.natl_u[-1],vision_output.natl_u[-1])])
    plt.legend(loc=2)
    plt.title('Total Cumulative Natural Uranium Required')
    plt.xlabel('Year')
    plt.ylabel('Quantity (kt)')
#    plt.show()
    plt.savefig('nat_u'+handle+'.eps')
    plt.clf()
    

## Waste
    plt.plot(vision_output.years[0:7], vision_output.used_fuel[0:7], label="Vision")
    plt.plot(cyclus_output.years[0:7], cyclus_output.used_fuel[0:7], label="Cyclus")
    # plt.axis([start_year+2,end_year,min(vision_output.used_fuel[2],cyclus_output.used_fuel[2]),max(cyclus_output.used_fuel[-1],vision_output.used_fuel[-1])])
    plt.axis([cyclus_output.years[0],cyclus_output.years[7],min(vision_output.used_fuel[0],cyclus_output.used_fuel[0]),max(cyclus_output.used_fuel[7],vision_output.used_fuel[7])]) 
    plt.legend(loc=2)
    plt.title('Total Cumulative Used Fuel Produced by Reactors')
    plt.xlabel('Year')
    plt.ylabel('Quantity (kt)')
    plt.show()
    plt.savefig('used_fuel'+handle+'.eps')
    plt.clf()
    lwr_amt = 18763.983/1e6
    hwr_amt = 138138.735/1e6
    print ""
    lwrs = [cyclus_output.lwrs[0], cyclus_output.lwrs[1], cyclus_output.lwrs[2]]
    hwrs = [cyclus_output.hwrs[0], cyclus_output.hwrs[1], cyclus_output.hwrs[2]]
    print lwrs[0], lwrs[1], lwrs[2]
    print hwrs[0], hwrs[1], hwrs[2]
    print lwr_amt*353+hwr_amt*38
    print cyclus_output.used_fuel[0], cyclus_output.used_fuel[1], cyclus_output.used_fuel[2]
    print vision_output.lwrs[0], vision_output.lwrs[1], vision_output.lwrs[2]
    print vision_output.hwrs[0], vision_output.hwrs[1], vision_output.hwrs[2]
    print vision_output.used_fuel[0], vision_output.used_fuel[1], vision_output.used_fuel[2]
    print ""

