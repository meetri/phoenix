import sys
import math
import enoch
import ephem
import starcalc
import mx.DateTime
import pytz

class Table(object):

    @staticmethod
    def day_header ():
        return  [["DJD","JD","EAD","ETD","Week","Priest","DOW","Sun","Pos","Phase","Date","Total","YearDay","Constellation"]]

    @staticmethod
    def list_days(date = "epoch", count = 30, dayskip = 1, yearskip = 0, offset = 0, negoffset = 0, bc = False):

        if str(date).lower() == "epoch":
            edate = enoch.EpochDate
        elif str(date).lower() == "now":
            edate = ephem.now()
        elif str(date).lower() == "priest":
            edate = "-8/6/23 12:00:00"
        elif str(date).lower() == "conception":
            edate = "-8/12/19 12:00:00"
        elif str(date).lower() == "birth":
            edate = "-7/9/23 12:00:00"
        else:
            if bc:
                date = "-" + date
            edate = "%s 12:00:00" % ( str(date) )

        e = enoch.Date( edate )

        if offset > 0 :
            e.next_day(offset)
        if negoffset > 0:
            e.prev_day(negoffset)

        #startday = e.djd
        startday = e.djd
        rows = Table.day_header()
        for year in range( count ):
            rows += Table.day_row(e)

            if yearskip > 0:
                e.next_year ( yearskip )
            else:
                e.next_day(dayskip)

        starcalc.Columnize.cprint ( rows )



    @staticmethod
    def day_row ( e ):
        dow = starcalc.weekday( e.jd() )

        sun,date = starcalc.Earth.previous_azimuth ( e.djd, e.sun )

        sunPos = "%s / %.2f" % ( date, sun.az * starcalc.RADIAN )

        return [[e.djd,e.jd(),e.ead_date(),e.etd_date(),e.week,enoch.Priests_Chronicals[e.week-1], str(dow) + ":" + str(e.dayofweek) + ":" + enoch.DayOfWeek[e.dayofweek],ephem.constellation(e.sun)[1],sunPos,"%.4f" % e.moon.ephem.moon_phase,"%d/%d" % (e.moon.month , e.moon.monthday), "%d/%d" % ( e.moon.monthlength, e.moon.months), "%d/%d" % ( e.moon.yearday , e.moon.yearlength ), ephem.constellation(e.moon.ephem)[1]]]


class Date(object):

    @staticmethod
    def next_ve_nm( date, accuracy = 1, dow = None ):
        "get next vernal equinox when the same as a new moon when on a wednesday"

        if type(date) is enoch.Date:
            e = date
        else:
            e = enoch.Date ( date )

        ve = e.djd
        nm = 0
        found = False
        while not found:
            ve = ephem.next_vernal_equinox ( ve )
            nm = ephem.next_new_moon ( math.floor(ve))
            df = math.fabs(ve-nm)
            if df < accuracy:
                e.set ( nm )
                if dow is not None:
                    if e.dayofweek == dow:
                        found = True
                else:
                    found = True

        return {"ve":ve,"enoch":e}
