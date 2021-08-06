import json

def ticker(counter,key):
    if key in counter.keys():
        counter[key]=counter[key]+1
    else:
        counter[key]=1
    return(counter)

def initReporting():
    progress=dict()
    progress["numberOfSurfacesCompleted"]          = int() # Progress meter of the number of surfaces that have been sucessfully imported.
    progress["numberOfSurfaces"]                   = int() # Total number of surfaces to be imported
    progress["numberOfEntitiesOnSurfaceCompleted"] = int() # Progress meter of the number of entities that have been sucessfully imported from THE CURRENT surface.
    progress["numberOfEntitiesOnSurface"]          = int() # Total number of entities to be imported from the current surface
    progress["totalNumberOfEntitiesCompleted"]     = int() # Progress meter of the number of entities that have been sucessfully imported from ALL surface.
    progress["totalNumberOfEntities"]              = int() # Total number of entities on all surfaces as read from the first line in the .base file.
    progress["numberOfIgnoredEntities"]            = int() # Total number of entities that are listed in the .base file, but will not be built.
    progress["entitiesAtTimestamp"]                = int()
    progress["cortos"]                             = int() # countOfEachTypeOnSurface["rocketsilo"]=1
    reportList=list()
    reportList.append("fileName")
    reportList.append("type")
    reportList.append("name")
    reportNot=dict()
    return(progress,reportList,reportNot)

def initUnknownEntity(meshPath):
    entityImportDetails=dict()
    entityImportDetails["name"]="blank entity"
    entityImportDetails["type"]="blank type"
    entityImportDetails["description"]="blank description"
    entityImportDetails["filename"]=meshPath+"arrow.blend"
    entityImportDetails["r"]=255
    entityImportDetails["g"]=255
    entityImportDetails["b"]=255
    entityImportDetails["visible"]=1
    entityImportDetails["3D"]=1
    return(entityImportDetails)

def displayPercentageCompleted(progress,timeStart,rate):
        import time
        #x = int(progress["totalNumberOfEntities"] / 100)
        x = int(progress["total"] / 100)
        if x != 0:
            y = progress["totalNumberOfEntitiesCompleted"] / x
        else:
            y=0
        if y==0:y=1
        if True: #(y - int(y) == 0) and (y > 0):
            percentage_completed = int(y)
            print("\n",percentage_completed, "% complete",end="")
        if False:
            print("\n",end="")
            print(time.strftime("%H:%M:%S",time.gmtime(time.time()-timeStart))," ",end="")
            #print(progress["totalNumberOfEntitiesCompleted"] , "of" , progress["totalNumberOfEntities"] , int(y),"%  ", end="")
            print(progress["totalNumberOfEntitiesCompleted"] , "of" , progress["total"] , int(y),"%  ", end="")
            if rate>1:print(int(rate),"item/s ",end="")
            if rate>0:
                #secondsRemaining=(progress["totalNumberOfEntities"]-progress["totalNumberOfEntitiesCompleted"])/rate
                secondsRemaining=(progress["total"]-progress["totalNumberOfEntitiesCompleted"])/rate
                print(time.strftime("%H:%M:%S", time.gmtime(secondsRemaining))," ",end="")

def sorter(unsorted=dict()):

    sorteddict=dict()
    failed=0

    while len(unsorted)>len(sorteddict):
        for current in unsorted.keys():
          if unsorted[current] != 0:
            for key in unsorted.keys():
              if unsorted[key] != 0:
                if unsorted[current] > unsorted[key]:
                    failed=1
            if failed==0:
                new=dict()
                new[current]=unsorted[current]
                sorteddict[len(sorteddict)]   =   json.dumps(   new   )
                unsorted[current]=0
            else:
                failed=0
    return(sorteddict)