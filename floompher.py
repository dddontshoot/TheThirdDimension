import sys
import pathlib
sys.path.append(str(pathlib.Path().absolute()))

import bpy
import lib.blender 

# intented command line for this module is:
# blender myfilename.blend -- python floompher.py

lib.blender.unselectEverything
#lib.blender.deleteDefaultCube() # no need to do this, it should have been removed by the concatenator.

meshes=dict()
entitiesInUse = list()
print("Now floomphing...")

# Create a collection for the Datums and, select it.
lib.blender.collectionCreate("Datum")
layer_collection = bpy.context.view_layer.layer_collection
bpy.context.view_layer.active_layer_collection = layer_collection.children["Datum"]

for item in bpy.data.objects.items():   # this selects from a list of every entitiy in the document.

    entity = item[1]
    #print("Floomphing",entity["name"])
    try:
        datum = entity["filename"]
    except:
        datum=""
    if datum != "":
      if datum not in entitiesInUse:

        # Add it to the list
        entitiesInUse.append(datum)

        # We haven't imported this file before, lets do that now.
        lib.blender.concatCollection(datum,"TTD")
        #lib.blender.buildEntity(datum) # Only needed if we go back to importing Objects.

        # Unselect it
        lib.blender.unselectEverything()

        # Store it ready for the next time we want to floomph something
        meshes[datum]=bpy.data.collections.get("TTD")
        #meshes[datum]=bpy.data.objects.get(datum) # Only needed if we go back to importing Objects.

        # And give it an appropriate name
        meshes[datum].name=datum

      # Finally, connect the empty instance to the appropriate datum
      entity.instance_collection=meshes[datum]
      #entity.data=meshes[datum].data # Only needed if we go back to importing Objects.

# We don't need to see the datums
bpy.data.collections.get("Datum").hide_viewport=True

lib.blender.saveAs(bpy.data.filepath)

print("==========================================")
print("============== Job is done! ==============")
print("==========================================")
