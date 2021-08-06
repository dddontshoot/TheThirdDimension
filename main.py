import sys
import pathlib
sys.path.append(str(pathlib.Path().absolute()))

import json
import os

#local modules
import lib.settings
from lib.args import getArgs
from lib.fileParser import parseBaseFile
from lib.fileParser import parseCSVFile
from lib.fileParser import writeFragmentList
import lib.systemCheck
#from lib.utils import ticker
from lib.utils import initReporting
import lib.report

# Load standard settings
settings=lib.settings.getSettings()

# Check for "--base" in the arguments. Value of coreID and entityType is redundant, but is required for compatability.
arguments=getArgs()

# Choose values from settings file or command line.
try:
    if len(settings["baseFile"]) > 0:
        pass
except:
    settings["baseFile"]=""

if len(arguments["baseFile"]) > 0:
    settings["baseFile"]=arguments["baseFile"]

if len(settings["baseFile"]) == 0:
    print("Please specify a base file to open using:")
    print("python3 main.py --baseFile <filename>")
    exit(1)

# Check that baseFile has ".base" extension
if settings["baseFile"][len(settings["baseFile"])-5 : len(settings["baseFile"])] == ".base":
    # Filename looks ok, let us divine the working folder and the final filename
    settings["workingPath"] = settings["baseFile"][0:len(settings["baseFile"])-5]+settings["pathCharacter"]
    settings["finalFileName"]=settings["baseFile"][0:len(settings["baseFile"])-5]+".blend"
else:
    print("== Base file must have '.base' extension!")
    print("== ",settings["baseFile"])
    exit(1)

# run system check
fail=lib.systemCheck.check(settings)
if fail == 1:
    print("\n"+("="*80))
    print("Failed system check! Please check lib.settings.py has the correct settings")

if fail == 1 and arguments["force"] == False:
    print("If you like, you can overide this system check with --force parameter")
    print("eg. python main.py --baseFile mybase.base --force")
    exit(1)

if arguments["systemCheck"] == True:
    exit(0)

print("\nContinuing...")

# Load the import details database
entityDatabase = parseCSVFile(settings["csvFile"], settings["meshPath"])

# Initialise reporting variables
progress,reportList,reportNot=initReporting()

# Load the .base file. listOfTypes is redundant.
surfaces=parseBaseFile(settings["basePath"]+settings["baseFile"])
progress["numberOfSurfaces"]=len(surfaces)

reportVisibleTypes, coetos, reportInvisibleTypes, unknownEntities = lib.report.buildReport(surfaces, settings, entityDatabase)
listOfTypes=reportVisibleTypes.keys()

lib.report.reportPrint(reportVisibleTypes,reportInvisibleTypes,unknownEntities)

if arguments["reportOnly"] == True:
    print("Report has been printed, quitting...")
    exit()

print("==",len(listOfTypes),"types in shortlist")
print("==",listOfTypes)

# lets make a folder for the final file, and a working folder for all the fragments.
if not os.path.exists(settings["outputPath"]):
    os.mkdir(settings["outputPath"])
if not os.path.exists(settings["outputPath"]+settings["workingPath"]):
    os.mkdir(settings["outputPath"]+settings["workingPath"])

result=0
fragmentList=list()
for surfaceName in surfaces:
  if result != 0:
        print("== skipping all remaining fragments")
  else:

    surface=json.loads(surfaces[surfaceName])
    cOETOS = json.loads(coetos[surfaceName])

    for settings["entityType"] in cOETOS.keys():    # Don't loop from listOfEntities which contains entities that are missing from some surfaces.
      if result != 0:
        print("== skipping all remaining fragments")
      else:

        for start in range(0, cOETOS[settings["entityType"]], settings["entityLimit"]):

          # Ctrl+c while fragmentBuilder.py is running will terminate that process only,
          # This if statement stops further instances of that process from starting.
          if result != 0:
            print("== skipping all remaining fragments")
          else:
            
            finish = start + settings["entityLimit"]

            # We're about to create a fragment, lets document it so the concatenator can find it later.
            
            fragment=dict()
            fragment["filename"]=settings["outputPath"]+settings["workingPath"]+"fragment-"+surfaceName+"-"+settings["entityType"]+"-"+str(start)+".blend"
            fragment["surfaceName"]=surfaceName
            fragment["entityType"]=settings["entityType"]
            fragment["collection"]=surfaceName+"-"+settings["entityType"]+"-fragment"
            fragmentList.append(json.dumps(fragment))

            # Execute the fragment builder inside Blender.
            command="blender --python fragmentBuilder.py --no-window-focus -- " + " --baseFile " + settings["baseFile"] + " --workingPath " + settings["workingPath"] + " --surfaceName " + surfaceName + " --entityType " + settings["entityType"] + " --range " + str(start) + " " + str(finish) + " --frag " + fragment["filename"]
            print("== running>",command,"\n")
            result=os.system(command)
            
# Now we drop a list of all those fragments into a file for the concatenator, even if there were errors.
writeFragmentList(fragmentList,settings)

if result != 0:
    print("== error ",result)
else:
    print("== Concatenating fragments")
    command="blender --python concatenator.py --no-window-focus -- --outputPath " + settings["outputPath"] + " --finalFilename " + settings["finalFileName"] + " --workingPath " + settings["workingPath"]
    print("== Running>",command,"\n")
    result=os.system(command)


if result != 0:
    print("== error ",result)
else:
    print("== Floomphing cubes into interesting entities")
    command="blender " + settings["outputPath"]+settings["finalFileName"] + " --python floompher.py"
    print("== Running>",command,"\n")
    result=os.system(command)
