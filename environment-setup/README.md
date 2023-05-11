**step 0**
# install anaconda 
https://www.anaconda.com/
https://docs.anaconda.com/free/anaconda/install/mac-os/

# install brew 
https://brew.sh/

**step 1**
use brew to install ffmpeg by running command 
brew install ffmpeg 

**step 2**
If you have create the environment that does not work, first remove the 
environment by the following command
conda remove --name gb-dev --full

Then running the following command to create the environment
conda env create -f environment.yaml

activating gb-dev environment
conda activate gb-dev

**step 3**
# update sound-file 
pip install --upgrade soundfile


