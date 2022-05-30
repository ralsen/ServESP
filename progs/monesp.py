#!/usr/bin/env python3
# https://docs.python.org/2/library/xml.etree.elementtree.html
# <!-- https://www.python-forum.de/viewtopic.php?t=33485c --> 
# <!-- http://www.willemer.de/informatik/python/xml.htm -->
"""
#******************************************************************************************************
#
#   Monitor
#    
#   this programm monitors all known nodes in he system. Therefore the programm scans at first
#   the config.xml-file and generates a timer-field for each node. NodeTimer holds the timer-field
#   and NodeDefault holds the default for NodeTimer. The program install  a pyinotify and the timer
#   callback NodeTicker.
#   In NodeTicker all NodeTimers are decremented by 1 if the Nodetimer isnt 0. If NodeTimer count to 0
#   a Alert is generated and the decrementation stopps.
#
#   the pyinotify handler EventHandler checks whether the event has to be monitored. if so and the 
#   NodeTicker is 0 the Node is back again. This event is logged. at the end the handler sets the 
#   NodeTicker to the NodeDefault-Value.
#
#   todos:
#   error handling -> check the presenta of XML-files and the Tags 
#   whats todo when events occured (the alert-text isnt enough)
#   log-file should have the same look as the other ones
#
#******************************************************************************************************
"""
import xml.etree.ElementTree as Config
import xml.etree.ElementTree as NodeConfig
import logging
import os
import re
import string
import pyinotify
import time
import datetime
import threading
import sys
import smtplib
from multiprocessing.connection import Listener
from concurrent import futures
from multiprocessing.connection import Client
from xml.etree import ElementTree

import classes.CL_ServESP as CL_ServESP

PROGNAME = "monesp"
VERNR = "1.3c"
CONFPATH="/media/samba/Daten/Projekte/Raspberry/ServESP/XML/"
CONFFILE=CONFPATH+"Config-neu.xml"


class NodeMonitor:
    LastEvent=""
    Nodes = []
    
    class Node():
        "Stores name and related data"
        def __init__(self, **args):
            self.Name=args["Name"]
            self.Ticker = args["Ticker"]
            self.Default = args["Default"]

    def __init__(self):
        print("\033[2J")
        
        self.wm = pyinotify.WatchManager()  # Watch Manager
        self.mask = pyinotify.IN_CLOSE_WRITE   # watched events

        self.CollectNodes()
    
        Handler= self.EventHandler()
        notifier = pyinotify.Notifier(self.wm, Handler)
        wdd = self.wm.add_watch(CL_ServESP.ServESP.pathes["XMLPath"], self.mask, rec=False)

        CL_ServESP.ServESP.LogIt(self, "Init ComControl()", logging.INFO)
        self.address = ('localhost', 6001)     # family is deduced to be 'AF_INET'
        self.listener = Listener(self.address, authkey=b'secret password')
        self.cc=futures.ThreadPoolExecutor(max_workers=3)
        self.cc.submit(self.ComRec)
 
        self.NodeTicker()
 
        notifier.loop()
        pass
                
    def ComRec(self):
        ComSwitch = {"Default"  : NodeMonitor.ListDefTimers,
                     "Current"  : NodeMonitor.ListCurTimers,
                     "Collect"  : NodeMonitor.CollectNodes,
                    }
            
        CL_ServESP.ServESP.LogIt(self, "ComRec()", logging.INFO)
        CL_ServESP.ServESP.LogIt(self, "waiting for command", logging.INFO)
        self.conn = self.listener.accept()
        CL_ServESP.ServESP.LogIt(self, "command received", logging.INFO)
        msg = self.conn.recv()
        # do something with msg 
        CL_ServESP.ServESP.LogIt(self, "mit Parameter: "+ msg, logging.INFO)
        if (msg=="Listx"):
            NodeMonitor.ListDefTimers(self)
        ComSwitch.get(msg, action_un)(self)
        self.cc=futures.ThreadPoolExecutor(max_workers=3)
        self.cc.submit(self.ComRec)
        CL_ServESP.ServESP.LogIt(self, "ComRec() end", logging.INFO)
                            
    class EventHandler(pyinotify.ProcessEvent):
        def process_IN_CLOSE_WRITE(self, event):
            EventName = event.name[:-4]
            for i in NodeMonitor.Nodes:
                if(EventName == i.Name):
                    if(i.Ticker == 0):
                        t = threading.Thread(target=CL_ServESP.ServESP.Mailit, args=(self, "J U B E L", EventName))
                        t.daemon = True
                        t.start()
