def getSettings():      # This file stores the file locations for your computer.
    print("Importing settings")
    settings=dict()

    settings["baseFile"]="mybase.base"             # Default file name only. Will be overridden by file names in the command line.
                                                   # baseFile should always have the extention .base to distinguish it from the working folder of the same name.
    settings["basePath"]="../script-output/"       # Filenames in the command line will be relative to this path. use settings["basePath"]="" for no path.
    settings["csvFile"]="assets/database_MasterList.csv" # Location of the reference database.
    settings["meshPath"]="Mesh/"                   # Location of the small entities to be imported into blender.
    settings["outputPath"]="output/"               # this settings is now obsolete. An output folder will be created with a name that matches the .base file.
    settings["pathCharacter"]="/"                  # use "/" for Linux, or "\\" for Windows.
    #settings["pathCharacter"]="\\"                 # using the wrong symbol here might not stop the program from running, but it could result in some interesting filenames.
    settings["entityLimit"]=1000                # entities with populations greater then this number will be spread over several files.

    return(settings)