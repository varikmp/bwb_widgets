import os
import glob
import sys
import functools
import jsonpickle
from collections import OrderedDict
from Orange.widgets import widget, gui, settings
import Orange.data
from Orange.data.io import FileFormat
from DockerClient import DockerClient
from BwBase import OWBwBWidget, ConnectionDict, BwbGuiElements, getIconName, getJsonName
from PyQt5 import QtWidgets, QtGui

class OWslim_web_gcp(OWBwBWidget):
    name = "slim_web_gcp"
    description = "nci idc slim viewer dicom arc gcp"
    priority = 1
    icon = getIconName(__file__,"120px-NIH_Master_Logo_Vertical_2Color.png")
    want_main_area = False
    docker_image_name = "varikmp/slim_web"
    docker_image_tag = "local"
    inputs = [("inputFile",str,"handleInputsinputFile"),("Trigger",str,"handleInputsTrigger")]
    outputs = [("OutputDir",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    PROJECT_ID=pset(None)
    LOCATION=pset(None)
    DATASET=pset(None)
    DICOM_STORE=pset(None)
    HEALTHCARE_API_URL=pset(None)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"slim_web_gcp")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsinputFile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("inputFile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsTrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("Trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"OutputDir"):
            outputValue=getattr(self,"OutputDir")
        self.send("OutputDir", outputValue)
