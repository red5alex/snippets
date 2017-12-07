"""
    Python Wrapper Class for FEFLOW time series.
"""

__author__ = 'are'


class CTimeSeries:
    """
    Python Wrapper Class for FEFLOW time series.

    Class CTimeSeries:

    members:
    str             name        Name of the time seres
    int             id          Time Series ID
    [(float,float)] DataPoints  List of Data Points (
    str             type        Interpolation option:
                                    "Polylined"
                                    "Constant"
    str             option      Time options:
                                    "linear"
                                    "cyclic"
    str             timeunit    unit of time axis
    str             unitclass   unit class of values
    str             userunit    unit of values

    methods:
    __init__(filename)  Constructor. will call LoadFrom(filename) if filename is given, empty otherwise
    ___eq()___          euality operator
    ___hash()___        hash operator
    loadFrom(filename)  Clear all data and load new data from file (filename)
    saveTo(filename)    Write Data to File

    getTimes(self)                  returns a list with the time stamps
    getValueByTime(self, time)      returns the value at the given time
    getTotalTimeCoverageAndAverageValue(self):
    getAverageValue(self)           returns time averaged value (considers polylined and constant type series only
    getTotalTimeCoverage(self):     returns total time before initial and final point, excluding GAPs
    appendTimePoint(self, time, value): add an additional data point
    appendDatePoint(self, date, value, ref_date): add an additinal point by date
    insertGap(self, position=None): inserts a gap
    clean(self, pattern="equalMidPoints"): removes unncessery points from the time series

    see inline comments for more
    """

    ## limited to 12 characters, appears as name in feflow, should be borehole name | measurement (time series name truncated to 12 chars)
    name = ""
    ## FEFLOW time series ID
    id = -1
    ## List of data points (float:time, float:value) tuples or "GAP"
    DataPoints = []#.copy()
    ## type of time series (Polylined, Constant, ..)
    type = "Polylined"
    ## temporal behavior (linear, cyclic)
    option = "linear"
    ## time unit (FEFLOW)
    timeunit = "d"
    ## class (FEFLOW)
    unitclass = "CARDINAL"
    ## userunit (FEFLOW)
    userunit = ""

    def __init__(self):
        """
        Class Constructor.
        :return:
        """
        self.name = ""
        self.id = -1
        self.DataPoints = []

    def getTimes(self):
        """
        returns the list of time stamps.
        :return: list with the time stamps
        """
        times = []
        for dp in self.DataPoints:
            times.append(dp[0])
        return times

    def getValueByTime(self, time):
        """
        Retrieve the TS cvalue at the given time.
        :param: time: simualtion time to retrieve value
        :type: float
        :return: the value at the given time"""
        for dp in self.DataPoints:
            if dp[0] == time:
                return dp[1]

    def getTotalTimeCoverageAndAverageValue(self):
        """
        returns the average value of the time series.
        if time series has only one datapoint, its value is returned
        of no datapoint is available, None is returned
        :return: time span in days.
        :rtype: float
        """
        totaltimecoverage = 0.
        totalintegralvalue = 0.
        priorPoint = None

        # no data point:
        if len(self.DataPoints) == 0:
            return 0, None

        # one data point:
        if len(self.DataPoints) == 1:
            return 0, self.DataPoints[0][1]

        # multiple data points
        for p in self.DataPoints:
            if priorPoint is None or priorPoint == 'GAP':
                priorPoint = p
                continue
            elif p != 'GAP':
                t0, f0 = priorPoint
                t1, f1 = p

                t0=float(t0)
                t1=float(t1)
                f0=float(f0)
                f1=float(f1)

                totaltimecoverage += t1 - t0
                if self.type == "Polylined":
                    totalintegralvalue += (f0 + f1)/2 * (t1 - t0)
                if self.type == "Constant":
                    totalintegralvalue += f0 * (t1 - t0)
            priorPoint = p
        average_value = totalintegralvalue / totaltimecoverage
        return totaltimecoverage, average_value

    def getAverageValue(self):
        """
        The average value of the time series (based on temporal Integration. (Note that this is different
        from the standard deviation of a sample set.
        :return:the average value as <float>
        """
        t, f = self.getTotalTimeCoverageAndAverageValue()
        return f

    def getTotalTimeCoverage(self):
        """
        Get the total coverage of the time series in days
        :return:
        """
        t, f = self.getTotalTimeCoverageAndAverageValue()
        return t

    def getTimeValues(self):
        """
        get all times of valid data points (GAP values are removed)
        :return:
        """
        a = [x[0] for x in self.DataPoints]
        while 'G' in a:
            a.remove('G')  # "G" is returned at a GAP
        return a

    def getDataValues(self):
        """
        Return the list of data values (GAP values removed)
        :return: list of values
        """
        a = [x[1] for x in self.DataPoints]
        while 'A' in a:
            a.remove('A')  # "A" is returned at a GAP
        return a

    def getTrend(self, initialtime=None, finaltime=None):
        """
        Caluclate the trend of the time series.
        :param initialtime: stattime of interval.
        :param finaltime: endtime of interval.
        :return: trend
        :rtype: float
        """
        a = self.getTimeValues()
        if len(a) < 2:
            return None
        if initialtime is None:
            initialtime = a[0]
        if finaltime is None:
            finaltime = a[-1]
        midtime = (initialtime + finaltime) / 2
        average = self.getAverageValue()

    def appendTimePoint(self, time, value):
        """
        Append a point to the time series
        :param time: time value in days
        :param value: value
        :return:
        """
        t = float(time)
        f = float(value)
        self.DataPoints.append((t, f))

    def appendDatePoint(self, date, value, ref_date):
        """
        Appends a point to the time series, provided as a julian date.
        :param date: Julian date
        :param value: value
        :param ref_date: reference of Julian date.
        :return:
        """
        delta = date - ref_date
        days = delta.days
        seconds = delta.seconds
        time = days + seconds/(24*60*60)
        self.appendTimePoint(time, float(value))

    def insertGap(self, position=None):
        """
        adds a GAP at the given location
        :param position: time stage number (default: end of time series)
        :return:
        """
        if position is not None:
            self.DataPoints.insert(position, "GAP")
        else:
            self.DataPoints.append("GAP")

    def clean(self, pattern="equalMidPoints"):
        """
        Removes unnecessary data points from the time series.
        :param pattern: the pattern to be used. "equalMidPoints" removes all points i where f(i-1) = f(i) = f(i+1)
        """
        if pattern is "equalMidPoints":
            dp = self.DataPoints
            pass
            for i in range(len(dp)-2, 1, -1):  # step backwards as elements become deleted
                if 0 < i < len(dp):  # necessary to check if elements become deleted
                    if dp[i-1][1] == dp[i][1] == dp[i+1][1]:
                        del dp[i]
            pass

    def __eq__(self, other):
        """
        operator "Equality"
        :param other:
        :return:
        """
        if self.DataPoints == other.DataPoints:
            return True
        else:
            return False

    def __hash__(self):
        """
        Hash key operator.
        :return:
        """
        hashstring = ""
        for dp in self.DataPoints:
            hashstring += str(dp[0]) + "," + str(dp[1])+"|"
        return hash(hashstring)





