
==============
WHAT IS GYES ?
==============

 Gyes is a Blender script that makes random materials. 

 One of the most basic ideas of Gyes is randomisation. The idea behind radomisation is that it can become tedious to change each parameter randomly when you dont have a specific direction to the result you want to achieve, a script will always do this many hundrends times faster. Instead of doing it by hand , Gyes give you the ability to create loads of random material in a few seconds and add them to the material list, then its a question of going in your material list keeping what you want and deleting what you dont like. 


===========================
WHERE I CAN DOWNLOAD GYES ?
===========================


 Go here 

https://github.com/kilon/Gyes/tree/

 Click Downloads, choose the download that fit your needs. (Download Zip will do)

========================
HOW DO I INSTALL GYES ?
========================

After you download the compressed file, uncompress to extract Gyes.py then go to Blender and install it like any other Addon. (user preferences -> Addons -> install add on -> Gyes -> enable the add on) . 

=================
HOW DO I USE IT ?
=================

 It should appear in the left panel of your viewport in the bottom side , but only if you have a mesh already selected and there is already a material assigned to your model.Create a new material for your object if you have not already. 

 Click "random material" button (see the second screenshot) and will keep adding materials to your mesh's material list, then you can simply go to the material list in material section of the main UI and choose the random material of your choosing. And thats it!!!

=========
UPDATES:
=========
 
9-6-2011

 *"Activate" button works on multiple selections
 * added next and previous button to browse through history
 * Added Store button to store random and non random edits to history
 * Script allows storage only on non-empty history index or the first empty history index 
  * optimised code to make it more readable and faster
  * added comments to explain fuctionality 


 6-6-2011

 * now random material, are stored in history. History is in essense a sophisticated undo tool
 * added GUI element for choosing the index in history, each random material stored in history has its own index
 * added Activate button, once you have chosen the index of the random material, this button will assign to the selected object the selected random material as active material. 
 
 4-6-2011
 * now randomises only assigned material, no need to assign the random material
 * now randomisation can apply to multiple mesh objects, with each one having a unique random material
 * added option to randomise Diffuse Shader
 * added option to randomise Diffuse Color
 * added option to randomise Specular Shader
 * added option to randomise Specular Color
 * added option to randomise Diffuse Intensity
 * added option to randomise Specular Intensity
 * added option to randomise Specular Hardness
 * added option to randomise Transparency

 25-5-2011

 * Gyes is now an addon and installs like any other addon. 

 24-5-2011

 * Added transparency randomisation , it now makes more interesting materials
 * Added all availiable specular shaders
