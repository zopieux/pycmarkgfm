#!/bin/bash

set -ex

rm -rf ./build
mkdir -p build

( cd build && cmake ../third_party/cmark )

cp -f \
  build/extensions/cmark-gfm-extensions_export.h \
  build/src/cmark-gfm_export.h \
  build/src/cmark-gfm_version.h \
  build/src/config.h \
  generated/

rm -rf ./build