#                        CL_ServESP.LogIt (self, " ! ! ! J U B E L ! ! ! ---> "+event.name, logging.INFO)
                    i.Ticker = NodeMonitor.Tolerance(self, i.Default)
                NodeMonitor.LastEvent  = EventName
    
    def Tolerance(self, val):
        return((val+1)*3)
        
    def CollectNodes(self):
        for Name in CL_ServESP.ServESP.Config.findall('.//Nodes/Name'):
            RootXML = NodeConfig.parse(CL_ServESP.ServESP.pathes["XMLPath"]+Name.text+".xml")
            NodeXML = RootXML.getroot()
            if NodeXML.findall(".//ConfComSec"):
                for XMLClass in NodeXML.findall(".//TransCycle"):
                    if (len(self.Nodes)==0):
                        self.Nodes.append(self.Node(Name=Name.text, Ticker=self.Tolerance(int(XMLClass.text)), Default=int(XMLClass.text)))
                    else:    
                        NodeExists = False
                        for i in self.Nodes:
                            if(i.Name == Name.text):
                                NodeExists = True
                                break

                        if(NodeExists == True):
                            CL_ServESP.ServESP.LogIt (self, "already known:  "+Name.text, logging.INFO)
                        else:
                            CL_ServESP.ServESP.LogIt (self, "new Node found: "+Name.text, logging.INFO)
                            self.Nodes.append(self.Node(Name=Name.text, Ticker=self.Tolerance(int(XMLClass.text)), Default=int(XMLClass.text)))
            else:
                outtext = " ! ! ! No ConfComSec tag ---> in "+Name.text
                CL_ServESP.ServESP.LogIt(self, outtext, logging.CRITICAL)
            

    def NodeTicker(self):
        threading.Timer(1, self.NodeTicker).start()
        start=(float)(time.time()) * 1000
        print("\033[2J")
        print("\033[0;0H")
        print(datetime.datetime.now())
        for i in self.Nodes:
            #self.ListCurTimers()
            print ("Ticker: %5d for "% (i.Ticker) + (str)(i.Name))
            if (i.Ticker):
                i.Ticker -= 1
                if(i.Ticker == 0):
                    t = threading.Thread(target=CL_ServESP.ServESP.Mailit, args=(self, "A L A R M", i.Name))
                    t.daemon = True
                    t.start()
#                    CL_ServESP.ServESP.LogIt(self, " ! ! ! A L A R M ! ! ! ---> "+i.Name, logging.INFO)
        print("last Event: "+NodeMonitor.LastEvent)
        print("duration: %3.2f ms" %((time.time()*1000) - start))
        print ("<----------------->")

    def ListDefTimers(self):
        CL_ServESP.ServESP.LogIt(self, "List of Node default timers:", logging.INFO)
        for i in self.Nodes:
            CL_ServESP.ServESP.LogIt(self, "  "+i.Name+" = "+(str)(i.Default), logging.INFO)
        
    def ListCurTimers(self):
        CL_ServESP.ServESP.LogIt(self, "List of currently Node timers:", logging.INFO)
        for j in self.Nodes:
            CL_ServESP.ServESP.LogIt(self, "  "+j.Name+" = "+(str)(j.Ticker), logging.INFO)

    
#******************************************************************************************************

se = CL_ServESP.ServESP(PROGNAME,VERNR)

def help():
        print("na du brauchst wohl Hilfe wie das hier funktioniert")
        print(switch.keys())
        #exit()
    
def action2():
    {
        print("Action2")
    }
def action3():
    {
        print("Action3")
    }
def action_un():
    {
        print("Action unknown")
    }

def sendCommand():
    address = ('localhost', 6001)
    conn = Client(address, authkey=b'secret password')
    conn.send(eachArg)
    conn.close()

def Hello():
    {
        print ("Hello from M.py")
    }
    
switch ={
         "M.py"     : Hello,
         "Monitor"  : NodeMonitor,
         "Default"  : sendCommand,
         "Current"  : sendCommand,
         "Collect"  : sendCommand,
         "two"      : action2, 
         "three"    : action3}



print (len(sys.argv))
if (len(sys.argv)<2):
    help()
    exit()


for eachArg in sys.argv:   
    print ("Parameter: "+eachArg)
    print(switch.get(eachArg, help)())



logging.info(PROGNAME+VERNR+" ended")

exit()

"""
------------------------------------------------------------------------------------------------------------

    history:
    --------------------- V1.2b
    22.02.21    ServESP class is external

    16.09.29    V1.2a   working with one Node-List instead of NodeTimer, NodeDefunlt and NodeName-lists
                        sending emails
                        with process communication
    
    18.05.20    V1.0b   first version with minimal functionality
    19.95.20    V1.0c   function Protokollis new
                        some error handlings done
------------------------------------------------------------------------------------------------------------
"""
