#!/usr/bin/env python
"""
    weather.py

    this program gets the weather data from openweathermap.org and stores the data.
    datas are stored in:
    - Logfile
    - the act. temperature value in Getouttemp.txt
    - the sun set/rise time ist stored in "SunCntrlFile" if the file doesnt exists

    !!! for history see end of file !!!

    this is important for request.get https://requests.readthedocs.io/en/master/user/quickstart/
    aware of failed call and the timeout parameter, this should be given
"""

import xml.etree.ElementTree as Weather
import time
import urllib
import string
import re
import os
import logging
#import rrdtool
import subprocess
from sys import exit

import classes.CL_ServESP as CL_ServESP

logger = logging.getLogger("logger")
jrnl = logging.getLogger("jrnl")

PROGNAME = "weather"
PROGVERS = "1.3c"

se = CL_ServESP.ServESP(PROGNAME, PROGVERS)

try:

    import requests
except ImportError:
    exit("This script requires the requests module\nInstall with: sudo pip install requests")

res = requests.get ('http://api.openweathermap.org/data/2.5/weather?q=Langenhagen,DE&appid=292f322d8c2231804fa357041a30a73e&units=metric&mode=xml')

# so jetzt schreiben wir das ganze in eine Datei, falls andere das auch gebrauchen koennen
# //FOL Statusabfrage noch einbauen
f=open(se.pathes["DataPath"]+se.files["WeatherFile"], "w")
f.write(res.text)
f.close()

WeatherXML = Weather.parse(se.pathes["DataPath"]+se.files["WeatherFile"])

def GetValue(key, value):
    for Name in WeatherXML.findall('.//'+key):
        return(Name.attrib[value])

data = 'N:'

logger.info ("Temperature akt: "+GetValue ("temperature", "value"))
data += GetValue ("temperature", "value") +":"

# write this in a file for other programs 
tempfile = open(se.pathes["DataPath"]+"OutTemp.txt", "w")
tempfile.write (GetValue("temperature", "value"))
tempfile.close()
# this is for compatibility
#tempfile = open("/home/pi/getouttemp.txt", "w")
tempfile = open("./data/OutTemp.txt", "w")
tempfile.write (GetValue("temperature", "value"))
tempfile.close()

logger.info ("Temperature min: "+GetValue ("temperature", "min"))
data += GetValue ("temperature", "min") +":"
logger.info ("Temperature max: "+GetValue ("temperature", "max"))
data += GetValue ("temperature", "max") +":"
logger.info ("Feels like     : "+GetValue ("feels_like", "value"))
data += GetValue ("feels_like", "value") +":"
logger.info ("Humidity       : "+GetValue ("humidity", "value"))
data += GetValue ("humidity", "value") +":"
logger.info ("Pressure       : "+GetValue ("pressure", "value"))
data += GetValue ("pressure", "value") +":"
logger.info ("Wind Speed     : "+GetValue ("speed", "value"))
data += GetValue ("speed", "value") +":"
logger.info ("Wind direction : "+GetValue ("direction", "value"))
data += GetValue ("direction", "value") #+":"
logger.info ("Sunset         : "+GetValue ("sun", "set")[11:19])
logger.info ("Sunrise        : "+GetValue ("sun", "rise")[11:19])
logger.info ("update         : "+GetValue ("lastupdate", "value")[11:19])

try:
    f=open(se.pathes["DataPath"]+"/"+se.files["SunCntrlFile"], "r")
    f.close()
except FileNotFoundError:
    f=open(se.pathes["DataPath"]+"/"+se.files["SunCntrlFile"], "w")
    f.write(GetValue ("sun", "rise")[11:19]+"\n")
    f.write(GetValue ("sun", "set")[11:19])
    f.close()
    logger.info ("calling        : "+se.pathes["ProgPath"]+"/" + se.files["SunExe"])
    print (os.system("python3 "+se.pathes["ProgPath"]+"/" + se.files["SunExe"]))

logger.info ("RRD-String     : "+data)
tempfile = open(se.pathes["DataPath"]+se.files["WeatherData"], "a")
tempfile.write (time.ctime()+" : "+data+"\r\n")
tempfile.close()
print("this has to be written in RRDTOOL: ", se.pathes["RRDPath"]+PROGNAME+".rrd", data)
#rrdtool.update(se.pathes["RRDPath"]+PROGNAME+".rrd", data)

se.Close()

quit()

"""
------------------------------------------------------------------------------------------------------------

    history:
    --------------------- V1.2b
    27.03.21    writes rrd-string into "DataPath/Weatherdata" additionaly
    --------------------- V1.2a
    22.02.21    ServESP class is external
    --------------------- V1.1a
    20.02.12    write the outside temperature in "OutTemp.txt" in DataPath
                this is just for other prgrams or computers who needs this information
                and dont have internet access or to reduce the requests to openweathermap
    --------------------- V1.0a
    16.02.21 - works with the new py-class ServESP
             - puts most weather data into a rrd
             - writes sunset and sunrise into a file if the file doesnt exist
               in the nicht crontab could delete the sunrise/sunset-file and
               this program writes a new one for the new day.
             - this programm needs some entrys in config.xml. For itself, log, archive etc.
    18.02.18    Umstellung auf python3

------------------------------------------------------------------------------------------------------------
"""
