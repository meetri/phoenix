#!/usr/local/bin/python
import sys,math, ephem, starcalc,enoch, search, mx.DateTime

# get list of potential cycle start dates
e = enoch.Date("-10000/1/1" )
eqlist = [] 
for count in range(0,100):
    e = search.Date.next_ve_nm( e, dow=3 )
    eqlist += [ e.djd ]

# build date groups of interest
datelist = []

# Date Jesus was born based on Revelation 12 ( 
# sun clothed the virgin and the moon at her feet )
#d = ephem.Date("-7/9/23 11:40:37")
d = ephem.Date("-7/9/23 12:00:00")

# 6 months when priest zacariah had vision about his son john in week of Abijah
datelist += [ephem.Date(d-278-180)]

# 9 months + 5 days ( 91*3+5 ? or 90*3=5 ) -- ( lefafa sedek ) jesus conception
datelist += [ephem.Date(d-278)]

# -7/9/23 Jesus Birthdate
datelist += [d]

header = search.Table.day_header()
for eq in eqlist:
    #change enoch epochdate
    enoch.EpochDate = str(eq)
    rows = []
    list = []
    for year in datelist:
        e = enoch.Date ( year )
        row = search.Table.day_row(e)
        rows += row
        list += [row[0][5]]

    if list[0] == "Abijah" and list[1] == "Jeshua" and list[2] == "Jehoiarib":
        print "\nEpoch: %s" % (enoch.EpochDate)
        starcalc.Columnize.cprint ( header + rows )


'''
for year in range(0,11000):
    ve = ephem.next_vernal_equinox( ve )
    nm = ephem.next_new_moon( math.floor(ve) )
    df = math.fabs(ve-nm)
    if df < 1:
        e.set( nm )
        dow = starcalc.weekday( e.jd() )
        if dow == 2:
            datelist += [ e.djd ]

print "dates that match formula:"
print datelist
for date in datelist:


starcalc.Columnize.cprint ( list_header + rows )
'''
