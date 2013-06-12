from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, clear_mappers, sessionmaker

from tables import getTableMaps as getTables

def loadSession(dbPath):
    clear_mappers()
    engine = create_engine('sqlite:///%s' % dbPath) #, echo=True)
    
    tables = getTables(engine)

    for key, value in tables.iteritems():
        mapper(value.obj, value.table)

    Session = sessionmaker(bind=engine)
    session = Session()
    return session
