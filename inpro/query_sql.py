#! /usr/bin/env python

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import Column, Integer, Float

import math
 
class Agents(object):
    pass

class Enrichment(object):
    pass
 
class Transactions(object):
    pass

class TransactedResources(object):
    pass

class CyclusOutput(object):
    def __init__(self,time,lwrs,hwrs,reactors,used_fuel,swu,natl_u):
        self.years = time
        self.lwrs = lwrs
        self.hwrs = hwrs
        self.reactors = reactors
        self.used_fuel = used_fuel
        self.swu = swu
        self.natl_u = natl_u
 
#----------------------------------------------------------------------
def loadSession(dbPath):
    engine = create_engine('sqlite:///%s' % dbPath, echo=True)
    metadata = MetaData(engine)

    agents = Table('agents', metadata, autoload=True)
    mapper(Agents,agents)

    enrichment = Table('enrichment', metadata, 
                       Column("ID", Integer, primary_key=True),
                       autoload=True)
    mapper(Enrichment,enrichment) 

    map_transactions = Table('transactions', metadata, autoload=True)
    mapper(Transactions,map_transactions) 

    transactedresources = Table('transactedresources', metadata, autoload=True)
    mapper(TransactedResources,transactedresources) 

    Session = sessionmaker(bind=engine)
    session = Session()
    return session

class EnrRow(object):
    def __init__(self,time,swu,natl_u):
        self.Time = time
        self.SWU = swu
        self.Natural_Uranium = natl_u

class Transaction(object):
    def __init__(self,time,uid):
        self.time = time
        self.id = uid

def load_enr(filename):
    fin = open(filename,'r')
    lines = fin.readlines()
    fin.close()

    rows = []
    count = 0
    for line in lines:
        count += 1
        if count > 1:
            entries = line.split(',')
            time = int(entries[1][2:-1])
            swu = int(entries[3][2:-2])
            u = int(entries[2][2:-1])/1e6
            # if swu > 0:
            #     u = int(entries[2][2:-1])/1e6
            # else:
            #     u = 0
            rows.append(EnrRow(time,swu,u))
    return rows

def get_reactors(nyears,nmonths,offset_month,session):
    lwr_months = [0] * nmonths
    hwr_months = [0] * nmonths
    entries = [[0] * nmonths,[0] * nmonths]
    leaves = [[0] * nmonths,[0] * nmonths]

    lwr_rows = session.query(Agents).filter(Agents.Prototype.like("LWR_Reactor")).all()
    hwr_rows = session.query(Agents).filter(Agents.Prototype.like("HWR_Reactor")).all()

    for row in lwr_rows:
        entries[0][row.EnterDate] += 1
        if (row.LeaveDate < nmonths):
            if (row.LeaveDate is not None):
                leaves[0][row.LeaveDate] += 1

    for row in hwr_rows:
        entries[1][row.EnterDate] += 1
        if (row.LeaveDate < nmonths):
            if (row.LeaveDate is not None):
                leaves[1][row.LeaveDate] += 1

    lwr_years = [0] * nyears
    hwr_years = [0] * nyears
    for month in range(nmonths-1):
        year = int(math.floor((offset_month+month+1)/12))
        lwr_years[year] += entries[0][month+1] - leaves[0][month]
        hwr_years[year] += entries[1][month+1] - leaves[1][month]

    for year in range(nyears-1):
        lwr_years[year+1] += lwr_years[year]
        hwr_years[year+1] += hwr_years[year]
    
    return lwr_years, hwr_years

def get_used_fuel(nyears,nmonths,offset_month,trans_f,trans_rsrcs_f):
    fin = open(trans_rsrcs_f,'r')
    lines = fin.readlines()
    fin.close()

    check_val = 1.38139
    tol = 0.001

    transactions = {}
    count = 0
    for line in lines:
        count += 1
        if count > 1:
            entries = line.split(',')
            uid = int(entries[0][1:-1])
            amt = float(entries[4][2:-2])/1e6
            if abs(amt-check_val) < tol:
                amt /= 10
            transactions[uid] = amt

    fin = open(trans_f,'r')
    lines = fin.readlines()
    fin.close()

    lwr_check = 0
    hwr_check = 0
    lwr_val = 0.018764 
    hwr_val = 0.138139
    fuel_months = [0] * nmonths
    count = 0
    for line in lines:
        count += 1
        if count > 1:
            entries = line.split(',')
            uid = int(entries[0][1:-1])
            month = int(entries[5][2:-1])
            commodity = entries[4][2:-1]
            if commodity == 'waste':
                fuel_months[month] += transactions[uid]
                if int(math.floor((offset_month+month)/12)) == 2:#(34-8):
                    if abs(transactions[uid]-lwr_val) < tol:
                        lwr_check += 1
                    elif abs(transactions[uid]-hwr_val) < tol:
                        hwr_check += 1
                    else:
                        print 'no match'
    print lwr_check, hwr_check

    fuel_years = [0] * nyears
    for month in range(nmonths):
        year = int(math.floor((offset_month+month)/12))
        fuel_years[year] += fuel_months[month]

    return fuel_years

