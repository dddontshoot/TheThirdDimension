import os

# Other things to check for...
# presence of object libraries in the Mesh folder


def check(settings):

    fail=0

    # check for presence of basePath
    print("\nChecking basePath...")
    if not os.path.isdir(settings["basePath"]):    
        print("Could not find basePath folder ", settings["basePath"])
        fail=1
    else:
        print("basePath ok.")

    # check for presence of baseFile
    print("\nChecking baseFile...")
    if not os.path.isfile(settings["basePath"]+settings["baseFile"]):
        print("Could not find baseFile ", settings["basePath"]+settings["baseFile"])
        fail=1
    else:
        print("baseFile ok.")

    # check for presence of csvFile
    print("\nChecking csvFile...")
    if not os.path.isfile(settings["csvFile"]):
        print("Could not find csvFile ", csvFile)
        fail=1
    else:
        print("csvFile ok.")

    # check for presence of meshPath
    print("\nChecking meshPath...")
    if not os.path.isdir(settings["meshPath"]):
        print("Could not find meshPath folder ", settings["meshPath"])
        fail=1
    else:
        print("meshPath ok.")

    # check for presence of fragmentBuilder.py etc
    print("\nChecking dependancies...")
    listOfDependancies=(
    "fragmentBuilder.py",
    "concatenator.py",
    "floompher.py")
    
    for filename in listOfDependancies:
        if not os.path.isfile(filename):
            print("Could not find "+filename)
            fail=1
        else:
            print(filename, " ok.")




    # check Blender
    print("\nChecking Blender...")

    testFile="lib"+settings["pathCharacter"]+"blenderTest.py"

    if not os.path.isfile(testFile):
        print("Could not find ",testFile," are you using the correct pathCharacter?")
        fail=1
    else:
        print("Found Blender test. Executing now...")

        command="blender --python "+testFile+" --no-window-focus"
        result = os.system(command)
        if result > 0:
            print("Blender test failed. Do you have Blender installed? Is it on your PATH?")
            fail=1
        else:
            print("Blender executed sucessfully!")

    return(fail)