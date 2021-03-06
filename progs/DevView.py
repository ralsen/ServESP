#!/usr/bin/env python3
# https://docs.python.org/2/library/xml.etree.elementtree.html
# <!-- https://www.python-forum.de/viewtopic.php?t=33485c --> 
# <!-- http://www.willemer.de/informatik/python/xml.htm -->

"""
------------------------------------------------------------------------------------------------------------

    Monitor

------------------------------------------------------------------------------------------------------------
"""

import classes.CL_ServESP as CL_ServESP
import logging
import sys
import os
import xml.etree.ElementTree as TableXML

logger = logging.getLogger("logger")
jrnl = logging.getLogger("jrnl")

PROGNAME = "DevView"
PROGVERS = "2.2"

#******************************************************************************************************

se = CL_ServESP.ServESP(PROGNAME, PROGVERS)

phpout = '<table border="1" cellpadding="5" align="left">'

def GetXMLValue(key):
    print("GetXMLValue(key):", key)
    try:
        if (NodeXML.find(key)):
            print(key+" found")
            logger.info(key+" found")
            
    except AttributeError:
        print (key+" not Found")
        logger.critical(key+" not Found")
    print(NodeXML.find(key).text)
    return(NodeXML.find(key).text)
    
# looking for all nodes in config
for Name in se.Config.findall('.//Nodes/Name'):
    logger.info (Name.text)            

    # try to open the nodes XML
    try:
        logger.info(se.pathes["XMLPath"]+Name.text+".xml")
        RootXML = se.NodeConfig.parse(se.pathes["XMLPath"]+Name.text+".xml")
    except FileNotFoundError:
        logger.info("file: "+se.pathes["XMLPath"]+Name.text+".xml"+" not found")
        print( "file: "+se.pathes["XMLPath"]+Name.tex+".xml"+" not found")
    NodeXML = RootXML.getroot()

    # try to open the table XML for the type of the node
    try:
        logger.info(se.pathes["XMLPath"]+"Table"+GetXMLValue(".//Type")+".xml")
        RootTable = TableXML.parse(se.pathes["XMLPath"]+"Table"+GetXMLValue(".//Type")+".xml")
    except FileNotFoundError:
        logger.critical("file: "+se.pathes["XMLPath"]++"Table"+GetXMLValue(".//Type")+".xml"+" not found")
        print( "file: "+se.pathes["XMLPath"]++"Table"+GetXMLValue(".//Type")+".xml"+" not found")

    Table = RootTable.getroot()

    # put all listed tags from Table XML and the assigned values from node XML in
    # the table to be displayed
    phpout += ("<tr>")    
    for entry in Table.findall('.//*'):
        value = GetXMLValue(".//"+entry.tag)
        phpout += "<td>"+entry.tag+"="
        if(entry.tag=="IP"):
            phpout += "<a target = \"_blank\" HREF=\"http://"+value+"/status\">"+value+"</a>"
        else:
            phpout += value
        phpout += "</td>"   
    phpout += ("</tr>")
phpout += ("</table>")


se.Close()
print (phpout)
sys.exit()

"""
------------------------------------------------------------------------------------------------------------

    history:
    --------------------- V1.0a
    22.02.21    ServESP class is external

------------------------------------------------------------------------------------------------------------
"""
