This repository provides a location of analysis and data visualization tools for
*Cyclus* output.

Overview
--------

The tool suite is nominally broken into 4 modules.

* Utility - provides access tools to the *Cyclus* database
* Tables - provides table descriptions of the *Cyclus* database
* Queries - provides an interface for standard queries of the Cyclus database
* Helpers - provides helper functions to aggregate data and time series

Usage
-----

Connection to the Databse
=========================

The analysis tools use SQLAlchemy's Object Relational Mapping (ORM) interface to
assist in making querying the *Cyclus* database easier. Querying the database
requires an active session, which can be accessed via:

```python
import utility		
dbPath = 'some_relative_path_to_the_database'
session = utility.loadSession(dbPath)
```

