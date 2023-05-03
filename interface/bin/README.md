Package Application
1. Requirement: 
    a. pyInstaller 
    Purpose: make .exe and .app file from the python script. 
    If the developer only needs to compile the python script 
    into a single executable or application file on their local
    machine, only using pyInstaller will be sufficient.

    Get PyInstaller: pyinstaller can be installed using pip, with the command: 
    - pip install pyinstaller          
  
    b. create-dmg 
    Purpose: make a .dmg file from .app file so that the app can be 
    distributed to other users 
    Get create-dmg: create-dmg can be installed using homebrew or npm, 
                    with one of the command: 
	- brew install create-dmg
	- npm install create-dmg
	
    c. Jamf Composer
    Purpose: make a .pkg file from .app file so that the app can be 
            distributed to other users 
    Get Jamf Composer: Jamf Composer can be downloaded from Jamf official 
                        website with a Jamf pro account or a Jamf now account 
 

    Macos operating system: 
    The following process only applies to Mac operating system. 
    In future project development, we will include instructions 
    on packaging the application for Windows and Linux operating system

2. files and purpose 
   The following files appear in the bin directories' 
   - build.sh: run pyInstaller with GailBot.spec to bundle the application, 
                pyInstaller will generated two directories, build and dist
                which is moved to install directory, 
                the  bundled application will appear in install/build/GailBot.app

   - buildDmg.sh: run create-dmg to create dmg , 
                The dmg will be stored in install/build/dmg

   - GailBot.spec: a spec sent to pyInstaller for packaging the application
   - ffmpeg: binary executable that will be copied over to packaged application 
 - 
3. Building GailBot Application as pkg 

   Step 1 Edit collect_lib.sh bash script
   go to /interface/bin/collect_lib.sh, change the path variable SRC_DIR 
   to be the local path that stores the python packages in the gailbot 
   development environment 

   Step 2 Bundle GailBot application through pyinstaller 
   We provided a bash script “build.sh” that includes command to build 
   the application. To run the script, use  the command: 
   - ./build.sh 

   Step 3 	build GailBot application dmgs
   We provided a bash script “buildDmg.sh” that includes command to build a 
   .dmg file from GailBot.app. To run the script, use the command: 
   - ./buildDmg.sh

   Step 4 
   The process will automatically create a GailBot application file,  and a 
   pop-up window  will appear to ask you to save the application under the 
   Application folder. Once this process is complete, you can run the 
   application in the Application folder. 


   Step 5 run shell script to collect library 
   	Go into the Gailbot application folder, cd unto GailBot.app/Content/Macos, run 
   	chmod +x collect_lib.sh 
   - ./collect_lib.sh
   Click on Application icon to make sure that the application can be opened 


   Step 6  Package the application using Jamf composer
   Add Gailbot.app to Jamf composer. This can be done by dragging the app directly 
   to the composer under sources on the sidebar. 


   Step 7 Configure the pkg Setting 
   Select the owner to be “root(0)”
   Select the group to be “wheel(0)”
   Check all check box under R W X , and confirm the mode is 777 
   Click on the “...” icon on the button and click on all options to 
   apply the same settings to the sub-files under applications folders

   Step 8 Packaging the application
   Click on the “Build as PKG” option at the Top to create the PKG file 
