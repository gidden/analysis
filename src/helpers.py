from copy import copy
from math import floor
from collections import namedtuple

YearPoint = namedtuple("YearPoint", "startMonth endMonth")

def groupItems(theList, groupSize):
    """returns a list of values grouped into increments of groupSize. if the
    length isn't divisible by groupSize, the last group will house the remaining
    values (i.e., the last group will have len <= groupSize whereas every other
    group will have len == groupSize).
    """
    vals = copy(theList)
    split_vals = []
    while len(vals) > groupSize:
        group = [vals.pop(0) for i in range(groupSize)]
        split_vals.append(group)
    split_vals.append(vals)
    return split_vals

def groupByYear(theList):
    """given a list of values per month, groupByYear returns a list of values
    partitioned by year. For example, if a list contains 24 values, groupByYear
    will return a container of two lists, each with 12 values. If the total
    number of values is not divisible by 12, the remainder will be housed in the
    final group.
    """
    return groupItems(theList, 12)

def getYearlyValue(values):
    """returns a yearly value given 12 or less monthly values. currently,
    returns the maximum value in the list.
    """
    assert len(values) <= 12
    return max(values)

def convertValuesMtoY(values):
    """returns a list of values given on a month-to-month basis converted into
    their yearly totals
    """
    split_vals = groupByYear(values)
    return [getYearlyValue(vals) for vals in split_vals]

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
    
