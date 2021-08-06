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
for item in bpy.data.objects.items():   # this selects from a list of every entitiy in the document.
    print("Floomphing",item)
    entity = item[1]    # entity
    try:
        datum = entity["filename"]
    except:
        datum=""
    if datum != "":
      if datum not in entitiesInUse:
        entitiesInUse.append(datum)
        # We haven't imported this file before, lets do that now.
        lib.blender.buildEntity(datum)
        lib.blender.unselectEverything()
        bpy.data.objects.get(datum).select_set(True)
        selected = bpy.context.selected_objects 
        if len(selected) > 0:
            newitem = selected.pop()
            meshes[datum]=newitem.data  # We're extracting the mesh from the imported datum,
      entity.data=meshes[datum]         # And inserting the into the blank objects.

lib.blender.deleteDatums(entitiesInUse)

lib.blender.saveAs(bpy.data.filepath)

print("==========================================")
print("============== Job is done! ==============")
print("==========================================")