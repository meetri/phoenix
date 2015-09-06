import os
import sys
import math
import enoch
import ephem
import starcalc
import mx.DateTime
import pytz

class Table(object):

    @staticmethod
    def chart_day_header ():
        return [["Earth","Moon","Enoch","DOW","Priest","day","Season","Rising","Moon Phase","Sun","Moon"]]

    @staticmethod
    def chart_day_divider(d):
        return [[d,"","","","","","","","","",""]]

    @staticmethod
    def chart_day_row ( e ):
        dow = starcalc.weekday( e.jd() )
        sun,date = starcalc.Earth.previous_azimuth ( e.djd, e.sun )
        goldate = "%s" % ( date )
        az = "%.2f" % ((sun.az * starcalc.RADIAN)-90.0)

        ny = e.newyear
        ny_season = int(ny * 4 / 364)
        season_day = ny - ( ny_season * 91 )


        return [[ e.djd, "%d/%d" % (e.moon.month,e.moon.monthday), "( %s ) %s" % (e.ead_date(),e.etd_date()), enoch.DayOfWeek[e.dayofweek],"[%d] %s" % ( e.week, enoch.Priests_Chronicals[e.week-1] ),"%d" % e.yearday,"%d.%d (%d)" % ( ny_season, season_day, ny) , az, "%.4f" % e.moon.ephem.moon_phase, ephem.constellation(e.sun)[1], ephem.constellation(e.moon.ephem)[1] ]]


    @staticmethod
    def day_header ():
        return  [["DJD","JD","EAD","ETD","Week","Priest","DOW","Year Day","New Year","Sun","Sunrise[G]","Sun Azimuth","Phase","Date","Total","YearDay","Constellation"]]

    @staticmethod
    def day_row ( e ):
        dow = starcalc.weekday( e.jd() )
        sun,date = starcalc.Earth.previous_azimuth ( e.djd, e.sun )
        goldate = "%s" % ( date )
        az = "%.2f" % (sun.az * starcalc.RADIAN)

        return [[e.djd,e.jd(),e.ead_date(),e.etd_date(),e.week,enoch.Priests_Chronicals[e.week-1], str(e.dayofweek+1) + ":" + enoch.DayOfWeek[e.dayofweek],int(e.yearday),int(e.newyear),ephem.constellation(e.sun)[1],goldate,az,"%.4f" % e.moon.ephem.moon_phase,"%d/%d" % (e.moon.month , e.moon.monthday), "%d/%d" % ( e.moon.monthlength, e.moon.months), "%d/%d" % ( e.moon.yearday , e.moon.yearlength ), ephem.constellation(e.moon.ephem)[1]]]


    @staticmethod
    def list_days(date = "epoch", count = 30, dayskip = 1, yearskip = 0, offset = 0, negoffset = 0, bc = False,readfile = False):

        datelist = None
        if ( readfile ):

            if os.path.isfile ( date ):
                with open(date) as f:
                    datelist = []
                    for line in f:

                        datelist += [line.replace("\n","") + " 12:00:00"]

        elif str(date).lower() == "epoch":
            edate = enoch.EpochDat
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


        if datelist is None:
            datelist = [edate]


        rows = Table.chart_day_header()
        for edate in datelist:

            e = enoch.Date( edate )

            if len(rows) > 2:
                rows += Table.chart_day_divider('---')

            if offset > 0 :
                e.next_day(offset)
            if negoffset > 0:
                e.prev_day(negoffset)

            #startday = e.djd
            startday = e.djd
            for year in range( count ):
                rows += Table.chart_day_row(e)

                if yearskip > 0:
                    e.next_year ( yearskip )
                else:
                    e.next_day(dayskip)

        starcalc.Columnize.cprint ( rows )





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

