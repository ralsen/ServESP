#!/usr/bin/env python3
# https://docs.python.org/2/library/xml.etree.elementtree.html
# <!-- https://www.python-forum.de/viewtopic.php?t=33485c --> 
# <!-- http://www.willemer.de/informatik/python/xml.htm -->

"""
------------------------------------------------------------------------------------------------------------

    Monitor

------------------------------------------------------------------------------------------------------------
"""


verbose = False
lang = "english"
field = {}


JRNL_TEXT = {}
JRNL_TEXT ["NO_ERROR"] = \
                    ("INFO", "NO_ERROR<br>",
                        {
                        "deutsch":"kein Fehler",
                        "english":"No Error"
                        }
                    )
                    
JRNL_TEXT ["W_RRD"] = \
                    ("ERROR", "RRD_FAILED<br>",
                        {
                        "deutsch":"RRD Fehler",
                        "english":"RRD Error"
                        }
                    )

JRNL_TEXT ["W_PARA"] = \
                    ("ERROR", "PARA_FAILED<br>",
                        {
                        "deutsch":"Parameter Fehler",
                        "english":"Parameter error"
                        }
                    )

JRNL_TEXT ["U_DEVICE"] = \
                    ("ERROR", "U_DEVICE<br>",
                        {
                        "deutsch":"unbekanntes Gerät",
                        "english":"unknown device"
                        }
                    )

JRNL_TEXT ["C_IP"] = \
                    ("INFO", "CHANGED_IP<br>",
                        {
                        "deutsch":"IP hat sich geändert",
                        "english":"changed IP"
                        }
                    )

JRNL_TEXT ["C_VERS"] = \
                    ("INFO", "CHANGED_VERSION<br>",
                        {
                        "deutsch":"Softwareversion hat sich geändert",
                        "english":"changed Software Version"
                        }
                    )

JRNL_TEXT ["U_TYPE"] = \
                    ("WARNING", "UNKNOWN_TYPE<br>",
                        {
                        "deutsch":"unbekannter Gerätetyp",
                        "english":"unknown device type"
                        }
                    )

JRNL_TEXT ["W_TYPE"] = \
                    ("WARNING", "WRONG_TYPE<br>",
                        {
                        "deutsch":"falscher Gerätetyp",
                        "english":"wrong device type"
                        }
                    )

JRNL_TEXT ["N_XML"] = \
                    ("CRITICAL", "NO_XML<br>",
                        {
                        "deutsch":"XML-Datei {TEXT} nicht gefunden",
                        "english":"XML-file {TEXT} not found"
                        }
                    )

JRNL_TEXT ["N_FILE"] = \
                    ("CRITICAL", "NO_FILE<br>",
                        {
                        "deutsch":"Datei {TEXT} nicht gefunden",
                        "english":"file {TEXT} not found"
                        }
                    )
                    
JRNL_TEXT ["U_HARDWARE"] = \
                    ("ERROR", "UNKNOWN_HARDWARE<br>",
                        {
                        "deutsch":"unbekannte Hardware {TEXT}",
                        "english":"unknown hardware {TEXT}"
                        }
                    )

JRNL_TEXT ["W_HARDWARE"] = \
                    ("ERROR", "WRONG_HARDWARE<br>",
                        {
                        "deutsch":"falsche Hardware {TEXT}",
                        "english":"wrong hardware {TEXT}"
                        }
                    )

