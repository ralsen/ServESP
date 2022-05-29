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
        CL_ServESP.ServESP.LogIt (self, CLASSNAME+" V"+VERNR+" initialized.", logging.INFO)
        for eachArg in sys.argv:   
            #print ("Parameter:"+eachArg)
            if (eachArg == "keep"):
                self.keep = True
        self.CollectArchives()
        pass

    def CollectArchives(self):
        CL_ServESP.ServESP.LogIt (self, "CollectArchives() start ", logging.INFO)
        Archive.ArchiveFiles=[]
        
        for Config in CL_ServESP.ServESP.Config.findall(".//archive"):
            for archive in Config:
                Archive.ArchiveFiles += [archive.tag]
                Archive.ArchiveCnt[archive.tag] = int (archive.text)
        CL_ServESP.ServESP.LogIt(self, "List of files to archive: ", logging.INFO)
        CL_ServESP.ServESP.LogIt(self, str(Archive.ArchiveCnt), logging.INFO)
        CL_ServESP.ServESP.LogIt(self, "CollectArchives() end ", logging.INFO)

    def DoArchive(self):
        CL_ServESP.ServESP.LogIt (self, "DoArchive() start ", logging.INFO)
        for file in self.ArchiveCnt.keys():
            date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            ZipFile = CL_ServESP.ServESP.pathes["ArchPath"]+file+"_"+date_time+".gz"
            OrgFile = CL_ServESP.ServESP.pathes["LogPath"]+file
            CL_ServESP.ServESP.LogIt (self, "---------------", logging.INFO)
            try:
                f2z = open(OrgFile, "rb")
                f2zContent = f2z.read()
                f2z.close()
            except:
                CL_ServESP.ServESP.LogIt(self, "NOT FOUND    : "+OrgFile, logging.WARNING)
                continue
            CL_ServESP.ServESP.LogIt (self, "creating Zip : "+ZipFile, logging.INFO)
            try:
                if (self.keep == False):
                    CL_ServESP.ServESP.LogIt (self, "delete it    : ", logging.INFO)
                    os.remove(OrgFile)
                zf = gzip.GzipFile(ZipFile, 'wb')
                zf.write(f2zContent)
                zf.close()
            except:
                CL_ServESP.ServESP.LogIt(self, "XXXXXNOT FOUND: "+OrgFile, logging.WARNING)

            FileList = (glob.glob(CL_ServESP.ServESP.pathes["ArchPath"]+file+"*.gz"))
            FileList = sorted(FileList)
            CL_ServESP.ServESP.LogIt (self, "current files: " + str(len(FileList)), logging.INFO)
            CL_ServESP.ServESP.LogIt (self, "max files    : " + str(Archive.ArchiveCnt[file]    ), logging.INFO)
            toDelete = len(FileList) - Archive.ArchiveCnt[file]
            if (toDelete>0):
                CL_ServESP.ServESP.LogIt (self, "to delete    : " + str(toDelete), logging.INFO)
                for currFile in FileList:
                    if(toDelete>0):
                        CL_ServESP.ServESP.LogIt (self, "deleting     : "+currFile, logging.INFO)
                        os.remove(currFile)
                        toDelete -= 1
        CL_ServESP.ServESP.LogIt(self, "DoArchive() end", logging.INFO)

"""
------------------------------------------------------------------------------------------------------------

    history:
    --------------------- V1.0a
    07.03.21    first version of the external class
"""
