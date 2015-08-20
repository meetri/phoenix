'''
Enoch Calculator
by: Demetrius A. Bell <meetri@gmail.com>
2015
'''
import ephem
import starcalc
import math

#EpochDate = "-7/9/23"
#EpochDate = "-9999/6/5"
#EpochDate = "-8693/5/27"
EpochDate = "-5269/5/3 12:00:00"

# the twelve portals 6 = summer solstice, 1 = winter solstice
Portal = (4,5,6,-6,-5,-4,-3,-2,-1,1,2,3)

# the month number
Months = (1,2,3,4,5,6,7,8,9,10,11,12)

# the day count for when each portal begins ( zero aligned )
PortalDays = (0,30,60,91,121,151,182,212,242,273,303,333)

#DayOfWeek = ("Wednesday","Thursday","Friday","Saturday","Sunday","Monday","Tuesday")
DayOfWeek = ("Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday")
DayOfWeek2 = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")

# order given in chronicals
Priests_Chronicals = ("Jehoiarib","Jedaiah","Harim","Seorim","Malchijah","Mijamin","Hakkoz","Abijah","Jeshua","Shecaniah","Eliashib","Jakim","Huppah","Jeshebeab","Bilgaha","Immer","Hezir","Happizzez","Pethahiah","Jehezkel","Jachin","Gamul","Delaiah","Maaziah")

# order implied by the Qumran Scrolls
Priests_Qumran = ("Gamul","Delaiah","Maaziah","Jehoiarib","Jedaiah","Harim","Seorim","Malchijah","Mijamin","Hakkoz","Abijah","Jeshua","Shecaniah","eliashib","Jakim","Huppah","Jeshebeab","Bilgaha","Immer","Hezir","Happizzez","Pethahiah","Jehezkel","Jachin")

# what works ...
Priests = ("Delaiah","Maaziah","Jehoiarib","Jedaiah","Harim","Seorim","Malchijah","Mijamin","Hakkoz","Abijah","Jeshua","Shecaniah","Eliashib","Jakim","Huppah","Jeshebeab","Bilgaha","Immer","Hezir","Happizzez","Pethahiah","Jehezkel","Jachin","Gamul")


class Time(object):

    def __init__(self, timestr ):
        self.moment = 0


class Moon(object):

    def __init__( self, date ):
        self.date = date
        self.ephem = ephem.Moon( date.djd )

        moonyear = starcalc.Earth.get_moon_year( date.djd )
        self.yearmonths = moonyear[0]
        self.yearstart = moonyear[1]
        self.yearday = int(date.djd - self.yearstart)
        self.months = len(self.yearmonths)
        self.yearlength = int(sum( self.yearmonths ))

        self.yearday += 1

        s = 0
        for idx,days in enumerate(self.yearmonths):
            s += days
            if self.yearday <= s:
                self.month = idx + 1
                self.monthlength = int(days)
                self.monthday = int(days - (s - self.yearday))
                break



