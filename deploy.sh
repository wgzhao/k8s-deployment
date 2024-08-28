#!/bin/bash
# 获取新增的app和project,并且按顺序排列，先执行project，后执行app
set -ex
files=`git show --raw|awk '{print $5,$6}'|grep A|awk '{print $2}'|grep  -E "project|app"|awk '{print length(), $0| "sort -n" }'|awk '{print $2}'`
for file in $files
do
  if [[ $file =~ 'app' || $file =~ 'project' ]];then
      echo "hello world"
      rsync -R $file root@188.160.10.11:/root/argocd
      ssh root@188.160.10.11 "kubectl apply -f /root/argocd/$file"
#   elif [[ $file =~ 'test' || $file =~ 'uat' ]] && [[ `hostname` = "backend" ]];then
#       rsync -R $file root@master:/root/argocd
#       ssh root@master "kubectl apply -f /root/argocd/$file"
#   else
#       if [[ `hostname` = "V-CBB-JK" ]] && [[ ! $file =~ 'test' ]];then
#           rsync -R $file root@188.175.2.11:/root/argocd
#           ssh root@node27 "kubectl apply -f /root/argocd/$file"
#       elif [[ `hostname` = "backend" ]] && [[ ! $file =~ 'prod' ]];then
#           rsync -R $file root@master:/root/argocd
#           ssh root@master "kubectl apply -f /root/argocd/$file"
#       fi
  fi
done

