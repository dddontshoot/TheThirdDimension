import sys
import pathlib
sys.path.append(str(pathlib.Path().absolute()))

import json

#local modules
import lib.settings
from lib.args import getArgs
from lib.fileParser import parseBaseFile
from lib.fileParser import parseCSVFile
from lib.fileParser import writeFragmentList
from lib.utils import ticker
from lib.utils import initReporting
from lib.utils import sorter

# Load standard settings
settings=lib.settings.getSettings()

# Check for "--base" in the arguments. Value of coreID and entityType is redundant, but is required for compatability.
arguments=getArgs()

# Choose values from settings file or command line.
if arguments["baseFile"] != "":
    settings["baseFile"]=arguments["baseFile"]

# Check that baseFile has ".base" extension
if settings["baseFile"][len(settings["baseFile"])-5 : len(settings["baseFile"])] == ".base":
    # Filename looks ok, let us divine the working folder and the final filename
    settings["workingPath"] = settings["baseFile"][0:len(settings["baseFile"])-5]+settings["pathCharacter"]
    settings["finalFileName"]=settings["baseFile"][0:len(settings["baseFile"])-5]+".blend"
    #print("==baseFile=",settings["baseFile"])
    #print("==workingPath=",settings["outputPath"])
else:
    print("== Base file must have '.base' extension!")
    print("== ",settings["baseFile"])
    exit(1)

# load the importDetails database
entityDatabase = parseCSVFile(settings["csvFile"], settings["meshPath"])

# Initialise reporting variables
progress,reportList,reportNot=initReporting()

print("Opening",settings["basePath"]+settings["baseFile"])
# load the base data
surfaces = parseBaseFile(settings["basePath"]+settings["baseFile"])

entitiesInUse=list()
unknownEntities=list()

buildingReport=dict()
invisibleReport=dict()

print("Collecting data...")
for surfaceName in surfaces.keys():
    surface=json.loads(surfaces[surfaceName])
    #print (entities)
    for item in surface:
        entityProperties=json.loads(item)
        name=entityProperties["name"]
        if name not in entityDatabase:
            if name not in unknownEntities:
                unknownEntities.append(name)
        else:
            entityImportDetails=json.loads(entityDatabase[name])
            if entityImportDetails["3D"] == 1 and entityImportDetails["visible"] == 1:
                    progress["totalNumberOfEntitiesCompleted"]=progress["totalNumberOfEntitiesCompleted"]+1
                    buildingReport=ticker(buildingReport,name)
            else:
                    progress["numberOfIgnoredEntities"]=progress["numberOfIgnoredEntities"]+1
                    #totalinvisible=totalinvisible+1
                    invisibleReport=ticker(invisibleReport,name)

if False:
    file=open("report.csv","w")
    for key in report:
        output=key + "," + str(report[key]) + "\n"
        file.write(output)

print("Building report...")

invisibleReport=sorter(invisibleReport)
for key in invisibleReport:
    print(invisibleReport[key])
print("")
print("Total invisible:",progress["numberOfIgnoredEntities"])
print("\n\n")

buildingReport=sorter(buildingReport)
for key in buildingReport:
    print(buildingReport[key])
print("")
print("Total visible:",progress["totalNumberOfEntitiesCompleted"])
print("\n\n")

if len(unknownEntities)>0:
    print("list of unknown entities:")
    for item in unknownEntities:
        print(item)
