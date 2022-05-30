#!/usr/bin/env python
"""
    MakeAllGraphs (mg.py)

    this program generates all Graphics for the Temperature sensors

    !!! for history see end of file !!!
"""    

import logging
import os
import sys
import subprocess
import time

import classes.CL_ServESP as CL_ServESP
import classes.CL_MakeGraphic as CL_MakeGraphic

PROGNAME = "Makegraphics"
PROGVERS = "1.1b"
    
# --------------------------------------------------------------------------------------------------
   
se = CL_ServESP.ServESP(PROGNAME, PROGVERS)

ng = CL_MakeGraphic.MakeGraphic()  
ng.MakeAllGraphs()

se.Close()

exit()

"""
------------------------------------------------------------------------------------------------------------

    history:
    --------------------- V1.0a
    22.02.21    ServESP class is external

------------------------------------------------------------------------------------------------------------
"""
