import json
import csv

def parseSettingsFile(settingsFile):
    print("opening",settingsFile)
    file=open(settingsFile,"r")
    return(json.loads(file.read()))


def parseCSVFile(csvfile, meshPath):
    print("Importing entityDatabase",csvfile)
    entityDatabase = dict()
    meshAdjustmentDatabase = dict()
    rotationAdjustmentDatabase = dict()
    with open(csvfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            entityImportDetails = dict()
            entityMeshAdjustment = dict()
            entityRotationAdjustment = dict()
            # punch in some blanks so that old csv files don't crash
            entityImportDetails["meshAdjustment"] = ""
            entityImportDetails["rotationAdjustment"] = ""
            entityImportDetails["rotation"] = ""
            entityImportDetails["connectsTo"]=""

            x = 0
            if row[0][0:1] != "#":
                for cell in row:
                    #print(item)
                    #print(type(item))
                    if (x == 0): # entity name
                        entityImportDetails["name"] = cell
                        #print(cell)
                    if (x == 1): # entity type
                        entityImportDetails["type"] = cell
                    if (x == 2): # optional discription
                        entityImportDetails["description"] = cell
                    if (x == 3): # mesh filename
                        if len(cell)==0:cell="arrow.blend"
                        entityImportDetails["filename"] = meshPath+cell
                    if (x == 4): # colour R
                        if len(cell)>0:
                            entityImportDetails["r"] = int(cell)
                        else:
                            entityImportDetails["r"] = 255
                    if (x == 5): # colour G
                        if len(cell)>0:
                            entityImportDetails["g"] = int(cell)
                        else:
                            entityImportDetails["g"] = 255
                    if (x == 6): # colour B
                        if len(cell)>0:
                            entityImportDetails["b"] = int(cell)
                        else:
                            entityImportDetails["b"] = 255
                    if (x == 7): # visibility. 1 to include, 0 to exclude from build.
                        if len(cell)>0:
                            entityImportDetails["visible"] = int(cell)
                        else:
                            entityImportDetails["visible"] = ""
                    if (x == 8): # Is the entity 2D or 3D? 0 for 2D, 1 for 3D.
                        if len(cell)>0:
                            entityImportDetails["3D"] = int(cell)
                        else:
                            entityImportDetails["3D"] = ""
                    if (x == 9): # Directions for rotationAdjustment or meshAdjustment.
                        if len(cell)>0:
                            if entityImportDetails["name"] in meshAdjustmentDatabase.keys():
                                #print("pulling current details")
                                entityMeshAdjustment=json.loads(meshAdjustmentDatabase[entityImportDetails["name"]])
                            entityImportDetails["meshAdjustment"] = cell.split(".")
                            if type(entityImportDetails["meshAdjustment"]) == int:
                                #print("writing int:",entityImportDetails["meshAdjustment"])
                                entityMeshAdjustment[entityImportDetails["meshAdjustment"]]=entityImportDetails["filename"]
                            if type(entityImportDetails["meshAdjustment"]) == list:
                                #print("writing list:",entityImportDetails["meshAdjustment"])
                                for item in entityImportDetails["meshAdjustment"]:
                                    entityMeshAdjustment[item]=entityImportDetails["filename"]
                        else:
                            entityImportDetails["meshAdjustment"] = ""

                    if (x == 10): # Angle of rotation to be applied if adjusted.
                        if len(cell)>0:
                            entityImportDetails["rotation"] = int(cell)
                        else:
                            entityImportDetails["rotation"] = ""

                    if (x == 11): # List of directions to have their rotation adjusted.
                        if len(cell)>0:
                            if entityImportDetails["name"] in rotationAdjustmentDatabase.keys():
                                #print("pulling current details")
                                entityRotationAdjustment=json.loads(rotationAdjustmentDatabase[entityImportDetails["name"]])
                            entityImportDetails["rotationAdjustment"] = cell.split(".")
                            if type(entityImportDetails["rotationAdjustment"]) == int:
                                #print("writing int:",entityImportDetails["rotationAdjustment"])
                                entityRotationAdjustment[entityImportDetails["rotationAdjustment"]]=entityImportDetails["rotation"]
                            if type(entityImportDetails["rotationAdjustment"]) == list:
                                #print("writing list:",entityImportDetails["rotationAdjustment"])
                                for item in entityImportDetails["rotationAdjustment"]:
                                    entityRotationAdjustment[item]=entityImportDetails["rotation"]
                        else:
                            entityImportDetails["rotationAdjustment"] = ""

                    if (x == 12): # list of entities that this mesh will attempt to connect to.
                        if len(cell)>0:
                            entityImportDetails["connectsTo"]=cell
                        else:
                            entityImportDetails["connectsTo"]=""

                    x = (x + 1)
                #if typeProperties["type"][0:1] != "#":
                #if typeProperties["type"] == "fish":print(typeProperties)

                if len(entityImportDetails["meshAdjustment"]) >0:
                    #meshAdjustmentDatabase[entityImportDetails["name"]](json.dumps(entityMeshAdjustment))
                    meshAdjustmentDatabase[entityImportDetails["name"]]=(json.dumps(entityMeshAdjustment))
                else:
                    entityDatabase[entityImportDetails["name"]] = json.dumps(entityImportDetails)

                if len(entityImportDetails["rotationAdjustment"]) >0:
                    #rotationAdjustmentDatabase[entityImportDetails["name"]](json.dumps(entityRotationAdjustment))
                    rotationAdjustmentDatabase[entityImportDetails["name"]]=(json.dumps(entityRotationAdjustment))

    #print("entityDatabase=",len(entityDatabase))
    #print("meshAdjustmentDatabase=",len(meshAdjustmentDatabase))
    #print(meshAdjustmentDatabase)
    return(entityDatabase,meshAdjustmentDatabase, rotationAdjustmentDatabase)

def parseBaseFile(baseFile):
    print("Importing",baseFile)
    try:
        file=open(baseFile,"r")
    except:
        print("Failed to open",baseFile)
        exit(1)
    universe=json.loads(file.read())
    surfaces=json.loads(universe["surfaces"])
    return(surfaces)

def writeLogFile(logFile,event):
    print("Writing logfile",logFile)
    file=open(logFile,"w")
    output=""
    for item in event.keys():
        output=output+str(item)+","+event[item]+"\n"
        file.write(output)

def writeFragmentList(fragmentList,settings):
    print("Writing fragment list")
    filename=settings["outputPath"]+settings["workingPath"]+"fragment.list"
    file=open(filename,"w")
    file.write(json.dumps(fragmentList))

def readFragmentList(settings):
    print("Reading fragment list")
    filename=settings["outputPath"]+settings["workingPath"]+"fragment.list"
    file=open(filename,"r")
    fragmentList=json.loads(file.read())
    return(fragmentList)

def write(universe,basefile):
    print("writing to",basefile)
    file = open(basefile,"w")
    file.write(json.dumps(universe))
