'''Enoch Ephemeris Tools'''

import ephem
import starcalc
import math
import datetime
import time
import pytz
import tzlocal

class Cosmos(object):

    def __init__( self ):
        self.sun = Sun

    def constellation(self, body ):

        boundaries = {
                    28.687 : "Pisces",
                    53.417 : "Aries",
                    90.140 : "Taurus",
                    117.988 : "Gemini",
                    138.038 : "Cancer",
                    173.851 : "Leo",
                    217.810 : "Virgo",
                    241.047 : "Libra",
                    247.638 : "Scorpius",
                    266.238 : "Ophiuchus",
                    299.656 : "Sagittarius",
                    327.488 : "Capricornus",
                    351.650 : "Aquarius",
                }

        lon = ephem.Ecliptic(body).lon * 57.295779513

        prev = 0
        name = "Pisces"
        delta = 0
        dif = 0
        cdeg = 0
        for idx,deg in enumerate( sorted ( boundaries )):
            if deg > lon:
                if prev > 0:
                    name =  boundaries[deg]

                delta = lon - prev
                dif = deg-prev
                cdeg = delta * 100 / dif
                break

            prev = deg

        return name, int(cdeg), round(lon,2)
        #return "%s[%d]" % ( name, cdeg )

    @staticmethod
    def previous_azimuth ( enoch , body ):
        enoch.loc.date = enoch.loc.previous_rising( body )
        body.compute ( enoch.loc )

        deg = body.az * 57.29578049044297
        return round(deg,2)

class TimeManager(object):

    def __init__(self, timezone = None,dt_format = None):

        if dt_format:
            self.dateFormat = dt_format
        else:
            self.dateFormat = "%Y/%m/%d %H:%M:%S"

        if timezone:
            self.tz = pytz.timezone( timezone )
        else:
            self.tz = pytz.timezone (tzlocal.get_localzone().zone)

    def timedif(self, date_in ):
        date_utc = ephem.Date ( date_in )
        date_local = ephem.Date( self.localtime ( date_utc ) )
        return date_utc - date_local


    def localtime(self, date_in,timeOnly = False,dateOnly = False):

        temp_date,orig_year = TimeManager.replace_year(2000,date_in)
        naive = datetime.datetime.strptime ( str(temp_date), self.dateFormat )
        localt = ephem.Date(naive.replace(tzinfo=pytz.utc).astimezone(self.tz))

        yeardif = localt.tuple()[0] - 2000
        orig_year += yeardif

        out = TimeManager.replace_year( orig_year, localt )[0]
        if timeOnly:
            out = str(out).split(" ")[1]
        elif dateOnly:
            out = str(out).split(" ")[0]

        return out

    def utc(self, date_in ):
        temp_date,orig_year = TimeManager.replace_year(2000,date_in)
        naive = datetime.datetime.strptime ( str(temp_date), self.dateFormat )
        local_dt = self.tz.localize(naive, is_dst=None)
        utc_dt = ephem.Date(local_dt.astimezone (pytz.utc))

        yeardif = utc_dt.tuple()[0] - 2000
        orig_year += yeardif

        return TimeManager.replace_year( orig_year, utc_dt )[0]


    @staticmethod
    def replace_year( year, date_in ):
        dt = ephem.Date ( date_in ).tuple()
        tempDate = "%d/%d/%d %d:%d:%d" % ( year,dt[1],dt[2],dt[3],dt[4],dt[5])
        newdate = ephem.Date ( tempDate )

        return newdate, dt[0]


class Time(object):

    def __init__(self, loc, enoch ):
        self.moment = 0
        self.degree = 0
        self.part = 0
        self.part_degree = 0
        self.sun_rising = 0
        self.sun_setting = 0
        self.location = loc
        self.enoch = enoch
        self.tm = TimeManager()
        self.set()

    def convert_time( self, date_in, display = False, local=True ):

        if local:
            now = self.tm.localtime( date_in )
            sr = self.tm.localtime(self.sun_rising)
        else:
            now = date_in
            sr = self.sun_rising

        now_secs = Time.time_to_seconds ( now )
        sr_secs = Time.time_to_seconds ( sr )

        cur_time = now_secs - sr_secs
        moment = cur_time / 4
        time = int(moment / 60)
        moment = abs(int( ( time * 60 ) - moment ))

        if display:
            return "%d.%d" % ( time, moment )
        else:
            return moment, time


    def get_time(self, display = False, local=True):
        return self.convert_time ( self.enoch.djd, display,local )


    def daylight_ratio(self, scale ):
        rt = self.localtime( self.sun_rising )
        rsecs = Time.time_to_seconds ( rt )

        st = self.localtime ( self.sun_setting )
        ssecs = Time.time_to_seconds ( st )

        return round((( ssecs - rsecs ) * scale) / 86400,2)

    def set (self):

        #adjust the date object to where it falls in the middle of sunrise and sun setting
        sunephem = ephem.Sun( self.enoch.djd )
        sunephem.compute( self.enoch.djd )
        self.sun_rising = self.location.previous_rising( sunephem )
        print "sr = %s, today = %s" % ( self.sun_rising, self.enoch.djd )

        tloc = ephem.Observer()
        tloc.lat = self.location.lat
        tloc.lon = self.location.lon
        tloc.elevation = self.location.elevation
        tloc.date = self.sun_rising

        self.sun_setting = tloc.next_setting ( ephem.Sun() )

        #update time based on timezone of location


    def localtime ( self, date_in ):
        return self.tm.localtime ( date_in )


    @staticmethod
    def time_to_seconds ( time_in ):
        '''convert the time component of a date string into seconds'''

        dateArr = str(time_in).split(" ")
        if len(dateArr) == 2:
            xtime = dateArr[1]
        else:
            xtime = dateArr[0]

        x = time.strptime(xtime.split('.')[0],'%H:%M:%S')
        return datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()

class Sun ( object ):

    @staticmethod
    def next_az( enoch ):
        enoch.loc.date = enoch.loc.next_rising( enoch.sun )
        enoch.sun.compute ( enoch.loc )

        #timedelta = mx.DateTime.TimeDelta(2,0,0)
        #dd = mx.DateTime.Date ( * golgotha.date.tuple() ) + timedelta

        deg = enoch.sun.az * 57.29746936176986
        return "%s,%d" % ( enoch.sun.alt, deg )






class Moon(object):

    def __str__(self):
        return "month:%d, monthday:%d,months:%d,monthlength:%d,yearlength:%d" % (self.month,self.monthday,self.months,self.monthlength,self.yearlength)

    def __init__( self, date ):
        self.date = date
        self.ephem = ephem.Moon( date.djd )
        self.ephem.compute( date.djd )

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


class Places(object):

    @staticmethod
    def atlanta():
        loc = ephem.Observer()
        loc.pressure = 0
        loc.horizon = '-0:34'

        loc.lat,loc.lon = '33.8','-84.4'
        return loc

    @staticmethod
    def sanfrancisco(date=None):
        loc = ephem.Observer()
        #loc.pressure = 0
        #loc.horizon = '-0:34'

        loc.lat, loc.lon = "37.773972","-122.431297"
        loc.elevation = 91
        if date is not None:
            loc.date = date

        return loc

    @staticmethod
    def golgotha(date=None):
        loc= ephem.Observer()
        loc.lat,loc.lon = "31.7811323","35.2296886"
        loc.elevation = 2484

        if date is not None:
            loc.date = date
        return loc

