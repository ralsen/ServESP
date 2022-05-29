import logging
import time

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
            self.LogFile = self.CONFPATH+"/log/"+self.ProgName+".loy"
        else:
            self.LogFile = self.pathes["LogPath"]+"/"+self.ProgName+".log"
            
        logging.basicConfig(
        filename = self.LogFile,
        level = logging.DEBUG,
        style = "{",
        format = "{asctime} [{levelname:8}] {message}",
        datefmt = "%d.%m.%Y %H:%M:%S")

        self.LogIt("---> "+self.ProgName+" V"+self.ProgVersion+" started", logging.INFO)
        if(configOK == False):
            self.LogIt("configuration failed", logging.CRITICAL)
            return
        else:
            self.LogIt("configuration file: "+ self.CONFFILE+" OK", logging.INFO)
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
        self.LogIt("<--- " + self.ProgName+" V"+self.ProgVersion+" ended", logging.INFO)
        logging.shutdown()

# --------------------------------------------------------------------------------------------------

    def LogIt(self, outtext, err):
        if (err == logging.CRITICAL):
            print (time.ctime()+" "+"[CRITICAL] "+outtext)
            logging.error(outtext)
            logging.critical("Program is stopping now !!!")
            self .Close()
            print("Program is stopping now !!!")
            exit(False)
        if (err == logging.INFO):
            print (time.ctime()+" "+"[INFO    ] "+outtext)
            logging.info(outtext) 
        if (err == logging.WARNING):
            print (time.ctime()+" "+"[WARNING ] "+outtext)
            logging.warning(outtext) 
            
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

