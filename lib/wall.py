import json
import lib.ortho
#import lib.distinctName
from lib.utils import distinctName
import lib.fileParser
#import lib.writeBasefile
import lib.matrix

def connect(surfaces, entityDatabase, addendingbasefile, arguments):
    # build list of connectors
    connectorShortlist = list() # List of entities that are of interest to the connector.
    connectsTo = dict() # Index of all connectors and the entities that they connect to.

    print("Building shortlist and index")
    for item in entityDatabase.keys():
        entityImportDetails=json.loads(entityDatabase[item])
        if entityImportDetails["visible"]==1:
          if len(entityImportDetails["connectsTo"])>0:
            connectorShortlist = connectorShortlist + entityImportDetails["connectsTo"].split(".")
            connectsTo[item]   = entityImportDetails["connectsTo"]

    print("=",len(connectsTo.keys()),"visible connectors found in database")
    pseudoSurfaces = dict()
    if len(connectsTo)>0:
        # Only procede if visible connectors are present.
        print(connectsTo.keys())
        #pseudoSurfaceName=lib.utils.distinctName(surfaces,"pseudoSurface")
        for surfaceName in surfaces.keys():
          pseudoSurfaceName=surfaceName
          pseudoSurface  = list()
          if len(arguments["surfaceName"]) == 0 or arguments["surfaceName"] == surfaceName:
            surface=json.loads(surfaces[surfaceName])
            print("\n= Connecting walls on",surfaceName,"...")

            x=0
            filteredSurface=list()

            print("= Building a filtered surface")
            for item in surface:
                # check all entities against the shortlist.
                # Then add them to the filteredSurface.
                entityProperties=json.loads(item)
                if entityProperties["name"] in connectorShortlist:
                    filteredSurface.append(json.dumps(entityProperties))

            print("= Filtered surface has",len(filteredSurface),"entities")
            matrix=lib.matrix.buildMatrix(filteredSurface)
            print("= matrix has",len(matrix.keys()),"lines")

            for item in filteredSurface:
                x=x+1
                # Unpack entities from the surface
                entityProperties=json.loads(item)
                entityProperties["x"]=entityProperties["x"]*(-1) # For some reason Blender universe is backwards to everything else.
                if entityProperties["name"] in connectorShortlist:
                        # entity is a wall type things that connects to something else
                        # Why am I still checking the shortlist? Everything on the filteredSurface is in the shortlist.
                        orthagonals=list()

                        if False: #for itemOther in surface:
                            # compare wall to every other item on the surface
                            entityPropertiesOther=json.loads(itemOther)
                            entityPropertiesOther["x"]=entityPropertiesOther["x"]*(-1) # For some reason Blender universe is backwards to everything else.
                            # using non-matrix search...
                            entityPropertiesOther["ortho"] = lib.ortho.go(entityProperties,entityPropertiesOther)
                            if entityPropertiesOther["ortho"] > 0:
                                # the two entities are next to each other... but are they the same type?
                                #print("\n",entityProperties["name"],entityProperties["x"],entityProperties["y"],"is orthagonal to",entityPropertiesOther["name"],entityPropertiesOther["x"],entityPropertiesOther["y"])
                                #print("before",orthagonals)
                                orthagonals.append(json.dumps(entityPropertiesOther))
                                #print("after",orthagonals)

                        else:
                            # checking the matrix...
                            orthagonals=lib.ortho.checkMatrix(matrix,entityProperties["x"],entityProperties["y"],connectorShortlist)
                        #print("length of orthagonals=",len(orthagonals),"\n",orthagonals)

                        # I should now have a list containing between 0 and 4 items that are next to the main entity.
                        if len(orthagonals)>0:
                          #print("found ",len(orthagonals),"neighbours")
                          for itemOther in orthagonals:
                            #print("itemOther=",itemOther)
                            entityPropertiesOther = json.loads(itemOther)
                            #print(type(entityPropertiesOther))
                            matchingConnectors=False
                            for connector in connectsTo.keys():
                                connectorList=connectsTo[connector].split(".")
                                #print("connector=",connector)
                                #print("connectorlist=",connectorList)
                                if entityProperties["name"] in connectorList:
                                  if entityPropertiesOther["name"] in connectorList:
                                    # the main entity, and the orthagonal one match!!!
                                    #print("match for ",entityPropertiesOther["x"],entityPropertiesOther["y"])
                                    entityPropertiesConnector=json.loads(entityDatabase[connector])
                                    #print("using",entityPropertiesConnector["name"])

                                    # So lets connect them with this new entity...
                                    newEntity=dict()
                                    newEntity["x"]=(entityProperties["x"]+entityPropertiesOther["x"])/2
                                    newEntity["y"]=(entityProperties["y"]+entityPropertiesOther["y"])/2
                                    newEntity["direction"]=entityPropertiesOther["ortho"]
                                    newEntity["filename"]=entityPropertiesConnector["filename"]
                                    newEntity["name"]=connector
                                    newEntity["orientation"]=1
                                    newEntity["rotationAdjustment"]=""
                                    newEntity["surface"]=item
                                    newEntity["type"]=entityPropertiesConnector["type"]

                                    # lib.matrix.insert will check for duplicates, and return with a boolean,
                                    # and it will also return the matrix with the new entity inserted into it.
                                    matrix,duplicate=lib.matrix.insert(matrix,newEntity)
                                    if duplicate == False:
                                        # but we still have to populate the new surface.
                                        newEntity["x"]=newEntity["x"]*(-1)
                                        pseudoSurface.append(json.dumps(newEntity))
                                        #print("pseudoSurface now has",len(pseudoSurface),"entries")
          pseudoSurfaces[pseudoSurfaceName]=json.dumps(pseudoSurface)
        print("= Attempting to write conecting entities into addending base file...")
        universe=dict()
        universe["surfaces"]=json.dumps(pseudoSurfaces)
        lib.fileParser.write(universe,addendingbasefile)
    else:
        # If no connectors are visible, then return an empty universe
        pseudoSurfaces=dict()
        surface=list()
        pseudoSurfaces["pseudoSurface"]=json.dumps(surface)
    return(pseudoSurfaces)