# def get_used_fuel(nyears,nmonths,offset_month,session):
#     trans_rows = session.query(Transactions).filter(Transactions.Commodity.like("waste")).all()
#     transactions = {}
#     for row in trans_rows:
#         if row.ID % 10000 == 0:
#             print "Adding transaction" + str(row.ID) + " at time " + str(row.Time)
#         transactions[int(row.ID)] = int(row.Time)

#     fuel_months = [0] * nmonths
#     rsrc_rows = session.query(TransactedResources).all()
#     for row in rsrc_rows:
#         if row.TransactionID % 10000 == 0:
#             print "Looking at row: " + str(row.TransactionID) + " and this is a waste transaction? " + str(transactions.has_key(int(row.TransactionID)))
#         if transactions.has_key(int(row.TransactionID)): 
#             fuel_months[transactions[int(row.TransactionID)]] += float(row.Quantity)/1e6

#     fuel_years = [0] * nyears
#     for month in range(nmonths):
#         year = int(math.floor((offset_month+month+1)/12))
#         fuel_years[year] += fuel_months[month]
#     return fuel_years

def analyze_cyclus_output(enr_f,trans_f,trans_rsrcs_f,db):
    time = []
    start_year = 2007
    end_year = 2100
    offset_month = 11
    
    nyears = (end_year - start_year)
    nmonths = nyears*12-offset_month

    swu_months = [0] * nmonths
    natl_u_months = [0] * nmonths

    res = load_enr(enr_f)
    for row in res:
        swu_months[row.Time] += row.SWU
        natl_u_months[row.Time] += row.Natural_Uranium
    
    swu_years = [0] * nyears
    natl_u_years = [0] * nyears
    for i in range(nyears):
        time.append(start_year + i)

    for month in range(nmonths):
        year = int(math.floor((offset_month+month)/12))
        swu_years[year] += swu_months[month]
        natl_u_years[year] += natl_u_months[month]

    for year in range(len(swu_years)-1):
        swu_years[year+1] += swu_years[year]
#        natl_u_years[year+1] += natl_u_years[year]

    session = loadSession(db)    
    lwrs, hwrs = get_reactors(nyears,nmonths,offset_month,session)
    reactors = []
    for n in range(len(lwrs)):
        reactors.append(lwrs[n]+hwrs[n])

    # used_fuel = get_used_fuel(nyears,nmonths,offset_month,session)
    used_fuel = get_used_fuel(nyears,nmonths,offset_month,trans_f,trans_rsrcs_f)

    for year in range(len(used_fuel)-1):
        used_fuel[year+1] += used_fuel[year]

    return CyclusOutput(time,lwrs,hwrs,reactors,used_fuel,swu_years,natl_u_years)

 
if __name__ == "__main__":
    nagents = {0:0}

    dbPath = 'inpro_low.sqlite'    
    session = loadSession(dbPath)
    res = session.query(Agents).filter(Agents.Prototype.like("LWR_Reactor")).all()
    for row in res:
        if row.EnterDate in nagents:
            nagents[row.EnterDate] += 1
        else:
            nagents[row.EnterDate] = 1

        # if row.LeaveDate in agents:
        #     nagents[row.LeaveDate] -= 1
        # else:
        #     nagents[row.LeaveDate] = -1

    # for entry in nagents:
    #     print entry, nagents[entry]

    total_swu = 0
    res = session.query(Enrichment).all()
    print len(res)
    for row in res:
        print row.SWU
        total_swu += float(row.SWU)
    print total_swu
