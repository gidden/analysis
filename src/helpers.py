from copy import copy

def splitMonthValues(values):
    """returns a list of values grouped into increments of 12. if the length
    isn't divisible by 12, the last group will house the remaining values (i.e.,
    the last group will have len <= 12 whereas every other group will have len
    == 12).
    """
    vals = copy(values)
    split_vals = []
    while len(vals) > 12:
        group = [vals.pop(0) for i in range(12)]
        split_vals.append(group)
    split_vals.append(vals)
    return split_vals

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
    split_vals = splitMonthValues(values)
    return [getYearlyValue(vals) for vals in split_vals]
