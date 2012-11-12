#! /usr/bin/env python

import vision_data
import query_sql

import matplotlib.pyplot as plt

filename = 'vision_low/vision_low.csv'
vision_output_low = vision_data.analyze_vision_output(filename)

filename = 'vision_high/vision_high.csv'
vision_output_high = vision_data.analyze_vision_output(filename)

# enr_f = 'enrichment_low'
# trans_f = 'lise_transactions_low' #'transactions_low'
# trans_rsrcs_f = 'lise_transacted_resources_low' #'transacted_resources_low'
# db = 'lise_inpro_low.sqlite'#'inpro_low.sqlite'
# cyclus_output = query_sql.analyze_cyclus_output(enr_f,trans_f,trans_rsrcs_f,db)

start_year = 2007
end_year = 2100

plt.plot(vision_output_low.years, vision_output_low.lwrs, label="Vision LWRs")
plt.plot(vision_output_low.years, vision_output_low.hwrs, label="Vision HWRs")
plt.plot(vision_output_low.years, vision_output_low.reactors, label="Vision Total")

plt.plot(vision_output_high.years, vision_output_high.lwrs, label="Vision LWRs")
plt.plot(vision_output_high.years, vision_output_high.hwrs, label="Vision HWRs")
plt.plot(vision_output_high.years, vision_output_high.reactors, label="Vision Total")

plt.show()

# # Reactors
# plt.plot(vision_output.years, vision_output.lwrs, label="Vision LWRs")
# plt.plot(vision_output.years, vision_output.hwrs, label="Vision HWRs")
# plt.plot(vision_output.years, vision_output.reactors, label="Vision Total")
# plt.plot(cyclus_output.years, cyclus_output.lwrs, label="Cyclus LWRs")
# plt.plot(cyclus_output.years, cyclus_output.hwrs, label="Cyclus HWRs")
# plt.plot(cyclus_output.years, cyclus_output.reactors, label="Cyclus Total")
# plt.axis([start_year+1,end_year,0,max(max(vision_output.reactors),max(cyclus_output.reactors))])
# plt.legend(loc=2)
# plt.title('Number of Deployed Reactors')
# plt.xlabel('Year')
# plt.ylabel('Quantity')
# #plt.show()
# plt.savefig('rxtrs.eps')
# plt.clf()

# # SWU
# plt.plot(vision_output.years, vision_output.swu, label="Vision")
# plt.plot(cyclus_output.years, cyclus_output.swu, label="Cyclus")
# plt.axis([start_year,end_year,0,max(cyclus_output.swu[-1],vision_output.swu[-1])])
# plt.legend(loc=2)
# plt.title('Total Cumulative SWU Required')
# plt.xlabel('Year')
# plt.ylabel('SWU')
# #plt.show()
# plt.savefig('swu.eps')
# plt.clf()

# # Waste
# plt.plot(vision_output.years, vision_output.used_fuel, label="Vision")
# plt.plot(cyclus_output.years, cyclus_output.used_fuel, label="Cyclus")
# plt.axis([start_year+2,end_year,min(vision_output.used_fuel[2],cyclus_output.used_fuel[2]),max(cyclus_output.used_fuel[-1],vision_output.used_fuel[-1])])
# plt.legend(loc=2)
# plt.title('Total Cumulative Used Fuel Produced by Reactors')
# plt.xlabel('Year')
# plt.ylabel('Quantity (kt)')
# #plt.show()
# plt.savefig('used_fuel.eps')
# plt.clf()

# # Nat U
# plt.plot(vision_output.years, vision_output.natl_u, label="Vision")
# plt.plot(cyclus_output.years, cyclus_output.natl_u, label="Cyclus")
# plt.axis([start_year,end_year,0,max(cyclus_output.natl_u[-1],vision_output.natl_u[-1])])
# plt.legend(loc=2)
# plt.title('Total Cumulative Natural Uranium Required')
# plt.xlabel('Year')
# plt.ylabel('Quantity (kt)')
# plt.show()
# plt.savefig('nat_u.eps')
# plt.clf()

# # plt.plot(cyclus_output.years, cyclus_output.natl_u)
# # plt.axis([start_year,end_year,0,cyclus_output.natl_u[-1]])
# # plt.show()

# # plt.plot(vision_output.years, vision_output.natl_u)
# # plt.axis([start_year,end_year,0,vision_output.natl_u[-1]])
# # plt.show()

# print "Cyclus:"
# for i in range(5):
#     index = i#+25
#     print cyclus_output.years[index], cyclus_output.lwrs[index], cyclus_output.hwrs[index], cyclus_output.used_fuel[index]

# print "Vision:"
# for i in range(5):
#     index = i#+25
#     print vision_output.years[index], vision_output.lwrs[index], vision_output.hwrs[index], vision_output.used_fuel[index]
