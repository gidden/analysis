import sqlalchemy as sql
from collections import namedtuple

"""SQLAlchemy provides a session interface to query databases. Database tables
are read into empty class objects that the user provides as a mapping.
"""

TableMapping = namedtuple("TableMapping", "obj table")
 
class Agents(object):
    pass

class AgentDeaths(object):
    pass

class Enrichments(object):
    pass 

class IsotopicStates(object):
    pass

class Resources(object):
    pass

class ResourceTypes(object):
    pass

class SimulationIDs(object):
    pass

class SimulationTimeInfo(object):
    pass

class TransactedResources(object):
    pass

class Transactions(object):
    pass

def getTableMaps(engine):
    """ This is the main configure function for reading the cyclus db. If the
    database structure changes, the changes must be reflected here.

    Each table is entered in the the dictionary of tables. Primary keys must be
    included in the definition of the Table class in order for SQLAlchemy to
    read tables from the database using ORM.
    """
    tables = {}
    metadata = sql.MetaData(engine)
    dialect = engine.dialect
    connection = engine.connect()

    # agents
    name = 'agents'
    if dialect.has_table(connection, name):
        obj = Agents
        table = sql.Table(name, \
                              metadata, \
                              sql.Column("ID", sql.Integer, primary_key=True), \
                              autoload=True)
        tables[name] = TableMapping(obj, table)

    # agent deaths
    name = 'agentdeaths'
    if dialect.has_table(connection, name):
        obj = AgentDeaths
        table = sql.Table(name, \
                              metadata, \
                              sql.Column("AgentID", sql.Integer, primary_key=True), \
                              autoload=True)
        tables[name] = TableMapping(obj, table)
        
    # isotopic states
    name = 'isotopicstates'
    if dialect.has_table(connection, name):
        obj = IsotopicStates
        table = sql.Table(name, \
                              metadata, \
                              sql.Column("ID", sql.Integer, primary_key=True), \
                              sql.Column("IsoID", sql.Integer, primary_key=True), \
                              autoload=True)
        tables[name] = TableMapping(obj, table)

    # enrichment
    name = 'enrichments'
    if dialect.has_table(connection, name):
        obj = Enrichments
        table = sql.Table(name, \
                              metadata, \
                              sql.Column("Type", sql.Integer, primary_key=True), \
                              autoload=True)
        tables[name] = TableMapping(obj, table)

    # resource types
    name = 'resourcetypes'
    if dialect.has_table(connection, name):
        obj = ResourceTypes
        table = sql.Table(name, \
                              metadata, \
                              sql.Column("Type", sql.Integer, primary_key=True), \
                              autoload=True)
        tables[name] = TableMapping(obj, table)
    
    # sim ids
    name = 'simulationids'
    if dialect.has_table(connection, name):
        obj = SimulationIDs
        table = sql.Table(name, \
                              metadata, \
                              sql.Column("SimId", sql.Integer, primary_key=True), \
                              autoload=True)
        tables[name] = TableMapping(obj, table)
        
    # simulation time
    name = 'simulationtimeinfo'
    if dialect.has_table(connection, name):
        obj = SimulationTimeInfo
        table = sql.Table(name, \
                              metadata, \
                              sql.Column("SimId", sql.Integer, primary_key=True), \
                              autoload=True)
        tables[name] = TableMapping(obj, table)

    # transactions
    name = 'transactions'
    if dialect.has_table(connection, name):
        obj = Transactions
        table = sql.Table(name, \
                              metadata, \
                              sql.Column("ID", sql.Integer, primary_key=True), \
                              autoload=True)
        tables[name] = TableMapping(obj, table)

    # transacted resources
    name = 'transactedresources'
    if dialect.has_table(connection, name):
        obj = TransactedResources
        table = sql.Table(name, \
                              metadata, \
                              sql.Column("ResourceID", sql.Integer, primary_key=True), \
                              sql.Column("TransactionID", sql.Integer, primary_key=True), \
                              autoload=True)
        tables[name] = TableMapping(obj, table)

    return tables

    
