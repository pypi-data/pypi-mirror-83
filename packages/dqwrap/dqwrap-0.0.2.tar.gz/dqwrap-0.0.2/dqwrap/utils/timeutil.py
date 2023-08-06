import time, os
from datetime import timezone, timedelta


def get_sys_timezone():
    tz = os.environ.get("TZ")
    if tz is not None:
        return timezone(timedelta(hours=int(tz)))
    return timezone(timedelta(hours=-time.timezone // 3600))


SYSTEM_TIMEZONE = get_sys_timezone()
