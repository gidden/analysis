#! /usr/bin/env python

class VisionOutput(object):
    def __init__(self,years,lwrs,hwrs,reactors,used_fuel,swu,natl_u):
        self.years = years
        self.lwrs = lwrs
        self.hwrs = hwrs
        self.reactors = reactors
        self.used_fuel = used_fuel
        self.swu = swu
        self.natl_u = natl_u

def analyze_vision_output(filename):

    fin = open(filename,'r')
    low_lines = fin.readlines()
    fin.close()

    year_index = 0
    swu_index = year_index + 4
    ore_index = year_index + 5
    u_index = year_index + 8
    lwr_index = year_index + 11
    hwr_index = year_index + 12
    wet_index = 14
    dry_index = 17
    
    count = 0
    entry_start = 12
    
    years = []
    lwrs = []
    hwrs = []
    reactors = []
    used_fuel = []
    swu = []
    natl_u = []
    
    for line in low_lines:
        count += 1
        if count >= entry_start:
            entries = line.split(',')
            
            years.append(entries[year_index])
            
            nlwrs = int(entries[lwr_index])
            nhwrs = int(entries[hwr_index])
            lwrs.append(nlwrs)
            hwrs.append(nhwrs)
            reactors.append(nlwrs+nhwrs)
            
            swu.append(float(entries[swu_index]))
            natl_u_used = float(entries[ore_index]) + float(entries[ore_index+1])
            natl_u.append(natl_u_used)
            
            wet_fuel = float(entries[wet_index]) + float(entries[wet_index+1])
            dry_fuel =  float(entries[dry_index]) + float(entries[dry_index+1])
            used_fuel.append(wet_fuel+dry_fuel)
    
    # subtract = 0
    # for year in range(len(used_fuel)-1):
    #     subtract += used_fuel[year]
    #     used_fuel[year+1] -= subtract
    
    subtract = 0
    for year in range(len(natl_u)-1):
        subtract += natl_u[year]
        natl_u[year+1] -= subtract

    return VisionOutput(years,lwrs,hwrs,reactors,used_fuel,swu,natl_u)

if __name__=="__main__":            

    import matplotlib.pyplot as plt
    
    filename = 'vision_low.csv'
    
    output = analyze_vision_output(filename)
    
    plt.plot(output.years, output.lwrs, output.years, output.hwrs, output.years, output.reactors)
    plt.axis([2008,2100,0,output.reactors[-1]])
    plt.show()
    
    plt.plot(output.years, output.swu)
    plt.axis([2008,2100,0,output.swu[-1]])
    plt.show()
