
import queries as q
import helpers as h

def growthCurve(session, fac_t, startMonth, endMonth, inYears = True):
    """ returns a list of growth values for a given facility type either per
    month or per year
    """
    if inYears:
        years = h.getYearPoints(startMonth, endMonth)
        return [q.nFacs(session, fac_t, year.startMonth, year.endMonth) \
                    for year in years]
    else:
        return [q.nFacs(session, fac_t, start + i) \
                    for i in range(end - start + 1)]

