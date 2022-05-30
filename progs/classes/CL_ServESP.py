import logging
import time

logger = logging.getLogger("logger")
jrnl = logging.getLogger("jrnl")

class ServESP:

#    CONFPATH="/mnt/samba/Daten/Projekte/Raspberry/ServESP/XML/"
    CONFPATH="./XML/"
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
            LogFile = self.CONFPATH+"/log/"+self.ProgName+".loy"
        else:
            LogFile = self.pathes["LogPath"]+"/"+self.ProgName+".log"
            JrnlFile = self.pathes["LogPath"]+"/"+self.ProgName+".jrnl"
        #formatter =  logging.Formatter('%(asctime)s :: %(levelname)-s :: %(message)s [%(module)s] [%(lineno)s]')
        formatter =  logging.Formatter('%(asctime)s - %(message)s [%(module)s] [%(lineno)s]')
        logger = logging.getLogger("logger")
        hdlrLogger = logging.FileHandler(LogFile)
        hdlrLogger.setFormatter(formatter)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(hdlrLogger)

        jrnl = logging.getLogger("jrnl")
        hdlrJrnl = logging.FileHandler(JrnlFile)
        hdlrJrnl.setFormatter(formatter)
        jrnl.setLevel(logging.DEBUG)
        jrnl.addHandler(hdlrJrnl)

        logger.info("---> "+self.ProgName+" V"+self.ProgVersion+" started")
        logger.info("here we are")
        jrnl.debug("in the journal")
        if(configOK == False):
            self.LogIt("configuration failed", logging.CRITICAL)
            return
        else:
            logger.info("configuration file: "+ self.CONFFILE+" OK")
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
        logger.info("<--- " + self.ProgName+" V"+self.ProgVersion+" ended.")
        #logger.shutdown()

# --------------------------------------------------------------------------------------------------

    def LogItx(self, outtext, err):
        if (err == logger.critical):
            print (time.ctime()+" "+"[CRITICAL] "+outtext)
            logger.error(outtext)
            logger.critical("Program is stopping now !!!")
            self .Close()
            print("Program is stopping now !!!")
            exit(False)
        if (err == logging.INFO):
            print (time.ctime()+" "+"[INFO    ] "+outtext)
            logger.info(outtext) 
        if (err == logging.WARNING):
            print (time.ctime()+" "+"[WARNING ] "+outtext)
            logger.warning(outtext) 
            
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
        ServESP.LogIt(self, "Email was send to: "+to+", Subject: "+SubjectText+", Text: "+MailText, logger.info)

