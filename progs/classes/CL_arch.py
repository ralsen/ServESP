#!/usr/bin/env python

"""
------------------------------------------------------------------------------------------------------------
    class CL_arch.python
    
    does all archive actions
    -   collecting the files to be archived
    -   generates the archive files
    -   needs CL_ServESP
    -   all destination pathes and files are read from config*.xnl
    
    __init__:
    -   initialezd the variable "keep". DoArchive needs that to keep the original
        files or not
    
    CollectArchives:
    -   is called from __init__, its not necessary to call this function
    -   reads the <archive> tag from the config*.xml and generatrs a list
 
    DoArchive:
    -   goes through the list, generates the zip and delete older files
    
------------------------------------------------------------------------------------------------------------
"""

import logging
import sys
import datetime
import time
import glob
import os
import gzip

logger = logging.getLogger("logger")
jrnl = logging.getLogger("jrnl")

from datetime import datetime

import classes.CL_ServESP as CL_ServESP
global ServESP

CLASSNAME = "CL_arch"
VERNR = "1.0a"


class Archive:
    ArchiveCnt={}
    ArchiveFiles=[]
    ArchivePaths=[]
    keep=False
    
    def __init__(self):
        print("here we are in ")
        #print (ServESP)
        logger (CLASSNAME+" V"+VERNR+" initialized.")
        for eachArg in sys.argv:   
            #print ("Parameter:"+eachArg)
            if (eachArg == "keep"):
                self.keep = True
        self.CollectArchives()
        pass

    def CollectArchives(self):
        logger.info(self, "CollectArchives() start ")
        Archive.ArchiveFiles=[]
        
        for Config in CL_ServESP.ServESP.Config.findall(".//archive"):
            for archive in Config:
                Archive.ArchiveFiles += [archive.tag]
                Archive.ArchiveCnt[archive.tag] = int (archive.text)
        logger.info(self, "List of files to archive: ")
        logger.info(self, str(Archive.ArchiveCnt))
        logger.info(self, "CollectArchives() end ")

    def DoArchive(self):
        logger.info(self, "DoArchive() start ")
        for file in self.ArchiveCnt.keys():
            date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            ZipFile = CL_ServESP.ServESP.pathes["ArchPath"]+file+"_"+date_time+".gz"
            OrgFile = CL_ServESP.ServESP.pathes["LogPath"]+file
            logger.info(self, "---------------")
            try:
                f2z = open(OrgFile, "rb")
                f2zContent = f2z.read()
                f2z.close()
            except:
                logger.info(self, "NOT FOUND    : "+OrgFile)
                continue
            logger.info(self, "creating Zip : "+ZipFile)
            try:
                if (self.keep == False):
                    logger.info(self, "delete it    : ")
                    os.remove(OrgFile)
                zf = gzip.GzipFile(ZipFile, 'wb')
                zf.write(f2zContent)
                zf.close()
            except:
                logger.warning(self, "XXXXXNOT FOUND: "+OrgFile)

            FileList = (glob.glob(CL_ServESP.ServESP.pathes["ArchPath"]+file+"*.gz"))
            FileList = sorted(FileList)
            logger.info(self, "current files: " + str(len(FileList)))
            logger.info(self, "max files    : " + str(Archive.ArchiveCnt[file]    ))
            toDelete = len(FileList) - Archive.ArchiveCnt[file]
            if (toDelete>0):
                logger.info(self, "to delete    : " + str(toDelete))
                for currFile in FileList:
                    if(toDelete>0):
                        logger.info(self, "deleting     : "+currFile)
                        os.remove(currFile)
                        toDelete -= 1
        logger.info(self, "DoArchive() end")

"""
------------------------------------------------------------------------------------------------------------

    history:
    --------------------- V1.0a
    07.03.21    first version of the external class
"""
