import sys
import pathlib
sys.path.append(str(pathlib.Path().absolute()))
import time
import json
import bpy

#local modules
import lib.settings
from lib.args import getArgs
from lib.fileParser import parseCSVFile
from lib.fileParser import parseBaseFile
from lib.fileParser import parseSettingsFile
from lib.fileParser import writeLogFile
import lib.blender
from lib.utils import ticker
from lib.utils import initReporting
from lib.utils import initUnknownEntity
from lib.utils import displayPercentageCompleted


# Load standard settings
settings=lib.settings.getSettings()

# Expect to recieve baseFile and entityType from main.py
arguments=getArgs()

settings["baseFile"]=arguments["baseFile"]
settings["workingPath"]=arguments["workingPath"]
settings["surfaceName"]=arguments["surfaceName"]
settings["entityType"]=arguments["entityType"]
settings["start"]=arguments["start"]
settings["finish"]=arguments["finish"]
settings["frag"]=arguments["frag"]
settings["pseudobase"]=arguments["pseudobase"]

# Lets throw away the default cube
lib.blender.deleteDefaultCube()

# I thought that removing the default collection was a good idea. It worked for a while...???
# Don't remove the default collection! I'm using it to create empty collection_instances!
#lib.blender.collectionRemove("Collection")

# Load the import details database
entityDatabase,meshAdjustmentDatabase, rotationAdjustmentDatabase = parseCSVFile(settings["csvFile"], settings["meshPath"])

# Initialise reporting variables
progress,reportList,reportNot=initReporting()

# Load the .base file.
if settings["pseudobase"] == False:
    surfaces=parseBaseFile(settings["basePath"]+settings["baseFile"])
else:
    surfaces=parseBaseFile(settings["outputPath"]+settings["workingPath"]+settings["baseFile"])
progress["numberOfSurfaces"]=len(surfaces)

#print("= Total number of surfaces =",    progress["numberOfSurfaces"])
#print("= Total number of entities on all surfaces = ",progress["totalNumberOfEntities"])

entitiesInUse=list()
timeStart=time.time()
timeStamp=0
event=dict()
listOfFragments=list()
counter=int()

myCollection=lib.blender.collectionCreate(settings["surfaceName"]+"-"+settings["entityType"]+"-fragment")
#mesh=lib.blender.meshCreate() # Only needed if we go back to importing Objects.
bezier=lib.blender.bezierCreate()
bezierList=list()
bezierList.append("straight-rail")
bezierList.append("curved-rail")

for surfaceName in surfaces.keys():   # this line could be replaced by a single surfaceName to be determined by the external python code.
  if surfaceName == settings["surfaceName"]:
    print("= Processing items on",surfaceName)

    surface=json.loads(surfaces[surfaceName])

    for item in surface:

        # Unpack entities from the surface
        entityProperties=json.loads(item)
        entityProperties["x"]=entityProperties["x"]*(-1) # For some reason Blender universe is backwards to everything else.
        entityProperties["surface"]=surfaceName

        # Try and find the entity in the database. If it's not there then report the finding of a new entity.
        if entityProperties["name"] == settings["entityType"]:
                # Lets pull the import details from the database
                entityImportDetails=json.loads(entityDatabase[entityProperties["name"]])
                #if entityImportDetails["3D"] == 1 and entityImportDetails["visible"] == 1: # The entity must be 2D and visible # This check is done by the report function from main.py
                if counter >= arguments["start"] and counter < arguments["finish"]:
                        
                        # Check if the entity needs a rotation adjustment
                        entityProperties["rotationAdjustment"]=0
                        if entityProperties["name"] in rotationAdjustmentDatabase:
                            if entityProperties["name"] not in entitiesInUse:
                                entitiesInUse.append(entityProperties["name"])
                                print("=", entityProperties["name"], entityProperties["direction"], "is listed in RotationAdjustment.json <----")
                            entityRotationAdjustment=json.loads(rotationAdjustmentDatabase[entityProperties["name"]])
                            if 999 in entityRotationAdjustment.keys() or "999" in entityRotationAdjustment.keys():
                                entityProperties["r"]=-360*entityProperties["orientation"]
                            else:
                              for index in entityRotationAdjustment.keys():
                                #print("(((",index,"))) (((",entityProperties["direction"],")))")
                                if int(entityProperties["direction"]) == int(index):
                                    #print("====== ",index,"is a listed index ======")
                                    entityProperties["rotationAdjustment"]=entityRotationAdjustment[index]
                              entityProperties["r"] = (entityProperties["direction"] * -45) + entityProperties["rotationAdjustment"]
                        else:
                              entityProperties["r"] = (entityProperties["direction"] * -45) + entityProperties["rotationAdjustment"]

                        lib.blender.newEntity(entityProperties, entityImportDetails, meshAdjustmentDatabase, myCollection)
                        #lib.blender.newEntity(entityProperties, entityImportDetails, meshAdjustmentDatabase, mesh) # Only needed if we go back to importing Objects.
                        if entityProperties["name"] in bezierList:
                            lib.blender.newEntity(entityProperties,entityImportDetails,meshAdjustmentDatabase,myCollection,bezier)
                            
                        progress["numberOfEntitiesOnSurfaceCompleted"] = progress["numberOfEntitiesOnSurfaceCompleted"] +1
                #print("= Entity number",arguments["start"]+progress["numberOfEntitiesOnSurfaceCompleted"],surfaceName,entityProperties["name"])
                counter=counter+1

    print("=",progress["numberOfEntitiesOnSurfaceCompleted"], "items processed")

# Filename is now passed from main.py
print("= Saving fragment",settings["frag"])
lib.blender.saveAs(settings["frag"])

print("= Completed\n\n")

exit(0)
