import datetime
import ephem
import time

class Constants(object):

    precessionArcSecondsPerYear = 50.2

class FormData(object):
    '''manage form values and defaults'''

    def __init__(self):
        self.sel_gregorian = ""
        self.sel_phoenix = ""
        self.sel_julian = ""

        self.sel_moments = ""
        self.sel_days = ""
        self.sel_years = ""
        self.sel_solaryears = ""

        self.date = ""
        self.skipamount = ""

class Tools(object):

    @staticmethod
    def get_constellation ( enoch ):
        return enoch.cosmos.constellation ( enoch.sun )

    @staticmethod
    def ecliptic_angle ( body ):
        return float(ephem.Ecliptic ( body).lon * 57.295779513 )

    '''
    @staticmethod
    def ecliptic_constellation ( body ):
        constellations = {
                    29.05 : "Aries",
                    53.43 : "Taurus",

                }
        a = Tools.ecliptic_angle ( body )
    '''


    @staticmethod
    def localtime ( date_in ):
        '''A hack to support local time conversion prior to unixtime'''

        dateArr = str(date_in).split(" ")
        dateSplit = dateArr[0].split("/")
        newDate = "2000/%s/%s" % ( dateSplit[1], dateSplit[2] )

        tdate = ephem.Date ( newDate + " " + dateArr[1] )
        return dateArr[0] + " " + str(ephem.localtime ( tdate )).split(" ")[1].split(".")[0]

    @staticmethod
    def time_to_seconds ( time_in ):
        '''convert the time component of a date string into seconds'''

        dateArr = time_in.split(" ")
        if len(dateArr) == 2:
            xtime = dateArr[1]
        else:
            xtime = dateArr[0]

        x = time.strptime(xtime.split('.')[0],'%H:%M:%S')
        return datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()

    @staticmethod
    def convert_date(date_in ):

        dateInArr = date_in.split(" ")
        if len(dateInArr) == 2:
            timeStr = dateInArr[1]
        else:
            timeStr = str(Tools.localtime ( ephem.now() )).split(" ")[1]

        dateArr = dateInArr[0].split("/")
        date_out = "%s/%s/%s %s" % (dateArr[2],dateArr[0],dateArr[1],timeStr )

        return str(date_out)

    @staticmethod
    def convert_date_to_form ( date_in ):

        dateInArr = str(date_in).split(" ")
        if len(dateInArr) == 2:
            time = dateInArr[1]
        else:
            time = ""

        if len(dateInArr) == 2:
            timeStr = dateInArr[1]
        else:
            timeStr = str(datetime.datetime.now().time())

        dateArr = dateInArr[0].split("/")
        date_out = "%s/%s/%s %s" % (dateArr[1],dateArr[2],dateArr[0], time )

        return str(date_out).strip()

