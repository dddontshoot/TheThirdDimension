import bpy
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
    masterCollection  = bpy.context.scene.collection
    #currentCollection = bpy.context.view_layer.active_layer_collection # Will this hold the newly imported fragment? ...well, it is currently selected.

    colSurfaceName = fragment["surfaceName"]
    colEntityName  = fragment["surfaceName"]+"-"+fragment["entityType"]

    if colSurfaceName not in collectionsInUse:
        
        # create a new collection inside it:
        lib.blender.collectionCreate(new=colSurfaceName, parent=bpy.context.scene.collection)

        # Add it to the list
        collectionsInUse.append(colSurfaceName)

    if colEntityName not in collectionsInUse:

        # create a new collection inside it:
        lib.blender.collectionCreate(new=colEntityName, parent=bpy.data.collections.get(colSurfaceName))

        # Add it to the list
        collectionsInUse.append(colEntityName)

    # select the correct collection ready to import the fragments directly into the right place.  # Also not helpful.
    layer_collection = bpy.context.view_layer.layer_collection.children[colSurfaceName].children[colEntityName]
    bpy.context.view_layer.active_layer_collection = layer_collection

    ######################################################

    section="\\Collection\\"
    #objectType = "Collection"
    #objectType = fragment["surface"]+"_"+fragment["collection"]
    objectType = fragment["collection"]

    directory = fragment["filename"] + section
    filename  = objectType
    filepath  = directory+filename

    newfragment=bpy.ops.wm.append(
    #filepath=filepath, 
    filename=filename, # lol
    directory=directory
    )

    # I'm expecting the newly imported fragment to just fall into the right place.
    #masterCollection.children.unlink(newFragment)

# save the final document, job is all done.
final=settings["outputPath"]+settings["finalFilename"]
print("> saving first draft",final)
lib.blender.saveAs(final)

exit(0)