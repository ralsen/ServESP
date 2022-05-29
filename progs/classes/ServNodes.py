import cfg
import classes.Journal as Journal
import classes.xml as xml
import logging
import time

"""
  analyzes the Node message and handle it
"""

logger = logging.getLogger(__name__)
  
class ServNodes:
  MessageParts = {}
  def __init__(self):
    logger.debug("INIT class ServNode")
    pass
    

  def Serv(self, esp, message):
    x = message.split("&")
    for entry in x:
        y = entry.split("=")
        self.MessageParts[y[0]] = y[1]  

    #if (esp.GetResponse() == "LONG"):
    #    for p in esp.pathes:
    #        print(p, "=", esp.pathes[p])

    t = self.MessageParts["Type"]
    print(t)
    print (message)
    #return
    if (t == "DS1820"):
        self.handle_DS1820(esp, self.MessageParts)
    elif (t == "Switch"):
        self.handle_Switch(self.MessageParts)
    elif (t == "ToF"):
        self.handle_ToF(self.MessageParts)
    else:
        print("!!! unknown Type !!!")
# ----------------------------------------------------------------------------------------
  def handle_DS1820(self, esp, field):
      
    logger.debug("Start handle_DS1820")
    logger.info("message from: " + field["?Host"])  
 
    xinfo=xml.XML(esp.pathes["XMLPath"]+field["?Host"]+".xml")
    if xinfo.Node == None:
      logger.critical("terminate program")
      exit(-1)

    outtempfile = esp.checkFile(esp.pathes["DataPath"]+esp.files["OutTempFile"], "r", True)
    outtemp = outtempfile.read()
    outtempfile.close()

    rrdfile = esp.checkFile(esp.pathes["RRDPath"]+field["?Host"]+".rrd", "a", True)
    
    Jrnl = Journal.Journal(esp)
    Jrnl.Entry("Systick=" + str(time.time()))
    Jrnl.Entry("Host=" + field['?Host'])
    Jrnl.Entry("Type=" + field['Type'])
    
    Jrnl.Entry("<----------------------------------->")  
    Jrnl.Close()
    logger.debug("End: DS1820")

# ----------------------------------------------------------------------------------------

  def handle_Switch(field):
    print (field["uptime"])
# ----------------------------------------------------------------------------------------

  def handle_ToF(field):
    print (field["uptime"])
# ----------------------------------------------------------------------------------------

  def schrott():
    print(field['Version'])
    print(xinfo.Get("Version"))
    for i in field:
      val = xinfo.Get(i)
      print(str(i)+" - " +str(val))
      if (val != None):
#        logger.info("field: "+str(i))
#        logger.info("  new value: "+str(field[i]))
        xmlval=xinfo.Get(i)
#        logger.info("  old value: "+str(xmlval))
        if(xmlval != field[i]):
          xinfo.Set("VarComSec", i, field[i])
#          logger.info("  -> changed ")
              
      #xinfo.Update()
      #xinfo.List(field)
      #Jrnl.Entry(cfg.JRNL_TEXT["NO_ERROR"])
      #Jrnl.Entry(cfg.JRNL_TEXT["N_XML"],"dummy.xml")
      #Jrnl.Entry(cfg.JRNL_TEXT["U_HARDWARE"], "RASPIX")
  