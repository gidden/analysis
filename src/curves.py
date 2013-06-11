
import queries as q
import helpers as h

def growthCurve(session, fac_t, startMonth, endMonth, inYears = False):
    """ returns a list of growth values for a given facility type either per
    month or per year
    """
    if inYears:
        years = h.getYearPoints(startMonth, endMonth)
        return [q.nFacs(session, fac_t, year.startMonth, year.endMonth) \
                    for year in years]
    else:
        return [q.nFacs(session, fac_t, startMonth + i) \
                    for i in range(endMonth - startMonth)]

def materialFlowCurve(session, fac_t, commod_t, startMonth, endMonth, \
                          direction = "in", inYears = False):
    """returns a material flow listing into a given facility class and commodity
    class either by month or by year. the curve is constructed as either "in"
    flow or "out" flow given by the direction.
    """
    if inYears:
        years = h.getYearPoints(startMonth, endMonth)
        return [q.materialFlow(session, fac_t, commod_t, \
                                   year.startMonth, year.endMonth, \
                                   direction = direction) \
                    for year in years]
    else:
        return [q.materialFlow(session, fac_t, commod_t, \
                                   startMonth + i, direction = direction) \
                    for i in range(endMonth - startMonth)]

def materialInventoryCurve(session, fac_t, commod_t, startMonth, endMonth, \
                               byYear = False):
    """returns the inventory of materials of a given facility class and
    commodity class either by month or by year
    """
    outof = materialFlowCurve(session, fac_t, commod_t, startMonth, endMonth, \
                                  direction = "out", byYear = byYear)
    into = materialFlowCurve(session, fac_t, commod_t, startMonth, endMonth, \
                                  direction = "in", byYear = byYear)
    return outof - into
