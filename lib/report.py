import json

#local modules
import lib.settings
from lib.utils import ticker
from lib.utils import initReporting
from lib.utils import sorter

def buildReport(surfaces,settings,entityDatabase):

    # Initialise reporting variables
    progress,reportList,reportNot=initReporting()

    # load the base data
    #surfaces = parseBaseFile(settings["basePath"]+settings["baseFile"])

    print("Collecting data...")

    reportVisibleTypes=dict()
    reportInvisibleTypes=dict()
    unknownEntities=list()
    coetos=dict()
    print("== Now building shortlist")
    for surfaceName in surfaces.keys():
        countOfEachTypeOnSurface=dict()
        #if surfaceName == "nauvis":
        progress["numberOfSurfacesCompleted"]=progress["numberOfSurfacesCompleted"]+1
        print("== Processing items on",surfaceName)
        print("== Surface", progress["numberOfSurfacesCompleted"], "of", len(surfaces))
        surface=json.loads(surfaces[surfaceName])
        progress["totalNumberOfEntities"]=progress["totalNumberOfEntities"]+len(surface)
        for item in surface:

            # Unpack entities from the surface
            entityProperties=json.loads(item)

            # Try and find the entity in the database. If it's not there then report the finding of a new entity so it can be classified.
            if entityProperties["name"] not in entityDatabase:
                    if entityProperties["name"] not in unknownEntities:
                       unknownEntities.append(entityProperties["name"])
            else:
                    # Lets pull the import details from the database
                    entityImportDetails=json.loads(entityDatabase[entityProperties["name"]])
                    if entityImportDetails["3D"] == 1 and entityImportDetails["visible"] == 1: # The entity must be 3D and visible
                        progress["totalNumberOfEntitiesCompleted"]=progress["totalNumberOfEntitiesCompleted"]+1
                        reportVisibleTypes = ticker(reportVisibleTypes, entityProperties["type"])
                        countOfEachTypeOnSurface = ticker(countOfEachTypeOnSurface, entityProperties["type"])
                        #listOfTypes.append(entityProperties["type"]) # This is the most acurate place to generate the listOfTypes
                    else:
                        progress["numberOfIgnoredEntities"]=progress["numberOfIgnoredEntities"]+1
                        #totalinvisible=totalinvisible+1
                        reportInvisibleTypes = ticker(reportInvisibleTypes, entityProperties["type"])
        coetos[surfaceName]=json.dumps(countOfEachTypeOnSurface)
    progress["coetos"] = json.dumps(coetos)
        

    return(reportVisibleTypes,coetos,reportInvisibleTypes,unknownEntities)

def reportPrint(reportVisibleTypes,reportInvisibleTypes,unknownEntities):

    print("")

    if len(reportInvisibleTypes) > 0:
        # lets convert reportInvisibleTypes from a dict() into a sorted list()
        reportInvisibleTypes=sorter(reportInvisibleTypes)
        totalIgnored=0
        for key in reportInvisibleTypes.keys():
            print(reportInvisibleTypes[key])
            e = json.loads(reportInvisibleTypes[key])
            for k in e.keys():
                totalIgnored=totalIgnored+e[k]
        print("")
        print("Total invisible entities:", totalIgnored)
        print("\n\n")
    else:
        print("No invisible types")

    if len(reportVisibleTypes) > 0:
        reportVisibleTypes=sorter(reportVisibleTypes)
        totalVisible=0
        for key in reportVisibleTypes:
            print(reportVisibleTypes[key])
            e = json.loads(reportVisibleTypes[key])
            for k in e.keys():
                totalVisible=totalVisible+e[k]
        print("")
        print("Total visible entities:", totalVisible)
        print("\n\n")
    else:
        print("No visible types")


    if len(unknownEntities)>0:
        print("list of unknown entities:")
        for item in unknownEntities:
            print(item)
    else:
        print("no unknown entities")


