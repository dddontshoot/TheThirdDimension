import bpy
import math

def meshCreate():
    mesh=bpy.data.meshes.new("mesh")
    return(mesh)

def bezierCreate():
    bezier=bpy.data.curves.new("newbezier","CURVE")
    return(bezier)

def newEntity(entityProperties, entityImportDetails, meshAdjustmentDatabase, collection, mesh):
    import math
    import json

    # Create a new object with basic mesh
    newObject = bpy.data.objects.new('new_object', mesh)

    # Add the object to a collection
    collection.objects.link(newObject)

    for item in entityProperties.keys():
        newObject[item]=entityProperties[item]

    # Mesh. Eventually, when we import the mesh, we'll need to know where to get it from.
    # Lets check to see if the entity matches the criteria for mesh adjustment.
    if entityProperties["name"] in meshAdjustmentDatabase.keys():
        #print("found matching entity name, comparing for",entityProperties["direction"])
        entityMeshAdjustment=json.loads(meshAdjustmentDatabase[entityProperties["name"]])
        if str(entityProperties["direction"]) in entityMeshAdjustment.keys():
            #print("replacing mesh...")
            newObject["filename"] = entityMeshAdjustment[str(entityProperties["direction"])]
        else:
                newObject["filename"]=entityImportDetails["filename"]
    else:
                newObject["filename"]=entityImportDetails["filename"]

    # Give the object an appropriate name
    newObject.name=entityProperties["name"]

    # Location
    newObject.location = (entityProperties["x"], entityProperties["y"], 0)

    # rotation # r is now set by the fragmentBuilder.py, and passed to blender.py
    #r = (entityProperties["direction"] * -45) + entityProperties["rotationAdjustment"]
    newObject.rotation_euler[2] = math.radians(entityProperties["r"])




def newObjectBezier(entityProperties, entityImportDetails,meshAdjustmentDatabase, collection, bezier):
    import math
    import json

    # Create a new object with basic mesh
    newObject = bpy.data.objects.new('new_object', bezier)

    # Add the object to a collection
    collection.objects.link(newObject)

    for item in entityProperties.keys():
        newObject[item]=entityProperties[item]

    # Mesh. Eventually, when we import the mesh, we'll need to know where to get it from.
    # Lets check to see if the entity matches the criteria for mesh adjustment.
    if entityProperties["name"] in meshAdjustmentDatabase.keys():
        #print("found matching entity name, comparing for",entityProperties["direction"])
        entityMeshAdjustment=json.loads(meshAdjustmentDatabase[entityProperties["name"]])
        if str(entityProperties["direction"]) in entityMeshAdjustment.keys():
            #print("replacing mesh...")
            newObject["filename"] = entityMeshAdjustment[str(entityProperties["direction"])]
        else:
                newObject["filename"]=entityImportDetails["filename"]
    else:
                newObject["filename"]=entityImportDetails["filename"]

    # Give the object an appropriate name
    newObject.name=entityProperties["name"]

    # Location
    newObject.location = (entityProperties["x"], entityProperties["y"], 0)

    # rotation # r is now set by the fragmentBuilder.py, and passed to blender.py
    #r = (entityProperties["direction"] * -45) + entityProperties["rotationAdjustment"]
    newObject.rotation_euler[2] = math.radians(entityProperties["r"])


def newInstance(entityProperties, entityImportDetails, meshAdjustmentDatabase, collection):

    ##### I'm using the name newObject, but don't forget that 
    ##### it's not an object, it's an instance.

    import math
    import json

    # Create a new collection_instance which is just a copy of an empty collection.
    bpy.ops.object.collection_instance_add(collection='Collection', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1)) # well, it created an instance, but I don't know how to access it.
    newObject=bpy.data.objects.get("Collection")

    # Give it an appropriate name
    newObject.name=entityProperties["name"]

    # Add the object to a collection
    collection.objects.link(newObject)

    # Fill in all the custom properties
    for item in entityProperties.keys():
        newObject[item]=entityProperties[item]

    # Mesh. Eventually, when we import the mesh, we'll need to know where to get it from.
    # Lets check to see if the entity matches the criteria for mesh adjustment.
    if entityProperties["name"] in meshAdjustmentDatabase.keys():
        #print("found matching entity name, comparing for",entityProperties["direction"])
        entityMeshAdjustment=json.loads(meshAdjustmentDatabase[entityProperties["name"]])
        if str(entityProperties["direction"]) in entityMeshAdjustment.keys():
            #print("replacing mesh...")
            newObject["filename"] = entityMeshAdjustment[str(entityProperties["direction"])]
        else:
                newObject["filename"]=entityImportDetails["filename"]
    else:
                newObject["filename"]=entityImportDetails["filename"]

    # Location
    newObject.location = (entityProperties["x"], entityProperties["y"], 0)

    # rotation
    #r = (entityProperties["direction"] * -45) + entityProperties["rotationAdjustment"]
    newObject.rotation_euler[2] = math.radians(entityProperties["r"])

