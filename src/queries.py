import tables as tbls

def agents(session, name):
    """returns a list of entries in the Agents table given the name of an
    Agent's prototype
    """
    search = tbls.Agents.Prototype.like(name)
    return session.query(tbls.Agents).filter(search).all()

def enterDate(session, agentId):
    """returns the Cyclus date that a specific agent entered the simulation"""
    search = tbls.Agents.ID.like(agentId)
    result = session.query(tbls.Agents).filter(search).all()
    assert len(result) == 1
    return result[0].EnterDate

def leaveDate(session, agentId):
    """returns the Cyclus date that a specific agent left the simulation"""
    search = tbls.AgentDeaths.AgentID.like(agentId)
    result = session.query(tbls.AgentDeaths).filter(search).all()
    assert len(result) == 1
    return result[0].DeathDate

def nFacs(session, agents, time):
    """returns the number of agents of a given type at a given time
    """
    n = 0
    for agent in agents:
        if enterDate(session, agent.ID) <= time \
                and leaveDate(session, agent.ID) > time:
            n += 1
    return n
            
def nFacsInRange(session, agents, start, end):
    """returns a list of the number of agents at each time step given a starting
    and ending time step
    """
    return [nFacs(session, agents, start + i) for i in range(end - start)]
        
