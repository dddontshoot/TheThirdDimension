# TheThirdDimension
Export your Factorio base into Blender

The data exporter is on the Factorio mod portal
https://mods.factorio.com/mod/TheThirdDimension_DataExporter
Development talk and support here: https://discord.gg/h8r8vpMb


Preparations:
=============
Before you start, you need these requirements:
- blender needs to be installed on your PATH.
    For Ubuntu users, you can set your path by editing the file called ".profile" in your home folder.
    For Windows users, Google is your best friend.
- Python3 needs to be installed on your PATH.


File locations:
===============
The main folder called TheThirdDimension goes into your Factorio folder.
The folder called TheThirdDimension_DataExporter goes into Factorio/Mods. Or you could just have Factorio download it from the mod portal, in which case, this folder can be deleted.
Also, take a look at TheThirdDimension/lib/settings.py you may need to edit that file to fit your setup.
I've put my 3D objects in Factorio/TheThirdDimension/Mesh/
And the csv file referencing them is in Factorio/TheThirdDimension/assets/


Exporting your base from Factorio:
==================================
You need to make sure the mod is installed before you load your saved game.
When you're in the game press the tilde key ~ to open the console and type:
/export -all
to export everything to a file called Factorio/script-output/mybase.base
You will see the screen freeze briefly while all the entities are collected and written to the file.
This could take anywhere from 2 seconds for a tiny base, to 5 minutes for a megabase, 
or longer if your base is rediculously larger than any of the ones we've been testing on.
It is a good idea to test your setup on a small base before jumping in and trying to export your megabase.


Execution:
==========
Open a command terminal in Factorio/TheThirdDimension/ and type:
python3 main.py --baseFile mybase.base

If everything goes smoothly, you'll have a folder called Factorio/TheThirdDimension/output 
that contains your base and a temporary folder with the same name.


Important:
==========

Keep an eye your disk space. There's a temporary working folder inside Factorio/output with a bunch of fragments,
they can be quite large, so you should delete them regularly.
And also, Blender likes to drop temporary files into its own temporary folder for some reason, so keep an eye on that too.

Make sure you move your export file to a safe folder. Mods have no way of checking if a file of the same name exists.
Any file left in the script-output folder risks being overwritten.

Also, it's a good idea to move your final blender file out of the output folder. I haven't written in any safeguards, 
so running the program a second time will overwrite any changes you made to the file manually.

Don't save your game with the mod installed. There's no benefit in doing so, and I haven't tested this with any other mods, 
and I don't want to be responsible for crashing your game and losing you an hours work.

And that's pretty much it, good luck :-)


Known bugs:
===========
- Half of the underneathies are around the wring way.
- Half of the curved rail are around the wrong way.
- All diagonal rail is wrong.
- Transport-belts always use the same mesh, so corners look like intersections.
- Walls and pipes don't automatically connect to their neighbours.
