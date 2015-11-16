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

for image in mip_node/r-summary-stats \
             mip_node/r-linear-regression \
             mip_federation/r-linear-regression; do

	cd $ROOT_DIR/$image
	captain push
done

