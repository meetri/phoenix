import sys
import socket
import datetime
import time
from urlparse import urlparse
from flask import Flask,render_template,request

sys.path.append("../phoenix" )
sys.path.append("./helpers" )

import enoch,enochephem,ephem,starcalc,helper

app = Flask (__name__)


@app.route("/clock", methods = ['GET','POST'])
def clock():

    formdata = helper.FormData()
    formdata.sel_gregorian = "selected "
    datetype = request.form.get("dateType","").strip()

    if request.method == "POST":
        dt = request.form.get("date","").strip()
    else:
        dt = request.args.get("date","").strip()

    tm = enochephem.TimeManager()

    if datetype == "Phoenix":
        e = enoch.Date()
        dtarr = dt.split("/")
        if len(dtarr) == 4:
            formdata.sel_phoenix = "selected"
            ep = ephem.now()
            ep2 = ephem.Date ( int( ep ) )
            t1 = str(ep)
            t2 = str(ep2)
            #print "t1 = %s, t2 = %s" % ( t1, t2 )

            time = ep - int(ep) + 1
            #print "time = %f, %s" % ( ep, str(ep) )
            #print dtarr
            e.set_etd(int(dtarr[3]),int(dtarr[2]),int(dtarr[0]),int(dtarr[1]),time)
            #print "conv date = %s" % str(e.djd)

        dt = e.djd
    elif dt.lower() == "epoch":
        dt = enoch.EpochDate
    elif dt.lower() == "now":
        dt = ephem.now()
    elif dt.lower() == "priest":
        dt  = ephem.Date("-8/6/23 12:00:00")
    elif dt.lower() == "conception":
        dt = ephem.Date("-8/12/19 12:00:00")
    elif dt.lower() == "birth":
        dt = ephem.Date("-7/9/23 12:00:00")
    elif len(dt) > 0:
        dt = helper.Tools.convert_date ( dt )
        dt = tm.utc ( dt )
    else:
        dt = ephem.now()

    enochtime = enoch.Date(dt)

    submit = request.form.get("submit",False)
    incval = request.form.get("incval",0)
    skiptype = request.form.get("skipType","")


    if incval:
        incval = int(incval)
        formdata.skipamount = incval

        nex = request.form.get("next",False)

        if skiptype == "Days":
            formdata.sel_days = "selected"
            if submit == "prev":
                enochtime.prev_day ( incval )
            elif submit == "next":
                enochtime.next_day( incval )
        elif skiptype == "Years":
            formdata.sel_years = "selected"
            if submit == "prev":
                enochtime.prev_year ( incval )
            elif submit == "next":
                enochtime.next_year( incval )



    #TODO: find a better equation for calculating precession
    yearcount = 2000 - int( str(enochtime.djd).split("/")[0])
    precession_shift = round(yearcount* helper.Constants.precessionArcSecondsPerYear / 3600)

    moment,thetime = enochtime.time.get_time()

    starDegree = 356 + precession_shift
    daysInMonth = enochtime.moon.monthlength
    moonDay = enochtime.moon.monthday
    enochday = enochtime.daycount
    flashparms = "?starDegree=%d&moment=%d&thetime=%d&daysInMonth=%d&moonDay=%d&eqDay=20&leap=1&enochday=%d&enochmode=1&weekshift=2" % (starDegree,moment,thetime,daysInMonth,moonDay,enochday)

# {{tools.convert_date_to_form( enochday.time.localtime(enochday.djd))}}
    if formdata.sel_phoenix:
        formdata.date = enochtime.etd_extended_date()
    elif formdata.sel_gregorian:
        formdata.date = helper.Tools.convert_date_to_form ( enochtime.time.tm.localtime(enochtime.djd ))

    return render_template("eclock.html",params=flashparms,clock_size=1000,enochday=enochtime,ephem=ephem,tools=helper.Tools,formdata=formdata)


@app.route("/test")
def test():
    return render_template("eclock.html")

