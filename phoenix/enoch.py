'''
Enoch Calculator
by: Demetrius A. Bell <meetri@gmail.com>
2015
'''
import ephem
import enochephem
#import starcalc
import math
#import datetime
#import time
#import pytz
#import tzlocal

#EpochDate = "-7/9/23"
#EpochDate = "-9999/6/5"
#EpochDate = "-8693/5/27"
EpochDate = "-5269/5/3 12:00:00"
#EpochDate = "-5269/5/3 00:00:00"
#EpochDate = "-5269/5/3"
#EpochDate = "-10629/6/9 12:00:00"

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

    def __init__(self, enoch ):
        self.moment = 0
        self.degree = 0
        self.part = 0
        self.part_seg = 0
        self.enoch = enoch
        self.time = 0
        self.set_time()

    def get_time( self ):

        sr_secs = self.enoch.time.time_to_seconds(self.enoch.time.sun_rising)
        now_secs = self.enoch.time.time_to_seconds( ephem.now() )

        print "srsecs = %d, nowsecs = %d" % ( sr_secs, now_secs )

    def set_time( self, time = 0 ):
        if time == 0:
            time = self.enoch.djd


        local = self.enoch.time.tm.localtime ( time )
        local_secs = self.enoch.time.time_to_seconds ( local )
        local_sunrise = self.enoch.time.tm.localtime ( self.enoch.time.sun_rising )
        sunrise_secs = self.enoch.time.time_to_seconds ( local_sunrise )

        #if it's after midnight ...
        if local_secs < sunrise_secs:
            dif = 86400 - ( sunrise_secs - local_secs )
        else:
            dif = local_secs - sunrise_secs

        part = dif * 18 / 86400
        seg_secs = (part - int(part)) * 1200
        seg = int(seg_secs / 60 )
        mom = int(seg_secs - ( seg * 60 ))

        deg = int(dif / 240 )

        self.part = int(part)
        self.part_seg = seg
        self.moment = mom
        self.degree = deg

        return int(part),seg,deg,mom







class Date(object):

    # when Christ was born ( Revelations 12 )

    def __init__(self, date = None ):

        # TODO: the vernal equinox of the epoch year
        self.epoch = 0

        # priest in service
        self.priest = ""

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
        return "daycount: %d, numweeks: %d, week: %d, year: %d, cycle: %d, yearday: %d, dayangle: %f, newyear: %d, translatedday: %d, month_day: %d, portal: %d, month: %d, dayshift: %f, priest: %s " % (self.daycount, self.numweeks,self.week,self.year,self.cycle,self.yearday,self.dayangle,self.newyear,self.translatedday,self.month_day,self.portal,self.month,self.dayshift,self.priest)


    def set_epoch ( self, date ):
        '''find the vernal equinox day where new moon 1 lunar month before the ve equinox and on a wednesday'''

        self.epoch = ephem.Date ( date )
        #print "epoch = " + str(self.epoch)

    def get_portal ( self, yearday ):
        for idx,startday in enumerate(reversed(PortalDays)):
            if yearday > startday:
                day = yearday - startday
                portal = Portal[11-idx]
                month = Months[11-idx]
                return {"day":day,"portal":portal,"month":month}

    def etd_date( self ):
        return "%d/%d" % ( self.t_month,self.t_month_day)
        #return "%d/%d/%d/%d" % ( self.cycle,self.year,self.t_month,self.t_month_day)

    def etd_extended_date( self ):
        return "%d/%d/%d/%d" % ( self.t_month,self.t_month_day,self.year,self.cycle)
        #return "%d/%d/%d/%d" % ( self.cycle,self.year,self.t_month,self.t_month_day)

    def ead_date( self ):
        return "%d/%d/%d/%d" % ( self.month,self.month_day,self.year,self.cycle)

    def dayinyear( self ):
        return (self.yearday + self.newyear - 1 ) % 364

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


        self.year = int(year+1)
        self.newyear = int(self.newyear+1)
        self.yearday = int(self.yearday+1)
        self.week = int(self.week+1)
        self.translatedday = int(self.translatedday+1)

        self.priest = Priests_Chronicals[ self.week - 1 ]
        self.week_name = DayOfWeek[self.dayofweek]

        data = self.get_portal ( self.yearday )
        self.month_day = data["day"]
        self.portal = data["portal"]
        self.month = data["month"]

        data = self.get_portal ( self.translatedday )
        self.t_month_day = data["day"]
        self.t_portal = data["portal"]
        self.t_month = data["month"]

        self.cycle = int(self.cycle)

        #ephem objects

        self.loc = enochephem.Places.sanfrancisco ( self.djd )
        self.loc.date = self.djd
        #self.loc = enochephem.Places.golgotha( self.djd )
        self.moon = enochephem.Moon ( self )
        self.sun = ephem.Sun ( self.djd )
        self.sun.compute( self.djd )
        self.cosmos = enochephem.Cosmos()

        self.time = enochephem.Time ( self.loc, self )
        self.clock = Time( self )


    def next_day(self,numDays = 1):
        #self.daycount+=numDays
        #self.djd = ephem.Date(self.daycount + self.epoch)
        self.djd = ephem.Date(self.djd + numDays )
        return self.calculate()

    def prev_day(self,numDays = 1):
        return self.next_day ( -1 * numDays )


    def next_week(self,numWeeks = 1):
        return self.next_day(7*numWeeks)


    def prev_week(self,numWeeks = 1):
        return self.next_day(-7*numWeeks)


    def next_year(self, numYears = 1 ):
        year = self.year + numYears
        time = self.djd - int(self.djd)
        self.set_etd ( self.cycle, year, self.t_month, self.t_month_day , time )



    def prev_year(self,numYears = 1):
        return self.next_year ( numYears * -1 )


    def set_enoch_day ( self, date ):
        self.djd = date
        self.daycount =  math.floor(date - self.epoch)


    def set_etd ( self, cycle, year, month, day, time = 0  ):
        if year > 294:
            cycle += 1
            year = year-294

        cycle-=1
        year-=1
        month-=1

        # not sure what 21 has to do with this...
        if year % 21 == 0:
            day-=1

        newyear =  ( math.ceil ( (364*year) / 294 )  ) % 364
        yearday = (PortalDays[month] + day + newyear ) % 364

        #print "pm = %d, day = %d, newyear = %d, yearday: %d" % ( PortalDays[month], day, newyear, yearday )

        enochyears = 294*cycle+year
        enochday = enochyears * 364 + yearday

        time = 0
        date = ephem.Date(enochday + self.epoch + time  )

        print "etd date %s " % str(date)

        self.set_enoch_day ( date )
        self.calculate()

        self.clock.get_time()

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



