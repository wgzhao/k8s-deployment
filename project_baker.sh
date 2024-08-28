#!/bin/bash
# quickly create a project template
# Usage:
# $0 <project group> <project name>

function usage() {
    echo "$0 <project group> <project name>..."
    echo "eg. $0 foo bar"
    echo "It will create foo/bar folder and populates templates"
    exit 0
}

function create_project() {
    group=$1
    project=$2

    [ -d "$group" ] || mkdir "$group"
    if [ -d "${group}/${project}" ];then
        echo "project ${group}/${project} has exists"
        exit 1
    fi

    mkdir "${group}/${project}"
    cd ${group}/${project}

    mkdir -p base overlays/{prod,test}
    touch base/{deployment.yaml,service.yaml}
cat <<-EOF >base/kustomization.yaml
namespace: ${group}
resources:
  - deployment.yaml
  - service.yaml
EOF

cat <<-EOF >overlays/test/kustomization.yaml
namespace: ${group}
resources:
  - ../../base/
EOF

cat <<-EOF >overlays/prod/kustomization.yaml
namespace: ${group}
resources:
  - ../../base/
EOF

cd ../../
}

if [ $# -lt 2 ];then
    usage
fi

group=$1
shift

for project in ${@}
do
  echo "create  $group/$project"
  create_project $group $project
done
