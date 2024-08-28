# ElasticSearch Cluster

为了安全，我们需要给集群设置密码，首次部署完后，执行下面的指令，进入到第一个节点

```shell
kubectl exec -it -n elk es-0 -- /bin/sh
```

然后执行下面的命令设置默认帐号的密码

```shell
bin/elasticsearch-setup-passwords interactive
Initiating the setup of passwords for reserved users elastic,apm_system,kibana,kibana_system,logstash_system,beats_system,remote_monitoring_user.
You will be prompted to enter passwords as the process progresses.
Please confirm that you would like to continue [y/N]y


Enter password for [elastic]:
Reenter password for [elastic]:
Enter password for [apm_system]:
Reenter password for [apm_system]:
Enter password for [kibana_system]:
Reenter password for [kibana_system]:
Enter password for [logstash_system]:
Reenter password for [logstash_system]:
Enter password for [beats_system]:
Reenter password for [beats_system]:
Enter password for [remote_monitoring_user]:
Reenter password for [remote_monitoring_user]:
Changed password for user [apm_system]
Changed password for user [kibana_system]
Changed password for user [kibana]
Changed password for user [logstash_system]
Changed password for user [beats_system]
Changed password for user [remote_monitoring_user]
Changed password for user [elastic]
```

上述要输入密码的地方均为 `yB6Wq-fUprsTJ`

如果你希望每个帐号都自动设置密码，则可以执行下面的命令

```shell
bin/elasticsearch-setup-passwords auto
```

## 更新说明

升级到 `8.7.0` 后，如果启用 `xpack.security.enabled` 后，就必须同时设置 TLS ，考虑到仅在集群内使用，所以暂时将此配置关闭

另外，目前 [analysis-ik](https://github.com/medcl/elasticsearch-analysis-ik) 不支持 `8.7.1`，所以暂时不升级

为了不改动官方镜像，我把插件独立放在 `/data/k8sdata/elk/es-plugins` 目录下，然后挂载到 POD 的 `/usr/share/elasticsearch/plugins` 目录。

这样要增加插件时，只需要把插件拷贝到上述目录，然后使用 `elasticsearch-plugin install <plugin name>` 即可
