from datetime import datetime


class Interval(object):
    '''Interval in minutes'''
    allowed_intervals = {1: "1m", 5: "5m", 15: "15m", 30: "30m",
                         60: "1h", 240: "4h", 720: "12h",
                         1440: "1d", 10080: "1w"}

    def __init__(self, interval):
        '''
        'interval': Can be one of the following:
            int: 1 5 15 30 60 240 1440 10080\n
            str: "1m" "5m" "15m" "30m" "1h" "4h" "12h" "1d" "1w"
        '''
        if isinstance(interval, int):
            if interval in self.allowed_intervals.keys():
                self.interval = interval
        elif isinstance(interval, str):
            x = [k for k, v in self.allowed_intervals.items() if v == interval]
            if any(x):
                self.interval = x[0]
            else:
                try:
                    i = int(interval)
                    if i in self.allowed_intervals.keys():
                        self.interval = i
                except:
                    raise ValueError(f"Interval {interval} is not allowed")
        else:
            raise ValueError(f"Interval {interval} is not allowed")

    def __str__(self):
        postfix = f" ({self.allowed_intervals[self.interval]})"
        postfix = postfix if self.interval >= 60 else ""
        return f"{str(self.interval)}m{postfix}"

    def __repr__(self):
        return str(self.interval)

    def __eq__(self, other):
        if isinstance(other, int):
            return self.interval == other
        return self.interval == other.interval

    def resolution(self) -> str:
        '''
        Returns the resolution of the interval in shorthand notation:
        (1m, 5m, 15m, 30m, 1h, 4h, 12h, 1d, 1w)'''
        return self.allowed_intervals[self.interval]

    @staticmethod
    def ONE_MINUTE():
        return Interval(1)

    def FIVE_MINUTES():
        return Interval(5)

    def FIFTEEN_MINUTES():
        return Interval(15)

    def THIRTEE_MINUTES():
        return Interval(30)

    def ONE_HOUR():
        return Interval(60)

    def FOUR_HOURS():
        return Interval(240)

    def TWELVE_HOURS():
        return Interval(720)

    def ONE_DAY():
        return Interval(1440)

    def ONE_WEEK():
        return Interval(10080)


class Intervals(object):
    '''Þau intervals sem eru í boði fyrir núverandi tíma'''

    def __init__(self, now: datetime):
        self.intervals = []
        self.now = now
        one = now.minute % 1 == 0
        five = now.minute % 5 == 0
        fifteen = now.minute % 15 == 0
        thirty = now.minute % 30 == 0
        sixty = now.minute % 60 == 0
        two_fourty = now.minute % 60 == 0 and now.hour % 4 == 0
        day = now.minute % 60 == 0 and now.hour % 24 == 0
        if one:
            self.intervals.append(Interval(1))
        if five:
            self.intervals.append(Interval(5))
        if fifteen:
            self.intervals.append(Interval(15))
        if thirty:
            self.intervals.append(Interval(30))
        if sixty:
            self.intervals.append(Interval(60))
        if two_fourty:
            self.intervals.append(Interval(240))
        if day:
            self.intervals.append(Interval(1440))

    def __contains__(self, interval: Interval):
        return interval in self.intervals

    def has(self, interval: Interval):
        return interval in self.intervals

