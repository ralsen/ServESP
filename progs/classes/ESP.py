import logging
from inspect import getframeinfo, stack
import os, time
import json
from pathlib import Path

logger = logging.getLogger(__name__)

"""
  initialized Config-variables, logging and mail
"""  


class ESP:

    CONFPATH="/mnt/samba/Daten/Projekte/Raspberry/ServESP/XML/"
    CONFFILE=CONFPATH+"Config-ESP.xml"

    import xml.etree.ElementTree as ConfigXML
    import xml.etree.ElementTree as NodeConfig
    
    RootXML = ConfigXML.parse(CONFFILE)
    Config = RootXML.getroot() 

    pathes = {}
    files = {}
    
    ProgName = ""
    ProgVersion = ""
    def __init__(self, Name, Version):
        self.ProgName = Name
        self.ProgVersion = Version
        configOK = self.GetConfig()
        if(configOK==False):
            self.LogFile = self.CONFPATH+"/log/"+self.ProgName+".loy"
        else:
            self.LogFile = self.pathes["LogPath"]+"/"+self.ProgName+".log"
            
        f = Path(self.LogFile)
        LogExist = f.is_file()

        logging.basicConfig(filename = self.LogFile,
                            level = logging.DEBUG,
                            style = "{",
                            format="{asctime} [ {levelname:8} ] {message} [{name} : {lineno}]",
                            datefmt = "%d.%m.%Y %H:%M:%S")

        logging.info("\r\n---> "+self.ProgName+" V"+self.ProgVersion+" started")
        
        if not LogExist:
          logging.info("Pathes:")
          for p in self.pathes:
            logging.info(" - " + p)
          logging.info("Files:")
          for f in self.files:
            logging.info(" - " + f)
       
        if(configOK == False):
            logging.critical("configuration failed")
            print("Program is stopping now !!!")
            exit(False)
            return
        else:
            logging.debug("configuration file: "+ self.CONFFILE)
            logging.info("configuration file: OK")
# --------------------------------------------------------------------------------------------------

    def checkFile(self, filename, mode, terminate):
      f = Path(filename)
      print (f.is_file())
      
      if f.is_file():
        try:
          with open(filename, "r") as f:
            return open(filename, mode)
        except Exception as err:
          logging.error("could not open file: "+str(err)+ " with mode "+mode)
          if terminate:
            logger.critical("terminate program")
            exit(-1)
          else: return None
        
# --------------------------------------------------------------------------------------------------

    def GetConfig(self):
        # find Root-Path and store it in pf
        try:
            self.pathes["RootPath"] = self.Config.find(".//ServESP/Pathes/RootPath").text
        except AttributeError:
            return False
            
        # find all other Pathes and replace {Root} with real Root-Text
        for Path in self.Config.findall(".//ServESP/Pathes/"):
            self.pathes[Path.tag] = Path.text.replace("{Root}", self.pathes["RootPath"])

        for File in self.Config.findall(".//ServESP/Files/"):
            self.files[File.tag] = File.text
           
        return True            
# --------------------------------------------------------------------------------------------------

    def Close(self):
        logging.info("<--- " + self.ProgName+" V"+self.ProgVersion+" ended")
        logging.shutdown()

# --------------------------------------------------------------------------------------------------

    def Mailit(self, SubjectText, MailText):
        import smtplib

        to = 'follrichs@icloud.com'
        gmail__user = 'follrichs@gmx.de'
        gmail__pwd = 'Gmxkettko02!'
        smtpserver = smtplib.SMTP("mail.gmx.net",587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(gmail__user, gmail__pwd)
        header = 'To:' + to + '\n' + 'From: ' + gmail__user + '\n' + "Subject: "+SubjectText+"\n"
        msg = header + MailText
        smtpserver.sendmail(gmail__user, to, msg)
        smtpserver.close()
        ServESP.LogIt(self, "Email was send to: "+to+", Subject: "+SubjectText+", Text: "+MailText, logging.INFO)

