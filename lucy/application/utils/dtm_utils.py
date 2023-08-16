from datetime import datetime, timedelta

from lucy.model.interval import Interval

def dtm_from_kraken(t: str) -> datetime:
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    return datetime.strptime(t, date_format)

def since_days(days: int):
    return int( (datetime.now() - timedelta(days=days)).timestamp() )

def since_hours(hours: int):
    return int( (datetime.now() - timedelta(hours=hours)).timestamp() )

def since_max_candles(interval: Interval) -> int:
    max = 500  # max rows that are returned from kraken
    # max = 5000  # max rows that are returned from kraken
    val = interval.interval

    if val < 60:
        return int( (datetime.now() - timedelta(minutes=max*val)).timestamp() )
    
    if val < 1440:
        hr = val / 60
        return int( (datetime.now() - timedelta(hours=max*hr)).timestamp() )
    
    if val < 10080:
        days = val / 1440
        return int( (datetime.now() - timedelta(days=max*days)).timestamp() )
    
    if val == 10080:
        weeks = 52 * 10
        return int( (datetime.now() - timedelta(weeks=weeks)).timestamp() )
