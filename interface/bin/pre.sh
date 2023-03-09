#! /bin/bash
cp -r /Users/yike/opt/anaconda3/envs/gb-ui-dev/lib/python3.10/site-packages/torchaudio* .
cp -r /Users/yike/opt/anaconda3/envs/gb-ui-dev/lib/python3.10/site-packages/torchvision* .
cp -r /Users/yike/opt/anaconda3/envs/gb-ui-dev/lib/python3.10/site-packages/librosa* cp -r /Users/yike/opt/anaconda3/envs/gb-ui-dev/lib/python3.10/site-packages/librosa* ..
cp -r /Users/yike/opt/anaconda3/envs/gb-ui-dev/lib/python3.10/site-packages/sklearn* .
cp -r /Users/yike/opt/anaconda3/envs/gb-ui-dev/lib/python3.10/site-packages/pyannote* .
cp -r /Users/yike/opt/anaconda3/envs/gb-ui-dev/lib/python3.10/site-packages/ffmpeg* .
cp -r /Users/yike/opt/anaconda3/envs/gb-ui-dev/lib/python3.10/site-packages/huggingface_hub* .
cp -r /Users/yike/opt/anaconda3/envs/gb-ui-dev/lib/python3.10/site-packages/whisper .
cp -r /Users/yike/opt/anaconda3/envs/gb-ui-dev/lib/python3.10/site-packages/pytorch_metric_learning* .
cp -r /Users/yike/opt/anaconda3/envs/gb-ui-dev/lib/python3.10/site-packages/hmmlearn* .
cp -r /Users/yike/opt/anaconda3/envs/gb-ui-dev/lib/python3.10/site-packages/speechbrain* .
cp -r /Users/yike/opt/anaconda3/envs/gb-ui-dev/lib/python3.10/site-packages/certifi* .
cp -r /Users/yike/opt/anaconda3/envs/ml135_env_sp23/lib/python3.10/logging .
rm libtorch_python.dylib
rm libtorch.dylibrm libtorch.dylib
rm libc10.dylib
rm libtorch_cpu.dylib
ln -s ./torch/lib/libtorch_python.dylib libtorch_python.dylib
ln -s ./torch/lib/libtorch.dylib libtorch.dylib
ln -s ./torch/lib/libc10.dylib libc10.dylib
ln -s ./torch/lib/libtorch_cpu.dylib libtorch_cpu.dylib

