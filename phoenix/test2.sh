#!/usr/local/bin/python
import math, ephem, starcalc,enoch

#e = enoch.Date( enoch.EpochDate )
e = enoch.Date ( "-10000/1/1" )
ve = e.djd

rows = [] 
list_header = [["Dif","EAD","nEquinox","JD","DOW","New Moon","Phase","Lunar Date","Lunar Month"]]
last_date = None
for year in range(0,11000):
    ve = ephem.next_vernal_equinox( ve )
    #ve = ephem.next_equinox( ve )
    nm = ephem.next_new_moon( math.floor(ve) )
    df = math.fabs(ve-nm)
    if df < 1:
        e.set( nm )
        dow = starcalc.weekday( e.jd() )
        if dow == 2:
            if last_date != None:
                ldif = math.floor((math.floor(e.djd) - math.floor(last_date)) / 364)
            else:
                ldif = 0

            rows += [[ldif,e.ead_date(),e.djd,e.jd(),enoch.DayOfWeek2[dow],nm,"%.2f" % e.moon.ephem.moon_phase,"%d/%d:%d" % (e.moon.month,e.moon.monthday,e.moon.yearday),"%d:%d" % (e.moon.monthlength,e.moon.months)]]
            last_date = e.djd

starcalc.Columnize.cprint ( list_header + rows )
