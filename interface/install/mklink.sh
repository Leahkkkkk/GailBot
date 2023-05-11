#!/bin/bash

# the destination directory of the app
SRC_DIR=../install/dist/GailBot.app/Contents/MacOS/
# Create symbolic links
remove_links () {
    rm libtorch_python.dylib libtorch.dylib libc10.dylib libtorch_cpu.dylib libtorchaudio.so 
}

create_links() {
  ln -s ./torch/lib/libtorch_python.dylib libtorch_python.dylib
  ln -s ./torch/lib/libtorch.dylib libtorch.dylib
  ln -s ./torch/lib/libc10.dylib libc10.dylib
  ln -s ./torch/lib/libtorch_cpu.dylib libtorch_cpu.dylib
  ln -s ./torchaudio/lib/libtorchaudio.so libtorchaudio.so
}

cd $SRC_DIR
remove_links
create_links
