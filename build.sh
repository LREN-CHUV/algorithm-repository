#!/bin/bash -e

get_script_dir () {
     SOURCE="${BASH_SOURCE[0]}"

     while [ -h "$SOURCE" ]; do
          DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
          SOURCE="$( readlink "$SOURCE" )"
          [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
     done
     cd -P "$( dirname "$SOURCE" )"
     pwd
}

ROOT_DIR="$(get_script_dir)"

IMAGES="mip_node/r-summary-stats mip_node/r-linear-regression mip_federation/r-summary-stats mip_federation/r-linear-regression"

for image in $IMAGES ; do
  cd $ROOT_DIR/$image
  captain test
  captain push
done
