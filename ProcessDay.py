
from DayFactory import DayFactory

NB_DAY = 5
LAST_DAY = True
SECOND_STAR = True


dayFactory = DayFactory(NB_DAY)
if LAST_DAY:
    day = dayFactory.get_day(NB_DAY)
    day.process_first_star()
    if SECOND_STAR:
        day = dayFactory.get_day(NB_DAY)
        day.process_second_star()
else:
    for i in range(1, NB_DAY+1):
        day = dayFactory.get_day(i)
        day.process_first_star()
        if SECOND_STAR:
            day = dayFactory.get_day(i)
            day.process_second_star()
