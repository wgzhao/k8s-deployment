# RocketMQ

该编排文件采取 2m-2s-noslave 部署模式，即两个 namesrv, 两个 broker，不包含 slave 节点。

注意，broker 采取 statefulset 类型，利用 pod 名称作为 `broker_name`，这样可以保证 broker 的名称不变，从而避免了 broker 重启后，名称变化导致的 broker 无法启动的问题。如果需要再增加 broker 时，只需要修改 `replicas` 参数即可。

访问方式：

集群内有两种方式方法，一种是直接指定 namesrv 的名字，为 `mqnamesrv-0.mqnamesrv-headless:9876;mqnamesrv-0.mqnamesrv-headless:9876`
另一种是通过 `service` 名称访问，则为 `rocketmq.default:9876`

注意，如果要增加 broker，在修改 `replicas` 参数之前，首先要执行下面的命令来创建所需要的目录，并设定好权限

```shell
BROKER="broker-<x>"
mkdir /data/k8sdata/rmq/{store,logs}/${BROKER}
chown -R 3000:3000 /data/k8sdata/rmq/{store,logs}/${BROKER}
```

其中 `<x>` 为编号，从 0 开始，例如第一个 broker 为 `broker-0`，第二个为 `broker-1`，以此类推。
