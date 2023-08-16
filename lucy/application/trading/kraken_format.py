from datetime import datetime

def dtm(datetime_string: str) -> datetime:
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    return datetime.strptime(datetime_string, date_format)