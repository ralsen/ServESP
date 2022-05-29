#!/usr/bin/env python

import logging
import os
from collections import OrderedDict

CLASSNAME = "CL_MakeGraphic"
VERNR = "1.0a"

import classes.CL_ServESP as CL_ServESP
global ServESP

class MakeGraphic:
    HOURDIC  = OrderedDict([("{Time}", "hour"), ("{TimeCount}", "4"), ("{TimeText}", "Stunde")])
    DAYDIC   = OrderedDict([("{Time}", "day"), ("{TimeCount}", "1"), ("{TimeText}", "Tag")])
    WEEKDIC  = OrderedDict([("{Time}", "week"), ("{TimeCount}", "1"), ("{TimeText}", "Woche")])
    MONTHDIC = OrderedDict([("{Time}", "month"), ("{TimeCount}", "1"), ("{TimeText}", "Monat")])
    YEARDIC  =  OrderedDict([("{Time}", "year"), ("{TimeCount}", "1"), ("{TimeText}", "Jahr")])
    YEAR3DIC = OrderedDict([("{Time}", "year"), ("{TimeCount}", "3"), ("{TimeText}", "3 Jahre")])


# --------------------------------------------------------------------------------------------------

    def __init__(self):
        CL_ServESP.ServESP.LogIt (self, CLASSNAME+" V"+VERNR+" initialized.", logging.INFO)
        pass        
    
# --------------------------------------------------------------------------------------------------

    def MakeAllGraphs(self):
        for Name in CL_ServESP.ServESP.Config.findall('.//Nodes/Name'):
            self.MakeGraph(Name.text)
        os.system("cp -v "+CL_ServESP.ServESP.pathes["PicPath"]+"/*.png /var/www/html")
        CL_ServESP.ServESP.LogIt (self, "load all files up to dropbox", logging.INFO)            
        os.system(CL_ServESP.ServESP.pathes["ProgPath"]+"dbupload.sh")
        CL_ServESP.ServESP.LogIt (self, "upload done", logging.INFO)            
       
