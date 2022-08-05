import sys
import pathlib
sys.path.append(str(pathlib.Path().absolute()))

import bpy
import lib.blender 

# intended command line for this module is:
# blender myfilename.blend -- python floompher.py

lib.blender.unselectEverything
#lib.blender.deleteDefaultCube() # no need to do this, it should have been removed by the concatenator.

# Damn you Python! Your two dimentional arrays are your most infuriating feature!
datumIndex=list()
datums=dict()
print("Now floomphing...")

# Create a collection for the Datums and, select it.
lib.blender.collectionCreate("Datum")
layer_collection = bpy.context.view_layer.layer_collection
bpy.context.view_layer.active_layer_collection = layer_collection.children["Datum"]

for item in bpy.data.objects.items():   # this selects from a list of every entitiy in the document.

    entity = item[1]
    #print("Floomphing",entity["name"])
    try:
        datumFilename = entity["filename"]
    except:
        datumFilename=""
    if datumFilename != "":
        datumIndexKey=entity.type+"-"+datumFilename
        if datumIndexKey not in datumIndex:
            datumIndex.append(datumIndexKey)
            importedObject=""
            if entity.type=="MESH":
                lib.blender.importObject(datumFilename,"Cube")
                importedObject=bpy.data.objects.get("Cube")
                
            if entity.type=="EMPTY":
                lib.blender.concatCollection(datumFilename,"TTD")
                importedObject=bpy.data.collections.get("TTD")

            if entity.type=="CURVE":
                lib.blender.importObject(datumFilename,"Bezier")
                importedObject=bpy.data.objects.get("Bezier")

            if importedObject != "":
                importedObject.name=datumIndexKey
                datums[datumIndexKey]=importedObject

        lib.blender.unselectEverything()

        if entity.type=="MESH":
            entity.data=datums[datumIndexKey].data

        if entity.type=="EMPTY":
            entity.instance_collection=datums[datumIndexKey]

        if entity.type=="CURVE":
            entity.data=datums[datumIndexKey].data

# We don't need to see the datums
bpy.data.collections.get("Datum").hide_viewport=True

lib.blender.saveAs(bpy.data.filepath)

print("==========================================")
print("============== Job is done! ==============")
print("==========================================")
