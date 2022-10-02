# import datetime
# import calendar
#
#
# def weekday_count(start, end):
#     start_date = datetime.datetime.strptime(start, '%d/%m/%Y')
#     end_date = datetime.datetime.strptime(end, '%d/%m/%Y')
#     week = {}
#     for i in range((end_date - start_date).days):
#         day = calendar.day_name[(start_date + datetime.timedelta(days=i + 1)).weekday()]
#         week[day] = week[day] + 1 if day in week else 1
#     return week
#
#
# print(weekday_count("01/01/2017", "31/01/2017"))


# from datetime import date
# from datetime import timedelta
#
# MON, TUE, WED, THU, FRI, SAT, SUN = range(7)
#
# def lastWday(adate, w):
#      """Mon:w=0, Sun:w=6"""
#      delta = (adate.weekday() + 6 - w) % 7 + 1
#      return adate - timedelta(days=delta)
#
# for x in range(3, 16):
#      # start = date(year=2021, month=11, day=x)
#      start = date(2021-11-5)
#      prev = lastWday(start, WED)
#      print(start, start.weekday(), prev, prev.weekday())


# import Python's datetime module

import datetime

# weekdays as a tuple

weekDays = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

# Find out what day of the week is this year's Christmas


thisXMas = datetime.date(2017, 12, 25)

thisXMasDay = thisXMas.weekday()

thisXMasDayAsString = weekDays[thisXMasDay]

print("This year's Christmas is on a {}".format(thisXMasDayAsString))

# Find out what day of the week next new year is

nextNewYear = datetime.date(2021, 11, 5)

nextNewYearDay = nextNewYear.weekday()
print(nextNewYearDay)

nextNewYearDayAsString = weekDays[nextNewYearDay]

print("Next new year is on a {}".format(nextNewYearDayAsString))