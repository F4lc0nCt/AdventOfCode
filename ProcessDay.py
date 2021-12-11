
import importlib
from DayFactory import DayFactory


NB_MAX_DAY = 25
LAST_DAY = False
SECOND_STAR = True

""" Get the number of Day implemented"""
for d in range(1, NB_MAX_DAY):
    day_name = "Day%d" % d
    try:
        getattr(importlib.import_module(day_name), day_name)
        nb_day = d
    except ModuleNotFoundError:
        break

dayFactory = DayFactory(nb_day)
if LAST_DAY:
    day = dayFactory.get_day(nb_day)
    day.process_first_star()
    if SECOND_STAR:
        day = dayFactory.get_day(nb_day)
        day.process_second_star()
else:
    for i in range(1, nb_day+1):
        day = dayFactory.get_day(i)
        day.process_first_star()
        if SECOND_STAR:
            day = dayFactory.get_day(i)
            day.process_second_star()
