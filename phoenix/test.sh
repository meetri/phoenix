#!/usr/local/bin/python
import sys, ephem, starcalc,enoch

e = enoch.Date("-7/9/23 12:00:00")

rows = [] 
list_header = [["Date","DJD","JD","EnochDate","Week","Priest","DOW","Sun","Phase","Date","Total","YearDay","Constellation"]]
for year in range(0,30):
    #localtime = ephem.localtime(e.djd)
    dow = starcalc.weekday( e.jd() )
    rows += [[e.djd,e.djd,e.jd(),e.etd_date(),e.week,enoch.Priests_Chronicals[e.week-1], str(dow) + ":" + str(e.dayofweek) + ":" + enoch.DayOfWeek[e.dayofweek],ephem.constellation(e.sun)[1],"%.4f" % e.moon.ephem.moon_phase,"%d/%d" % (e.moon.month , e.moon.monthday), "%d/%d" % ( e.moon.monthlength, e.moon.months), "%d/%d" % ( e.moon.yearday , e.moon.yearlength ), ephem.constellation(e.moon.ephem)[1]]]
    e.next_day()

starcalc.Columnize.cprint ( list_header + rows )
