-- ## v11 is stable and very good. I could make it public.
-- ## Changes in 12:
-- ## attempt to print list of blocked or allowed entities...
--    by moving the lists into a function
--    current problem:
--      How do I set a variable manually using the console? /c visible={}   ?
--      if I define a variable that already had information in it, the information is now lost :-(
--      So how do I test for the existance of a variable without crashing if the variable doesn't exist?

local json = require "json"

-- If the export takes too long, or the output files are too large,
-- you can adjust these values to include or ignore entity types.
function populateLists()

            ignore, visible = testForLists()

            ignore[#ignore+1]="tree"
            ignore[#ignore+1]="fish"
            ignore[#ignore+1]="cliff"
            ignore[#ignore+1]="simple-entity"


            visible[#visible+1]="assembling-machine"
            visible[#visible+1]="construction-robot"
            visible[#visible+1]="fluid-turret"
            visible[#visible+1]="ammo-turret"
            visible[#visible+1]="furnace"
            visible[#visible+1]="inserter"
            visible[#visible+1]="lab"
            visible[#visible+1]="logistic-robot"
            visible[#visible+1]="mining-drill"
            visible[#visible+1]="pipe"
            visible[#visible+1]="pipe-to-ground"
            visible[#visible+1]="splitter"
            visible[#visible+1]="transport-belt"
            visible[#visible+1]="underground-belt"
            visible[#visible+1]="wall"

            return ignore, visible
end

function testForLists()
        --game.print("Attempting to detect Ignore table...")
        if ignore == nil then
            --game.print("Ignore table not detected, initialising now...")
            ignore={}
        else
            --game.print("found Ignore table of length " .. #ignore)
            pass=0
        end

        --game.print("Attempting to detect Visible table...")
        if visible == nil then
            --game.print("Visible table not detected, initialising now...")
            visible={}
        else
            --game.print("found Visible table of length " .. #visible)
            pass=0
        end
        
        return ignore, visible
end

function printLists(tableIn)
    game.print("==========")
    ignore, visible = testForLists()

    if #ignore > 0 then
        game.print("contents of Ignore table:")
        for i = 1, #ignore do
            game.print(ignore[i])
        end
    end
    game.print("Ignore has " .. #ignore .. " items")

    game.print("==========")

    if #visible > 0 then
        game.print("contents of Visible table:")
        for i = 1, #visible do
            game.print(visible[i])
        end
    end
    game.print("Visible has " .. #visible .. " items")

    game.print("==========")
end

function ignore_clear() 
    ignore={}
    return ignore
end

function visible_clear()
    visible={}
    return visible
end

function ripper(tableIn)
    output=""
    eol=""
    for entity,properties in pairs(game.entity_prototypes) do
        --game.print(entity)
        --game.print(properties["type"])
        output=output .. eol .. entity .. "," .. properties["type"]
        eol="\n"
    end
    game.write_file("database.csv", output, false)
end

function listify(string)
    if string == nil then
        --game.print("dodged a bullet")
    else
        list={}
        prev=1
        for x = 1, #string+1 do
            if string:sub(x,x) == " " or x == #string+1 then
                l=string:sub(prev,x-1)
                if #l>0 then
                    list[#list+1] = string:sub(prev,x-1)
                end
                prev=x+1
            end
        end
    end
    return(list)
end

function help()
            game.print("/export         Command with no parameters will display this message.")       
            game.print("  -all          Export every surface in the game. Even those with spaces in their name.")
            game.print("  -surface <surfacename> <surfacename>")
            game.print("                Include only the surfaces following this parameter (for surface names that do not include spaces).")
            game.print("  -surface_ <surfacename> <surfacename>")
--            game.print("                Surface names that include spaces are not supported with this parameter, use -all instead.")
            game.print("                This parameter will convert underscore characters in all following surface names to a space character.")
            game.print("                eg /export -surface_ nauvis_orbit")
            game.print("                will export the surface called 'nauvis orbit'.")
            game.print("                This command does not support surface names that have both spaces and underscores. Use -all instead.")
            game.print("  -output  <filename>")
            game.print("                Sets the name of the output file. Default filename is 'mybase.base'.")
            game.print("  -visible      Include entity types in the hardcoded list of visible types only.")
            game.print("  -ignore       Ignore entity types on the hardcoded list, unless they is also in the list of visible types.")
            game.print("")
            game.print("eg:")
            game.print("/export -all")
            game.print("/export -surface nauvis")
            game.print("/export -all -output mybase.base -ignore")
            game.print("")
            game.print("Other commands:")
            game.print("")
            game.print("/printlists     Print the Ignore list and the Visible list to the console.")
            game.print("")
            game.print("/i <entity> <entity>")
            game.print("                Add entity types to the Ignore list")
            game.print("                eg /i tree fish")
            game.print("")
            game.print("/v <entity> <entity>")
            game.print("                Add entity types to the Visible list")
            game.print("                eg /v transport-belt inserter assembling-machine")
            game.print("")
            game.print("/ignore_clear   Remove all items from the list, ie reset the Ignore list to zero items.")
            game.print("")
            game.print("/visible_clear  Remove all items from the list, ie reset the Visible list to zero items.")
            game.print("")
            game.print("/populatelists  Add some hardcoded entity types to the Ignore and Visible lists.")
end

function export(tableIn)
    game.print("")
    --game.print("working...")

    universe = {}
    surfaceNames = {}
    surfaces = {}
    listOfTypes = {}
    listOfEntities = {}
    numberOfIgnored = 0
    job=""

    -- Default command line parameters
    fileName = "mybase.base"
    useVisible=0
    useIgnore=0
    useTypeList=0

    if tableIn.parameter == nil then
        help()
    else
        args=listify(tableIn.parameter)
        if args[1] == "-help" or args[1] == "-?" then
            help()
        else
            for x = 1,#args do
                if args[x] == "-all" then
                    for i = 1,#game.surfaces do
                        surfaceNames[i] = game.surfaces[i]["name"]
                    end
                    --game.print("Exporting all surfaces ("..#surfaceNames..")")
                else
                    if args[x] == "-surface" then
                        job="surface"
                    else
                        if args[x] == "-surface_" then
                           job="surface_"
                        else
                            if args[x] == "-output" then
                                job=""
                                fileName=args[x+1]
                            else
                                if args[x] == "-visible" then
                                    job=""
                                    useVisible=1
                                end
                                if args[x] == "-ignore" then
                                    job=""
                                    useIgnore=1
                                end
                                if job=="surface" then
                                    surfaceNames[#surfaceNames+1]=args[x]
                                end
                                if job=="surface_" then
                                    sname=args[x]
                                    for u = 1, #sname do
                                        if sname:sub(u,u) == "_" then
                                            sname=sname:sub(1,u-1).." "
                                        end
                                    surfaceNames[#surfaceNames+1]=sname
                                    end
                                end
                            end
                        end
                    end
                end
            end

            -- The next stage requires a working folder with the same name as the .base file. So now we need to make sure .base files have the .base extention.
            if fileName:sub(#fileName-4,#fileName) ~= ".base" then
                fileName = fileName .. ".base"
            end

            visible, ignore = testForLists()

            if useVisible==0 then
                game.print("Not using visible table")
            else
                game.print("Using visible table")
            end

            if useIgnore==0 then
                game.print("Not using ignore table")
            else
                game.print("Using ignore table")
            end

            if #surfaceNames==0 then
                surfaceNames[#surfaceNames+1]="nauvis"
            end
            game.print("Output filename:"..fileName)
            game.print(#surfaceNames.." surfaces")

            if #surfaceNames>0 then
              for sn = 1, #surfaceNames do
                game.print("Working on surface:" .. surfaceNames[sn])

                listOfEntities = game.surfaces[surfaceNames[sn]].find_entities()
                surface={}

                --entities[#entities+1]="#" .. #listOfEntities  --Sometimes it's nice to know the total number of entities
                game.print("Processing " .. #listOfEntities .. "Entities")

                for i = 1 ,#listOfEntities do

                    entityProperties = {}
                    typeIsKnown=0
                    ignoreThisEntity=0
                    typeIsVisible=0
                    hardVisible=0
                    hardIgnore=0

                    if useIgnore==1 then
                        for j = 1 , #ignore do
                            if ignore[j] == listOfEntities[i].type then
                                numberOfIgnored=numberOfIgnored+1
                                ignoreThisEntity=1
                            end
                        end
                    end
                    if useVisible==1 then
                        for k = 1,#visible do
                            if listOfEntities[i].type == visible[k] then
                                typeIsVisible=1
                            end
                        end
                    end
                    if ignoreThisEntity==1 and typeIsVisible==0 then
                        hardIgnore=1
                        hardVisible=0
                    end
                    if typeIsVisible==1 then
                        hardIgnore=0
                        hardVisible=1
                    end
                    if useVisible==0 and ignoreThisEntity==0 then
                        hardIgnore=0
                        hardVisible=1
                    end

                    if hardVisible==1 then    -- Entities will only be exported if they are on the visible list.
                        --if ignoreThisEntity==0 or typeIsVisible==1 then   -- Entities in the ignore list will be ignored unless they are also in the visible list. Unlisted entities will be exported.

                        if useTypeList==1 then  --I suspect this type list slows the export process significantly
                            for x = 1,#listOfTypes do
                                if listOfEntities[i].type == listOfTypes[x] then
                                    typeIsKnown=1
                                end
                            end
                            if typeIsKnown==0 then
                              listOfTypes[#listOfTypes+1]=listOfEntities[i].type
                            end
                        end

                        -- entity has passed all the tests, and will be processed for export.

                        -- record electrical network properties (test produces false posatives!)
                        --is_connected="nil"
                        --if  listOfEntities[i].is_connected_to_electric_network then
                        --    is_connected = "True"
                        --else
                        --    is_connected = "False"
                        --end

                        -- record circuit network properties
                        -- listOfEntities[i].circuit_connected_entities
                        -- listOfEntities[i].get_circuit_network.circuit_connector
                        -- listOfEntities[i].get_circuit_network.wire

                        -- record turret orientation
                        -- listOfEntities[i].relative_turret_orientation

                        -- record Spidertron torso orientation
                        -- listOfEntities[i].torso_orientation

                        -- record Inserter properties
                        -- listOfEntities[i].held_stack
                        -- listOfEntities[i].held_stack_position

                        -- record colour
                        if allow_manual_color==1 then
                            entityProperties["color"]=listOfEntities[i].color
                        end

                        entityProperties["name"]=listOfEntities[i].name
                        entityProperties["type"]=listOfEntities[i].type
                        entityProperties["x"]=listOfEntities[i].position.x
                        entityProperties["y"]=listOfEntities[i].position.y
                        entityProperties["direction"]=listOfEntities[i].direction
                        entityProperties["orientation"]=listOfEntities[i].orientation
                        surface[#surface+1]=json.encode(entityProperties)
                  end
                end
                surfaces[surfaceNames[sn]] = json.encode(surface)
              end
            end
            universe["surfaces"]=json.encode(surfaces)
            universe["metadata"]=json.encode(listOfTypes)

            game.print("Writing to file...")
            game.write_file(fileName, json.encode(universe),false)

            game.print("Done!")
            --numberOfEntities=#listOfEntities-numberOfIgnored
            --game.print(numberOfEntities .. " Entities exported")
            --game.print(numberOfIgnored .. " Entities ignored")
        end
    end
end

function ignore_add(tableIn)
    ignore, visible = testForLists()
    if tableIn.parameter == nil then
        game.print("usage: /i <entity1> <entity2> < entity3> etc...")
    else
        currentList = listify(tableIn.parameter)
        for i = 1, #currentList do
            ignore[#ignore+1]=currentList[i]
        end
    end
    return ignore, visible
end

function visible_add(tableIn)
    ignore, visible = testForLists()
    if tableIn.parameter == nil then
        game.print("usage: /v <entity1> <entity2> < entity3> etc...")
    else
        currentList = listify(tableIn.parameter)
        for i = 1, #currentList do
            visible[#visible+1]=currentList[i]
        end
    end
    return ignore, visible
end

commands.add_command("export","read the game data and export it",export)
commands.add_command("ripper","export all entity types",ripper)
commands.add_command("printlists","print the current list of favourite entities",printLists)
commands.add_command("populatelists","populate the Ignore list and the Visible list with hard coded entity types",populateLists)
commands.add_command("v","Add a type to the list of visible entities - eg /a inserter",visible_add)
commands.add_command("i","Add a type to the list of ignored entities - eg /i tree",ignore_add)
commands.add_command("ignore_clear","remove all items from the Ignore list",ignore_clear)
commands.add_command("visible_clear","remove all items from the Visible list",visible_clear)
