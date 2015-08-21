import ephem, math, sys

RADIAN = 180 / 3.1415926
TZ_JERUSALEM = 2
TZ_PACIFIC = -7

def weekday( jd ):
    return int(jd % 7)

class Places(object):

    @staticmethod
    def home (date):
        loc = ephem.Observer()
        loc.lat = "38.162881"
        loc.lon = "-122.266138"
        loc.elevation = 46
        loc.date = date
        loc.pressure = 0
        return loc

    @staticmethod
    def golgotha(date):
        golgotha = ephem.Observer()
        golgotha.lat = "31.7811323"
        golgotha.lon = "35.2296886"
        golgotha.elevation = 2484
        golgotha.date = date
        golgotha.epoch = date
        golgotha.pressure = 0
        return golgotha

class Earth(object):

    @staticmethod
    def next_azimuth ( date , body ):
        golgotha = Places.golgotha( date )
        golgotha.date = golgotha.next_rising( body )
        body.compute ( golgotha )

        timedelta = mx.DateTime.TimeDelta(2,0,0)
        dd = mx.DateTime.Date ( * golgotha.date.tuple() ) + timedelta

        date = ephem.date ( "%d/%d/%d %d:%d:%d" % dd.tuple()[:6] )

        return body,date

    @staticmethod
    def previous_azimuth ( date , body ):
        golgotha = Places.golgotha( date )
        golgotha.date = golgotha.previous_rising( body )
        body.compute ( golgotha )

        timedelta = ephem.hour * TZ_JERUSALEM
        date = ephem.Date( golgotha.date + timedelta )


        return body,date



    @staticmethod
    def get_moon_year(date,ignoreTime = True ):
        pve = ephem.previous_vernal_equinox(date)
        nve = ephem.next_vernal_equinox(pve)
        fnm = pnm = ephem.next_new_moon(math.floor(pve))

        # check if date is still in previous lunar year
        if date < fnm:
            nve = pve
            pve = ephem.previous_vernal_equinox(nve)
            fnm = pnm = ephem.next_new_moon(math.floor(pve))

        #print str(date) + " : " + str(pve) + " : " + str(nve)
        nm = pve
        moonyear = []
        while nm < nve:
            nm = ephem.next_new_moon(pnm)
            if ignoreTime:
                moonyear += [ math.floor(nm)-math.floor(pnm) ]
            else:
                moonyear += [ round(nm-pnm) ]

            pnm = nm

        return (moonyear,fnm,nm)


class Columnize(object):

    @staticmethod
    def cprint(list):
        margin=4
        colwidth = {}
        for row in list:
            for idx, col in enumerate(row):
                if idx not in colwidth:
                    colwidth[idx] = []
                colwidth[idx].append(len(str(col))+margin)

        maxwidth = {}
        for idx in colwidth:
            maxwidth[idx] = max(colwidth[idx])

        for row in list:
            for idx,col in enumerate(row):
                print ( str(col).ljust( maxwidth[idx] ) ),
            print ""
