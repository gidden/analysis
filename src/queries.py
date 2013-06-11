import tables as tbls

def agents(session, name):
    """returns a list of entries in the Agents table given the name of an
    Agent's prototype
    """
    search = tbls.Agents.Prototype == name
    return session.query(tbls.Agents).filter(search).all()

def agentdeaths(session):
    """returns a list of entries in the AgentDeaths table
    """
    return tbls.AgentDeaths

def enterDate(session, agent):
    """returns the Cyclus date that a specific agent entered the simulation"""
    return agent.EnterDate

def leaveDate(session, agent, agentdeaths):
    """returns the Cyclus date that a specific agent left the simulation"""
    search = agentdeaths.AgentID == agent.ID
    result = session.query(agentdeaths).filter(search).all()
    assert len(result) == 1
    return result[0].DeathDate

def nFacs(session, agents, time):
    """returns the number of agents of a given type at a given time
    """
    n = 0
    for agent in agents:
        if enterDate(session, agent) <= time \
                and leaveDate(session, agent, agentdeaths(session)) > time:
            n += 1
    return n
            
def nFacsInRange(session, agents, start, end):
    """returns a list of the number of agents at each time step given a starting
    and ending time step
    """
    return [nFacs(session, agents, start + i) for i in range(end - start)]

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
