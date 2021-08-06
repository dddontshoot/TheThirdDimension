import json
import csv

def parseSettingsFile(settingsFile):
    print("opening",settingsFile)
    file=open(settingsFile,"r")
    return(json.loads(file.read()))


def parseCSVFile(csvfile, meshPath):
    print("Importing entityDatabase",csvfile)
    entityDatabase = dict()
    with open(csvfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            entityImportDetails = dict()
            x = 0
            if row[0][0:1] != "#":
                for cell in row:
                    #print(item)
                    #print(type(item))
                    if (x == 0):
                        entityImportDetails["name"] = cell
                    if (x == 1):
                        entityImportDetails["type"] = cell
                    if (x == 2): 
                        entityImportDetails["description"] = cell
                    if (x == 3):
                        if len(cell)==0:cell="arrow.blend"
                        entityImportDetails["filename"] = meshPath+cell
                    if (x == 4):
                        if len(cell)>0:
                            entityImportDetails["r"] = int(cell)
                        else:
                            entityImportDetails["r"] = 255
                    if (x == 5):
                        if len(cell)>0:
                            entityImportDetails["g"] = int(cell)
                        else:
                            entityImportDetails["g"] = 255
                    if (x == 6):
                        if len(cell)>0:
                            entityImportDetails["b"] = int(cell)
                        else:
                            entityImportDetails["b"] = 255
                    if (x == 7): 
                        if len(cell)>0:
                            entityImportDetails["visible"] = int(cell)
                        else:
                            entityImportDetails["visible"] = ""
                    if (x == 8):
                        if len(cell)>0:
                            entityImportDetails["3D"] = int(cell)
                        else:
                            entityImportDetails["3D"] = ""
                    x = (x + 1)
                #if typeProperties["type"][0:1] != "#":
                #if typeProperties["type"] == "fish":print(typeProperties)
                entityDatabase[entityImportDetails["name"]] = json.dumps(entityImportDetails)
    return(entityDatabase)

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