class Date(object):

    # when Christ was born ( Revelations 12 )

    def __init__(self, date = None ):

        # TODO: the vernal equinox of the epoch year
        self.epoch = 0

        # number of days since the epoch
        self.daycount = 0

        # which week in the 24 week cycle
        self.week = 0

        # which day in the 7 day cycle
        self.dayofweek = 0

        # the year day that marks the beginning of the 364 day cycle
        self.newyear = 0

        # the current day in the year
        self.yearday = 0

        # the actual day of the year in relation to the sun's cycle
        self.translatedday = 0

        # the year day converted to an angle in 360 degrees
        self.dayangle = 0

        # the year in the 294 year cycle
        self.year = 0

        # the number of completed 294 year cycles since the epoch
        self.cycle = 0

        # the portal / window the sun is in
        self.portal = 0

        # the month in the 12 month yearly cycle
        self.month = 0

        # the day in the 364 day yearly cycle
        self.day = 0

        # date in dublin julian date format
        self.djd = 0

        # enoch moon
        self.moon = None

        # ephem sun
        self.sun = None

        self.dayshift = 0

        # set default epoch
        self.set_epoch ( EpochDate )

        if date is not None:
            self.set(date)

    def __str__(self):
        return "daycount: %d, numweeks: %d, week: %d, year: %d, cycle: %d, yearday: %d, dayangle: %f, newyear: %d, translatedday: %d, month_day: %d, portal: %d, month: %d, dayshift: %f " % (self.daycount, self.numweeks,self.week,self.year,self.cycle,self.yearday,self.dayangle,self.newyear,self.translatedday,self.month_day,self.portal,self.month,self.dayshift)


    def set_epoch ( self, date ):
        '''find the vernal equinox day where new moon 1 lunar month before the ve equinox and on a wednesday'''

        self.epoch = ephem.Date ( date )

    def get_portal ( self, yearday ):
        for idx,startday in enumerate(reversed(PortalDays)):
            if yearday > startday:
                day = yearday - startday
                portal = Portal[11-idx]
                month = Months[11-idx]
                return {"day":day,"portal":portal,"month":month}

    def etd_date( self ):
        return "%d/%d/%d/%d" % ( self.cycle,self.year,self.t_month,self.t_month_day)

    def ead_date( self ):
        return "%d/%d" % ( self.month,self.month_day)

    def calculate( self ):
        numyears = math.floor( self.daycount / 364 )
        cycle = math.floor(numyears/294)
        year = numyears % 294

        # offset to the 3rd day ( wednesday ). Sun was created on 3rd day
        self.numweeks = math.floor ( (self.daycount + 3 ) / 7 )
        self.dayofweek = int((self.daycount + 3 ) % 7)
        self.yearday = self.daycount - ((cycle*294*364) + (year*364))
        self.dayangle = round ( (360 * self.yearday) / 364, 2 )
        self.newyear =  ( 364 - math.ceil ( (364*year) / 294 )  ) % 364
        self.translatedday = ( self.yearday + self.newyear ) % 364
        self.week = int(self.numweeks % 24)

        self.dayshift = ( 364 - self.newyear ) % 364

        if cycle >= 0:
            self.cycle = cycle+1
        else:
            self.cycle = cycle

        self.year = year+1
        self.newyear += 1
        self.yearday += 1
        self.week += 1
        self.translatedday += 1

        data = self.get_portal ( self.yearday )
        self.month_day = data["day"]
        self.portal = data["portal"]
        self.month = data["month"]

        data = self.get_portal ( self.translatedday )
        self.t_month_day = data["day"]
        self.t_portal = data["portal"]
        self.t_month = data["month"]

        self.moon = Moon ( self )
        self.sun = ephem.Sun ( self.djd )


    def next_day(self,numDays = 1):
        self.daycount+=numDays
        self.djd = ephem.Date(self.daycount + self.epoch)
        return self.calculate()

    def prev_day(self,numDays = 1):
        return self.next_day ( -1 * numDays )


    def next_week(self,numWeeks = 1):
        return self.next_day(7*numWeeks)


    def prev_week(self,numWeeks = 1):
        return self.next_day(-7*numWeeks)


    def next_year(self, numYears = 1 ):
        year = self.year + numYears
        cycle = self.cycle
        return self.set_etd ( self.cycle, year, self.t_month, self.t_month_day )


    def prev_year(self,numYears = 1):
        return self.next_day(-364*numYears)


    def set_enoch_day ( self, date ):
        self.djd = date
        self.daycount =  math.floor(date - self.epoch)


    def set_etd ( self, cycle, year, month, day ):
        if year > 294:
            cycle += 1
            year = year-294

        cycle-=1
        year-=1
        month-=1
        day-=1

        newyear =  ( math.ceil ( (364*year) / 294 )  ) % 364
        yearday = (PortalDays[month] + day + newyear ) % 364

        enochyears = 294*cycle+year
        enochday = enochyears * 364 + yearday

        date = ephem.Date(enochday + self.epoch )
        self.set_enoch_day ( date )
        self.calculate()


    def jd(self):
        return int(round(self.djd + 2415020,0))


    def set( self, datestr = None, julianday = None ):
        if datestr is None and julianday is None:
            datestr = EpochDate

        if julianday is not None:
            self.set_enoch_day ( ephem.Date(julianDay - 2415020) )
        elif type(datestr) is str:
            self.set_enoch_day ( ephem.Date ( datestr) )
        elif type(datestr) is ephem.Date:
            self.set_enoch_day ( datestr )
        else:
            self.set_enoch_day ( ephem.Date(datestr) )

        return self.calculate()


'''

    def jd():

    def next_day():

    def prev_day():

    def ead():

    def etd():


'''

class Places(object):

    @staticmethod
    def golgotha():
        golgotha = ephem.Observer()
        golgotha.lat = 31.7811323
        golgotha.lon = 35.2296886
        golgotha.elevation = 2484
        return golgotha
