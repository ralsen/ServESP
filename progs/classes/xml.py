#!/usr/bin/env python3
# https://docs.python.org/2/library/xml.etree.elementtree.html
# <!-- https://www.python-forum.de/viewtopic.php?t=33485c --> 
# <!-- http://www.willemer.de/informatik/python/xml.htm -->

"""
------------------------------------------------------------------------------------------------------------

    Monitor

------------------------------------------------------------------------------------------------------------
"""

#import cfg
import logging
import sys
import datetime
import time
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class XML:
    import xml.etree.ElementTree as NodeXML
    
    Node = None
    
    def __init__(self, file):
        logger.debug("INIT class XML")
        logger.info("XML file: "+file)
        try:
          RootXML = self.NodeXML.parse(file)
        except:
          logger.error("could not access XML-file: "+file)
          return None
        self.Node = RootXML.getroot() 
        
    def List(self, field):
        logger.debug("--- START List ---")
        logger.debug(self.Node.tag)
        logger.debug ("list sections")
#        for child in self.Node:
#            logger.debug("Field: "+child.tag)
            
#        for entry in self.Node.iter('Color'):
#            logger.debug("--->"+ entry.text)
            
        logger.debug("list fields in message")
        for i in self.Node.findall(".//*"):
            try:
                logger.info (i.tag+" = "+field[i.tag])
            except KeyError:
                logger.info("tag -"+i.tag+"- unknown")
        logger.debug("--- END ---")
        
    def Get(self, value):
        for entry in self.Node.findall(".//*"):
#            print("###"+str(entry.tag))
            if(entry.tag == value):
                return entry.text
                
    def Set(self, section, var, val):
        for entry in self.Node.findall(".//"+section+"/"):
            if(entry.tag == var):
                entry.text = val
    
    def Update(self):
        logger.debug(self.Node.get("*"))
        #self.NodeXML.write("xml.xml")
                