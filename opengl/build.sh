#/usr/bin/env bash

if [ -d "build" ]; then
    echo "Removing old build directory..."
    rm -rf build
fi

mkdir -p build
cd build
cmake ..
make
./main