def collectionCreate(new, parent=bpy.context.scene.collection):
    print("Creating collection ",new)
    
    if type(parent) == str:
        parent=bpy.data.collections.get(parent)

    myCollection = bpy.data.collections.new(new)   # yes, this is how you create a collection.
    parent.children.link(myCollection)             # The new collection resides in a void until this line links it in place.

    return(myCollection)

def collectionRemove(name):
    print("Removing collection ",name)
    item = bpy.data.collections.get(name)
    bpy.data.collections.remove(item)


def collectionRename(old,new):
    print("Renaming collection ",old,"to",new)
    item = bpy.data.collections.get(old)
    item.name=new

def collectionSelect(colSurfaceName,colEntityName):
    layer_collection = bpy.context.view_layer.layer_collection.children[colSurfaceName].children[colEntityName]
    bpy.context.view_layer.active_layer_collection = layer_collection

def deleteDefaultCube():
    print("Deleting the default objects.")

    unselectEverything()

    try:
        bpy.data.objects.get("Cube").select_set(True)  # It was set to FALSE!!!
    except:
        pass

    try:
        bpy.data.objects.get("Camera").select_set(True)
    except:
        pass

    try:
        bpy.data.objects.get("Light").select_set(True)
    except:
        pass

    bpy.ops.object.delete()

def unselectEverything():
        selected = bpy.context.selected_objects
        if len(selected) > 0:
            for obj in selected:
                obj.select_set(False)

def deleteDatums(entitiesInUse):
        print("Removing " + str(len(entitiesInUse)) + " datums now...")
        unselectEverything()
        for obj in entitiesInUse:
            bpy.data.objects[obj].select_set(True)
            bpy.ops.object.delete()

def saveAs(fragmentFilename):
    bpy.ops.wm.save_as_mainfile(filepath=fragmentFilename)

def buildEntity(datumFilename,objectName):
                        print("From",datumFilename,"importing",objectName)

                        section="\\Object\\"

                        filepath  = datumFilename + section + objectName
                        directory = datumFilename + section
                        filename  = objectName

                        bpy.ops.wm.append(
                        filepath=filepath, 
                        filename=filename, # lol
                        directory=directory
                        )
                        #bpy.data.objects[filename].name = datum

                        unselectEverything()

def buildBezier(entityProperties,entityImportDetails):
                        datum=entityImportDetails["filename"]
                        print("Importing bezier" , datum)

                        section="\\Object\\"

                        filepath  = datum + section + "Bezier"
                        directory = datum + section
                        filename  = "Bezier"

                        bpy.ops.wm.append(
                        filepath=filepath, 
                        filename=filename, # lol
                        directory=directory
                        )
                        selected = bpy.context.selected_objects
                        selected[0].name = datum+"-Bezier"
                        selected[0].location = (entityProperties["x"], entityProperties["y"], 0)
                        selected[0].rotation_euler[2] = math.radians(entityProperties["r"])

                        unselectEverything()

def concatCollection(fileName,collectionName):
                        print("Importing" , fileName,"/",collectionName)

                        section   = "\\Collection\\"

                        directory = fileName + section
                        filename  = collectionName
                        filepath  = directory+filename

                        bpy.ops.wm.append(
                        filepath=filepath, 
                        filename=filename, # lol
                        directory=directory
                        )

                        unselectEverything()
