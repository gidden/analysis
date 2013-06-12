from math import floor
from collections import namedtuple

YearPoint = namedtuple("YearPoint", "startMonth endMonth")

def getYearPoints(startMonth, endMonth):
    """given a starting month index and and ending month index, returns a
    collection of YearPoints covering the span.
    """
    start = startMonth
    points = []
    while start <= endMonth:
        end = start + 11
        if end < endMonth:
            year = YearPoint(start, end)
        else:
            year =YearPoint(start, endMonth)
        points.append(year)
        start += 12
    return points
                         
def yearIndicies(startMonth, endMonth):
    """returns a list of year indicies, assuming a simulation begins in year 0.
    The months-to-year mapping is as follows, months 0-11 => year 0, months
    12-23 => year 1, etc.
    """
    startYear = int(floor(startMonth / 12))
    endYear = int(floor(endMonth / 12))
    return [i + startYear for i in range(endYear - startYear + 1)]
    
