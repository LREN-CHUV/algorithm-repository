#!/bin/sh

SUMMARY_STATS_DIR="../../../../mip-functions/hbpsummarystats"

(cd $SUMMARY_STATS_DIR && ./build.sh && ./dist.sh)
cp $SUMMARY_STATS_DIR/hbpsummarystats_0.0.0.9000_R_x86_64-pc-linux-gnu.tar.gz downloads/
