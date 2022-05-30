#!/usr/bin/env python3
# https://docs.python.org/2/library/xml.etree.elementtree.html
# <!-- https://www.python-forum.de/viewtopic.php?t=33485c --> 
# <!-- http://www.willemer.de/informatik/python/xml.htm -->

"""
------------------------------------------------------------------------------------------------------------

    Monitor
    
    this programm monitors all known nodes in he system. Therefore the programm scans at first
    the config.xml-file and generates a timer-field for each node. NodeTimer holds the timer-field
    and NodeDefault holds the default for NodeTimer. The program install  a pyinotify and the timer
    callback NodeTicker.
    In NodeTicker all NodeTimers are decremented by 1 if the Nodetimer isnt 0. If NodeTimer count to 0
    a Alert is generated and the decrementation stopps.

    the pyinotify handler EventHandler checks whether the event has to be monitored. if so and the 
    NodeTicker is 0 the Node is back again. This event is logged. at the end the handler sets the 
    NodeTicker to the NodeDefault-Value.

    !!! for history see end of file !!!

    todos:
    error handling -> check the presenta of XML-files and the Tags 
    whats todo when events occured (the alert-text isnt enough)
    log-file should have the same look as the other ones

------------------------------------------------------------------------------------------------------------
"""

import classes.CL_ServESP as CL_ServESP
import classes.CL_arch as CL_arch

PROGNAME = "arch"
PROGVERS = "1.3a"

#******************************************************************************************************


se = CL_ServESP.ServESP(PROGNAME, PROGVERS)

nm=CL_arch.Archive()
nm.DoArchive()

se.Close()

exit()

"""
------------------------------------------------------------------------------------------------------------
    History:
    --------------------- V1.1a
    05.03.21    Archive class is external
                log-readability is improved
    --------------------- V1.1a
    22.02.21    ServESP class is external
    ---------------------
    18.05.20    V1.0b   first version with minimal functionality
    19.95.20    V1.0c   function Protokollis new
                        some error handlings done
------------------------------------------------------------------------------------------------------------
"""
