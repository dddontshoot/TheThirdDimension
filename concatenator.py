import sys
import pathlib
sys.path.append(str(pathlib.Path().absolute()))
import json

#local modules
import lib.blender
from lib.args import getArgs
from lib.fileParser import readFragmentList

settings=dict()

arguments=lib.args.getArgs()
settings["outputPath"]=arguments["outputPath"]
settings["finalFilename"]=arguments["finalFilename"]
settings["workingPath"]=arguments["workingPath"]

# Lets throw away the default cube
lib.blender.deleteDefaultCube()

listOfFragments=readFragmentList(settings)

# Concatenate each of the fragments into the complete base.
print("> Total number of fragments",len(listOfFragments))

collectionsInUse=list()
for item in listOfFragments:
    fragment=json.loads(item)
    
    print("> from ",fragment["filename"]," Importing" , fragment["collection"])

    ############### Manage collection tree ##############

    colSurfaceName = fragment["surfaceName"]
    colEntityName  = fragment["surfaceName"]+"-"+fragment["entityType"]

    if colSurfaceName not in collectionsInUse:
        
        # create a new collection inside it:
        lib.blender.collectionCreate(new=colSurfaceName)

        # Add it to the list
        collectionsInUse.append(colSurfaceName)

    if colEntityName not in collectionsInUse:

        # create a new collection inside it:
        lib.blender.collectionCreate(new=colEntityName, parent=colSurfaceName)

        # Add it to the list
        collectionsInUse.append(colEntityName)

    # select the correct collection ready to import the fragments directly into the right place.  # Also not helpful.
    lib.blender.collectionSelect(colSurfaceName,colEntityName)

    ######################################################

    lib.blender.concatCollection(fragment["filename"],fragment["collection"])

# save the final document, job is all done.
final=settings["outputPath"]+settings["finalFilename"]
print("> saving first draft",final)
lib.blender.saveAs(final)

exit(0)
