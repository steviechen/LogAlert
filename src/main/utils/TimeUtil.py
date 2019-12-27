import time
import datetime
from datetime import timedelta

class Timeutil(object):
    def getTimestamp(self, x: str) -> int:
        print("input time is " + x)
        return int(time.mktime(time.strptime(str(x), '%Y-%m-%d %H:%M:%S')))

    def getDateRange(self,dateStart:str,dateEnd:str) -> list:
        date_list = []
        begin_date = datetime.datetime.strptime(dateStart, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(dateEnd, "%Y-%m-%d")
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y-%m-%d")
            date_list.append(date_str)
            begin_date += datetime.timedelta(days=1)
        return date_list

    def getYesterday(self) -> str:
        yesterday = datetime.datetime.today() + timedelta(-1)
        return str(yesterday.strftime('%Y-%m-%d'))

