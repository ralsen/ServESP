#!/usr/bin/env python3
# https://docs.python.org/2/library/xml.etree.elementtree.html
# <!-- https://www.python-forum.de/viewtopic.php?t=33485c --> 
# <!-- http://www.willemer.de/informatik/python/xml.htm -->

"""
------------------------------------------------------------------------------------------------------------

    Monitor

------------------------------------------------------------------------------------------------------------
"""

import cfg
#from cfg import debuginfo as dbgi
import time
import logging

logger = logging.getLogger(__name__)

class Journal:
    JrnlBuf = ""
    
    def __init__(self, esp):
        logger.debug("INIT class Journal")
        self.JrnlFile = esp.checkFile(esp.pathes["LogPath"]+esp.files["JrnlFile"], "a", True)
        self.JrnlBuf = "[ date + time ]"
        
    def Close(self):
        logger.debug("--- START class Journal.close() ---")
        print(self.JrnlBuf)
        #self.JrnlFile.write(self.JrnlBuf)
        #self.JrnlFile.close()

    def Entry(self, text=""):
        logger.debug("--- START Entry() ---")
        self.JrnlBuf += "\n\r" + text 
        
        