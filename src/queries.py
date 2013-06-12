import tables as tbls
import helpers as h
from sqlalchemy import func
        
def nFacs(session, fac_t, startTime, endTime = None):
    """returns the number of agents of a given type at a given time
    """
    if endTime is None: endTime = startTime

    f1 = tbls.Agents.Prototype == fac_t
    f2 = tbls.Agents.EnterDate <= endTime
    entry_rows = session.query(tbls.Agents).filter(f1).filter(f2).all()
    entry_ids = set(row.ID for row in entry_rows)
    assert len(entry_rows) == len(entry_ids)
    
    f1 = tbls.AgentDeaths.DeathDate >= startTime # if death == start, its still in the sim at that point
    f2 = tbls.AgentDeaths.AgentID.in_(entry_ids)
    result = session.query(tbls.AgentDeaths).filter(f1).filter(f2).all()
    return len(result)

def materialFlow(session, fac_t, commod_t, startTime, endTime = None, \
                     direction = "in"):
    """returns the flow of a class of material into or out of a facility class
    over a given time range
    """
    if endTime is None: 
        endTime = startTime
    span = range(startTime, endTime + 1)

    f = tbls.Agents.Prototype == fac_t
    agent_rows = session.query(tbls.Agents).filter(f).all()
    agent_ids = set(row.ID for row in agent_rows)
    assert len(agent_rows) == len(agent_ids) > 0

    if direction is "in": 
        f1 = tbls.Transactions.ReceiverID.in_(agent_ids)
    else:
        f1 = tbls.Transactions.SenderID.in_(agent_ids)
    f2 = tbls.Transactions.Time.in_(span)
    f3 = tbls.Transactions.Commodity == commod_t
    transactions = session.query(tbls.Transactions)\
        .filter(f1).filter(f2).filter(f3).all()
    trans_ids = set(row.ID for row in transactions)
    assert len(transactions) == len(trans_ids)
    
    if len(trans_ids) == 0:
        return 0.0
    else:
        fil = tbls.TransactedResources.TransactionID.in_(trans_ids)
        fun = func.sum(tbls.TransactedResources.Quantity)
        return session.query(fun).filter(fil).scalar()

def SWU(session, startTime, endTime = None, agentID = None):
    """returns SWU usage as reported in the Enrichments table. Optional
    arguments include an ending time period and an agentID. If an ending time is
    provided, the SWU usage is totaled over the time period. If an agentID is
    provided, only SWU usaged related to that agent is included.
    """
    if endTime is None: endTime = startTime
    span = range(startTime, endTime)
    
    fun = func.sum(tbls.Enrichments.SWU)
    f1 = tbls.Enrichments.Time.in_(span)
    if agentID is not None:
        f2 = tbls.Enrichments.ID == agentID
        return session.query(fun).filter(f1).filter(f2).scalar()
    else:
        return session.query(fun).filter(f1).scalar()

def natlU(session, startTime, endTime = None, agentID = None):
    """returns natural uranium usage as reported in the Enrichments
    table. Optional arguments include an ending time period and an agentID. If
    an ending time is provided, the natural uranium usage is totaled over the
    time period. If an agentID is provided, only natural uranium usaged related
    to that agent is included.
    """
    if endTime is None: endTime = startTime
    span = range(startTime, endTime)
    
    fun = func.sum(tbls.Enrichments.Natural_Uranium)
    f1 = tbls.Enrichments.Time.in_(span)
    if agentID is not None:
        f2 = tbls.Enrichments.ID == agentID
        return session.query(fun).filter(f1).filter(f2).scalar()
    else:
        return session.query(fun).filter(f1).scalar()
    
def startMonth(session, simid):
    f = tbls.SimulationTimeInfo.SimId == simid
    result = session.query(tbls.SimulationTimeInfo).filter(f).all()
    assert len(result) == 1
    return result[0].SimulationStart

def nMonths(session, simid):
    f = tbls.SimulationTimeInfo.SimId == simid
    result = session.query(tbls.SimulationTimeInfo).filter(f).all()
    assert len(result) == 1
    return result[0].Duration


def endMonth(session, simid):
    # note -1 because we begin month indexing at 0
    return nMonths(session, simid) - startMonth(session, simid) - 1
    
