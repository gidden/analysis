import tables as tbls

import helpers as h

def qAgents(session, fac_t):
    """returns a query of entries in the Agents table given the name of an
    Agent's prototype
    """
    search = tbls.Agents.Prototype == fac_t
    return session.query(tbls.Agents).filter(search)

def nFacs(session, fac_t, startTime, endTime = None):
    """returns the number of agents of a given type at a given time
    """
    if endTime is None: endTime = startTime

    search = tbls.Agents.EnterDate <= endTime
    entry_rows = qAgents(session, fac_t).filter(search).all()
    entry_ids = set(row.ID for row in entry_rows)
    assert len(entry_rows) == len(entry_ids)

    search1 = tbls.AgentDeaths.DeathDate > startTime
    search2 = tbls.AgentDeaths.AgentID.in_(entry_ids)
    result = session.query(tbls.AgentDeaths).filter(search1).filter(search2).all()
    return len(result)
            
def nFacsInRange(session, fac_t, start, end, byYear = False):
    """returns a list of the number of agents at each time step given a starting
    and ending time step
    """
    if byYear:
        years = h.getYearPoints(start, end)
        return [nFacs(session, fac_t, year.startMonth, year.endMonth) for year in years]
    else:
        return [nFacs(session, fac_t, start + i) for i in range(end - start + 1)]
                      

def startMonth(session, simid):
    search = tbls.SimulationTimeInfo.SimId == simid
    result = session.query(tbls.SimulationTimeInfo).filter(search).all()
    assert len(result) == 1
    return result[0].SimulationStart

def endMonth(session, simid):
    search = tbls.SimulationTimeInfo.SimId == simid
    result = session.query(tbls.SimulationTimeInfo).filter(search).all()
    assert len(result) == 1
    return result[0].Duration
