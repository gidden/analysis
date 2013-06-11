import tables as tbls
import helpers as h

def nFacs(session, fac_t, startTime, endTime = None):
    """returns the number of agents of a given type at a given time
    """
    if endTime is None: endTime = startTime

    f1 = tbls.Agents.Prototype == fac_t
    f2 = tbls.Agents.EnterDate <= endTime
    entry_rows = session.query(tbls.Agents).filter(f1).filter(f2).all()
    entry_ids = set(row.ID for row in entry_rows)
    assert len(entry_rows) == len(entry_ids)
    
    f1 = tbls.AgentDeaths.DeathDate > startTime
    f2 = tbls.AgentDeaths.AgentID.in_(entry_ids)
    result = session.query(tbls.AgentDeaths).filter(f1).filter(f2).all()
    return len(result)
            
def startMonth(session, simid):
    f = tbls.SimulationTimeInfo.SimId == simid
    result = session.query(tbls.SimulationTimeInfo).filter(f).all()
    assert len(result) == 1
    return result[0].SimulationStart

def endMonth(session, simid):
    f = tbls.SimulationTimeInfo.SimId == simid
    result = session.query(tbls.SimulationTimeInfo).filter(f).all()
    assert len(result) == 1
    return result[0].Duration
