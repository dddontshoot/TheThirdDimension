from sys import argv

def getArgs():

        arguments=dict()

        if "--baseFile" in argv:
            arguments["baseFile"] = argv[argv.index("--baseFile") + 1:].pop(0)
        else:
            arguments["baseFile"] = str()

        if "--entityType" in argv:
            arguments["entityType"] = argv[argv.index("--entityType") + 1:].pop(0)
        else:
            arguments["entityType"] = str()

        if "--workingPath" in argv:
            arguments["workingPath"] = argv[argv.index("--workingPath") + 1:].pop(0)
        else:
            arguments["workingPath"] = str()

        if "--outputPath" in argv:
            arguments["outputPath"] = argv[argv.index("--outputPath") + 1:].pop(0)
        else:
            arguments["outputPath"] = str()

        if "--finalFilename" in argv:
            arguments["finalFilename"] = argv[argv.index("--finalFilename") + 1:].pop(0)
        else:
            arguments["finalFilename"] = str()

        if "--settings" in argv:
            arguments["settings"] = argv[argv.index("--settings") + 1:].pop(0)
        else:
            arguments["settings"] = str()

        if "--surfaceName" in argv:
            arguments["surfaceName"] = argv[argv.index("--surfaceName") + 1:].pop(0)
        else:
            arguments["surfaceName"] = str()

        if "--range" in argv:
            arguments["start"] = int(argv[argv.index("--range") + 1:].pop(0))
            arguments["finish"] = int(argv[argv.index("--range") + 2:].pop(0))
        else:
            arguments["start"] = int()
            arguments["finish"] = int()

        if "--reportOnly" in argv:
            arguments["reportOnly"] = True
        else:
            arguments["reportOnly"] = False

        if "--frag" in argv:
            arguments["frag"] = argv[argv.index("--frag") + 1:].pop(0)
        else:
            arguments["frag"] = str()

        if "--systemCheck" in argv:
            arguments["systemCheck"] = True
        else:
            arguments["systemCheck"] = False

        if "--force" in argv:
            arguments["force"] = True
        else:
            arguments["force"] = False

        if "--pseudobase" in argv:
            arguments["pseudobase"] = True
        else:
            arguments["pseudobase"] = False

        return(arguments)
