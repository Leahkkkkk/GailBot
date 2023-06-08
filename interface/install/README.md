Package Application
TODO: add link to composor
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
   - mkapp.sh:  run pyInstaller with GailBot.spec to bundle the application, 
                and move GailBot.app to Application folder. 
                a fully functional GailBot application is expected to be located 
                at /Applications folder after this script is run 
   - mklink.sh: run by mkapp.sh to make symlink for torch dynamic library files,
     - relatd issue on github in packaging torchaudio library 
     - https://github.com/pyinstaller/pyinstaller-hooks-contrib/issues/375            

   - GB.spec: a spec sent to pyInstaller for packaging the application
   - ffmpeg: binary executable that will be copied over to packaged application 
   - hook: conatin a hook script to facilitate pyinstaller collecting the packages 
  
3. Building GailBot Application as pkg 

   Step 1 make .app file using pyinstaller 
    run the following command:
    chmod +x mkapp.sh
    ./mkapp.sh
    check /Applications folder to make sure that GailBot.app is properlly installed
    and is able to run 
    
   Step 2  Package the application using Jamf composer
   Add Gailbot.app to Jamf composer. This can be done by dragging the app directly 
   to the composer under sources on the sidebar. 


   Step 3 Configure the pkg Setting 
   Select the owner to be “root(0)”
   Select the group to be “wheel(0)”
   Check all check box under R W X , and confirm the mode is 777 
   Click on the “...” icon on the button and click on all options to 
   apply the same settings to the sub-files under applications folders

   Step 4 Packaging the application
   Click on the “Build as PKG” option at the Top to create the PKG file 
