
import queries as q

def growthCurve(session, fac_t, startMonth, endMonth, inYears = True):
    """ returns a list of growth values for a given facility type either per
    month or per year
    """
    return q.nFacsInRange(session, fac_t, startMonth, endMonth, byYear = inYears)

