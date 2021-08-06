import bpy

def meshCreate():
    mesh=bpy.data.meshes.new("mesh")
    return(mesh)

def newObject(entityProperties, entityImportDetails, collection, mesh):
    import math

    # Create a new object with basic mesh
    newObject = bpy.data.objects.new('new_object', mesh)

    # Add the object to a collection
    collection.objects.link(newObject)

    for item in entityProperties.keys():
        newObject[item]=entityProperties[item]

    # Mesh. Eventually, when we import the mesh, we'll need to know where to get it from.
    newObject["filename"]=entityImportDetails["filename"]

    # Give the object an appropriate name
    newObject.name=entityProperties["name"]

    # Location
    newObject.location = (entityProperties["x"], entityProperties["y"], 0)

    # rotation
    r = entityProperties["direction"] * -45
    newObject.rotation_euler[2] = math.radians(r)

def collectionCreate(new, parent=bpy.context.scene.collection):
    print("Creating collection ",new)

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

def buildEntity(datum):
                        print("Importing" , datum)

                        section="\\Object\\"

                        filepath  = datum + section + "Cube"
                        directory = datum + section
                        filename  = "Cube"

                        bpy.ops.wm.append(
                        filepath=filepath, 
                        filename=filename, # lol
                        directory=directory
                        )
                        bpy.data.objects[filename].name = datum

                        unselectEverything()

def concatCollection(datum):
                        print("Importing" , datum)

                        section="\\Collection\\"

                        filepath  = datum + section + "Collection"
                        directory = datum + section
                        filename  = "Collection"

                        bpy.ops.wm.append(
                        filepath=filepath, 
                        filename=filename, # lol
                        directory=directory
                        )

                        unselectEverything()

