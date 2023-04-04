#!/bin/bash

# Define source and destination directories
SRC_DIR=/Users/yike/opt/anaconda3/envs/gb-ui-dev/lib/python3.10/site-packages/
DEST_DIRS=( "." )

# packages to copy
PACKAGES=(
  "torchaudio"
  "torchvision"
  "librosa"
  "sklearn"
  "pyannote"
  "huggingface_hub"
  "whisper"
  "pytorch_metric_learning"
  "hmmlearn"
  "speechbrain"
  "certifi"
  "syllables"
)

# Copy packages from source to destination directories
copy_packages() {
  for pkg in "${PACKAGES[@]}"; do
    for dest_dir in "${DEST_DIRS[@]}"; do
      cp -r "${SRC_DIR}${pkg}" "${dest_dir}"
    done
  done
}

# Remove unnecessary files
remove_files() {
  rm libtorch_python.dylib libtorch.dylib libc10.dylib libtorch_cpu.dylib
}

# Create symbolic links
create_links() {
  ln -s ./torch/lib/libtorch_python.dylib libtorch_python.dylib
  ln -s ./torch/lib/libtorch.dylib libtorch.dylib
  ln -s ./torch/lib/libc10.dylib libc10.dylib
  ln -s ./torch/lib/libtorch_cpu.dylib libtorch_cpu.dylib
}

# Run the script
copy_packages
remove_files
create_links
