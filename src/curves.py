
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
        return [q.nFacs(session, fac_t, month) \
                    for month in range(startMonth, endMonth + 1)]

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
                                   month, direction = direction) \
                    for month in range(startMonth, endMonth + 1)]

def materialInventoryCurve(session, fac_t, commod_t, startMonth, endMonth, \
                               inYears = False):
    """returns the inventory of materials of a given facility class and
    commodity class either by month or by year
    """
    outof = materialFlowCurve(session, fac_t, commod_t, startMonth, endMonth, \
                                  direction = "out", inYears = inYears)
    into = materialFlowCurve(session, fac_t, commod_t, startMonth, endMonth, \
                                  direction = "in", inYears = inYears)
    return outof - into

def SWUCurve(session, startMonth, endMonth, inYears = False):
    """returns the a list of amount of SWU used at each time point by month or
    by year
    """    
    if inYears:
        years = h.getYearPoints(startMonth, endMonth)
        return [q.SWU(session, year.startMonth, endTime = year.endMonth) \
                    for year in years]
    else:
        return [q.SWU(session, month) \
                    for month in range(startMonth, endMonth + 1)]

def natlUCurve(session, startMonth, endMonth, inYears = False):
    """returns the a list of amount of natural uranium used at each time point
    by month or by year
    """    
    if inYears:
        years = h.getYearPoints(startMonth, endMonth)
        return [q.natlU(session, year.startMonth, endTime = year.endMonth) \
                    for year in years]
    else:
        return [q.natlU(session, month) \
                    for month in range(startMonth, endMonth + 1)]