# --------------------------------------------------------------------------------------------------

    def MakeGraph (self, Node):
        RRD =       ( 
            "rrdtool graph \"{PIC_PATH}/{NodeName}_{TimeText}.png\" "
            "-t \"{NodeName} ({TimeText})\" --vertical-label \"Grad Celsius\" -s \"now - {TimeCount} \"{Time} -e \"now\"  -w 700 -h 200")

        RRD_DEF =   (
            " DEF:{Channel_No}={RRD_PATH}/{RRD_Name}.rrd:{Channel_No}:AVERAGE")
             
        RRD_VDEF =  (
            " VDEF:{Channel_No}_av={Channel_No},AVERAGE"
            " VDEF:{Channel_No}_ma={Channel_No},MAXIMUM"
            " VDEF:{Channel_No}_mi={Channel_No},MINIMUM"
            " VDEF:{Channel_No}_ak={Channel_No},LAST")
             
        RRD_COM =   (   
            " COMMENT:\"                         Durchschnitt   Maximum   Minimum    aktuell\\n\"")

        RRD_GPRINT =(   
            " LINE1:{Channel_No}{ChannelColor}:\"{ChannelName}{Spaces}\""
            " GPRINT:{Channel_No}_av:\" %8.2lf\""
            " GPRINT:{Channel_No}_ma:\" %8.2lf\""
            " GPRINT:{Channel_No}_mi:\" %8.2lf\""
            " GPRINT:{Channel_No}_ak:\" %8.2lf\""
            " COMMENT:\"                    ({Adr})\\n\"")
                

        try:
            CL_ServESP.ServESP.LogIt(self, CL_ServESP.ServESP.pathes["XMLPath"]+Node+".xml", logging.INFO)
            RootXML = CL_ServESP.ServESP.NodeConfig.parse(CL_ServESP.ServESP.pathes["XMLPath"]+Node+".xml")
        except FileNotFoundError:
            CL_ServESP.ServESP.LogIt("file: "+CL_ServESP.ServESP.pathes["XMLPath"]+Node+".xml"+" not found", logging.CRITICAL)
            print( "file: "+CL_ServESP.ServESP.pathes["XMLPath"]+Node+".xml"+" not found")
            
        NodeXML = RootXML.getroot()
        
        try:
            if (NodeXML.find(".//HardwareSec/Type").text != "DS1820"):
                #self.LogIt(0, "no temp.-sensor", logging.WARNING)
                return False
        except AttributeError:
            print ("\".//HardwareSec/Type\" not Found")
            CL_ServESP.ServESP.LogIt("\".//HardwareSec/Type\" not Found", logging.CRITICAL)

        Channels = 0
        try:
            NodeXML.find(".//ConfAppSec/Sensors").text
            for Name in NodeXML.findall('.//ConfAppSec/Sensors/'):
                Channels +=1
        except AttributeError:
            CL_ServESP.ServESP.LogIt(self, "\".//ConfAppSec/Sensors/\" not Found", logging.CRITICAL)
            print ("\".//ConfAppSec/Sensors/\" not Found")
            return False
        
            
        try:
            CL_ServESP.ServESP.LogIt (self, "Node: "+NodeXML.find(".//ConfComSec/Name").text, logging.INFO)            
            CL_ServESP.ServESP.LogIt (self, "Channel(s) found: "+(str)(Channels), logging.INFO)            
            try:
                RRDStr = RRD.replace("{PIC_PATH}", CL_ServESP.ServESP.pathes["PicPath"])
            except KeyError:
                CL_ServESP.ServESP.LogIt(self, "\"KeyError using pf-array\"", logging.CRITICAL)
            
            RRDStr = RRDStr.replace("{NodeName}", NodeXML.find(".//ConfComSec/Name").text)
        except AttributeError:
            CL_ServESP.ServESP.LogIt(self, "\".//ConfComSec/Name\" not Found", logging.CRITICAL)
            
        for sensors in NodeXML.findall('.//ConfAppSec/Sensors/*'):
            CL_ServESP.ServESP.LogIt (self, sensors.tag+" found", logging.INFO)
            RRDStr += RRD_DEF+RRD_VDEF+RRD_GPRINT
            for channel in sensors.findall(".//*"):
                CL_ServESP.ServESP.LogIt (self, channel.tag+" ---> "+channel.text, logging.INFO)
                if(channel.tag=="Database"):
                    RRDStr = RRDStr.replace("{Channel_No}", channel.text)
                    RRDStr = RRDStr.replace("{Channel_No}", channel.text)
                    RRDStr = RRDStr.replace("{Channel_No}", channel.text)
                if(channel.tag=="Name"):
                    spaces = " "*(20-len(channel.text))
                    RRDStr = RRDStr.replace("{ChannelName}", channel.text)
                    RRDStr = RRDStr.replace("{Spaces}", spaces)
                if(channel.tag=="Color"):
                    RRDStr = RRDStr.replace("{ChannelColor}", channel.text)
                if(channel.tag=="Adr"):
                    RRDStr = RRDStr.replace("{Adr}", channel.text)

        ## insert commemt line ahead of first "LINE1" line
        x = RRDStr.find("LINE1:")-1
        RRDStr = RRDStr[:x]+RRD_COM+RRDStr[x:]

        RRDStr = RRDStr.replace("{RRD_PATH}", CL_ServESP.ServESP.pathes["RRDPath"])
        RRDStr = RRDStr.replace("{RRD_Name}", Node)

        CL_ServESP.ServESP.LogIt (self, "generating diagrams ...\n", logging.INFO)
        self.ReplaceMulti(RRDStr, self.HOURDIC)
        self.ReplaceMulti(RRDStr, self.DAYDIC)
        self.ReplaceMulti(RRDStr, self.WEEKDIC)
        self.ReplaceMulti(RRDStr, self.MONTHDIC)
        self.ReplaceMulti(RRDStr, self.YEARDIC)
        self.ReplaceMulti(RRDStr, self.YEAR3DIC)
        return

# --------------------------------------------------------------------------------------------------
        
    def ReplaceMulti(self, text, dic):
        for i, j in dic.items():
            text = text.replace(i, j)
        os.system(text+" >/dev/null")
        return      

# --------------------------------------------------------------------------------------------------
