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

if groups $USER | grep &>/dev/null '\bdocker\b'; then
  CAPTAIN="captain"
else
  CAPTAIN="sudo captain"
fi

IMAGES="r-summary-stats r-linear-regression"

commit_id="$(git rev-parse --short HEAD)"

for image in $IMAGES ; do
  cd $ROOT_DIR/$image
  $CAPTAIN test
  $DOCKER push $image:$commit_id
  $DOCKER push $image:latest
done
