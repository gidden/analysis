
import queries as q
import helpers as h

def growthCurve(session, fac_t, startMonth, endMonth, inYears = True):
    """ returns a list of growth values for a given facility type
    """
    result = q.nFacsInRange(session, fac_t, startMonth, endMonth)
    if inYears: return h.convertValuesMtoY(result)
    else: return result

