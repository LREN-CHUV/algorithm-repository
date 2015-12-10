#!/bin/sh

L_REGRESS_DIR="../../../../mip-functions/hbplregress"

(cd $L_REGRESS_DIR && ./build.sh && ./dist.sh)
cp $L_REGRESS_DIR/hbplregress_0.0.0.9000_R_x86_64-pc-linux-gnu.tar.gz downloads/
