#!/usr/local/bin/python
import sys
import ephem

sun = ephem.Sun()
golgotha = ephem.Observer()
golgotha.lat = 31.7811323
golgotha.lon = 35.2296886
golgotha.elevation = 2484
import enoch

ve = ephem.next_vernal_equinox( '-5500' )
golgotha.date = int(ve)
sr = golgotha.next_rising(sun)
print ve
print sr

#sys.exit()

for priest in enoch.Priests:
    print "priest: " + priest

daysofweek=('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')


home = ephem.Observer()
home.lat = 38.162881
home.lon = -122.266138
home.elevation = 46

d = "2000"
ve = ephem.next_vernal_equinox( d )
dif = 0
p = None
lm = 0
for idx in range(0,100):
    d = ephem.next_new_moon(d)
    home.date = int(d)
    s = home.next_rising(sun)

    if s > ve:
        ve = ephem.next_vernal_equinox( s )
        lm = 0

    lm+=1
    if p is not None:
        dif = ( s - p )

    p = s

    print "%d\t%d\t-\t%s" % (lm, dif, ephem.localtime(s) )


    #print "%d - %d,%d, date: %s, next sunrise: %s" % (lm, dif2, dif, d, s )



dl = "-7"
for idx in range(0,2):
    dl = ephem.next_equinox(dl)
    moon = ephem.Moon(dl)
    d = dl.datetime()

    abr,const_name = ephem.constellation( moon )
    #print "constellation: %s dow: %s date: %s - GEOCENTRIC(%d,%d), Phase: %d " % ( const_name, daysofweek[d.weekday()], dl, moon.hlat,moon.hlon, moon.moon_phase )
    print """
Date: %s : %s
Moon Phase: %f / Constellation: %s
Lat: %f, Long: %f""" % ( dl , daysofweek[d.weekday()],moon.moon_phase,const_name,moon.hlat, moon.hlon, )
