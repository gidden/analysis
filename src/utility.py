from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import mapper, clear_mappers, sessionmaker

import tables as tbls

def loadSession(dbPath):
    clear_mappers()
    engine = create_engine('sqlite:///%s' % dbPath) #, echo=True)
    metadata = MetaData(engine)
    tables = tbls.getTableMaps(metadata)
    for value in tables.itervalues():
        mapper(value.obj, value.table)

    Session = sessionmaker(bind=engine)
    session = Session()
    return session
