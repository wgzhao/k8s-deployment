# k8s 基础服务编排仓库

该仓库是保存项目所需要的基础服务的容器编排配置文件，专为 [ArgoCD][1] 提供仓库同步使用。

## 基本术语

[ArgoCD][1] 有以下两个容易和我们的代码仓库以及 k8s 混淆的术语，说明如下：

- application: 对应的就是我们的一个实际项目，和代码仓库的要发布的仓库名称相对应
- project: 多个 `application` 的集合，他应该是和代码仓库的 `group` 以及 k8s 集群中的 `namespace` 相对应

## 目录结构

仓库按照 `project/application` 方式进行命名，其中 `project` 对应代码仓库中的 `group`， `application` 对应代码仓库中的 `repo`。

假定在代码托管服务器上(github，gitlab或者其他) 有一个名为 `foo` 的组，里面有一个名为 `bar` 的仓库，那么这个仓库的目录结构应该是这样的：

```
foo
├── bar
│   ├── base
│   └── overlays
│       ├── prod
│       └── test
│       └── dev
│       └── uat
```

考虑到 `application` 必须全局唯一，所以那些基础服务，比如 `redis`, `mysql`,`ingress`等，可以加上一个后缀来命名  `application`。

## 文件组织结构

一个 `application` 下的文件按照 [kustomize][2] 来组织资源，比如 `bar` 这个 `application` 的文件组织结构如下：

```
bar
├── base
│   ├── deployment.yaml
│   ├── kustomization.yaml
│   └── service.yaml
└── overlays
    ├── prod
    │   └── kustomization.yaml
    └── test
    │    └── kustomization.yaml
    └── uat
    │    └── kustomization.yaml
    └── dev
        └── kustomization.yaml
```

`base` 用于存储这个 `application` 的基本配置， `overlays` 用于定制化不同境下的不同配置，目前我们按照不同环境，可以创建 `prod`, `test`, `uat`,`dev` 等子目录。

在 kubernetes 上部署后，就类似于这样：

```
root@node11:~# kubectl   -n foo  get svc,deployment
NAME            TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
service/bar   ClusterIP     10.1.170.158   <none>        8080/TCP         169d

NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/bar      1/1     1            1        176d
```

这个更具体的配置和使用，可以参考 [kustomize 官方文档][2]

## 脚手架

[project_baker_all.py](./project_baker_all.py) 提供了快速创建一个 `application` 的功能，使用帮助如下：

```shell
usage: project_baker.py [-h] --application APP --namespace NS
                        [--project PROJECT] [--path DPATH]
                        [--type {java,nodejs,mysql,redis,ingress,none}] [--port PORT]

ArgoCD 应用程序脚手架，用于快速创建一个满足 ArgoCD 规范的应用程序
       主要用于创建三类程序：Java类，nodejs类, mysql, redis, ingress以及空白应用程序
       比如：
       $prog -a foo -n default -t java
       则会创建 default/foo 目录，并按照 kustomization 规范创建子目录，填充 Java 类型程序的配置

optional arguments:
  -h, --help            show this help message and exit
  --application APP, -a APP
                        ArgoCD 应用程序名
  --namespace NS, -n NS
                        要部署到 k8s 集群的哪个 namespace 里
  --project PROJECT, -p PROJECT
                        该应用程序属于 ArgoCD 的哪个 project，如果不指定，则和 namespace 相同
  --path DPATH, -d DPATH
                        该应用程序在该仓库的路径名称，默认和应用程序名相同
  --type {java,nodejs,redis,mysql,ingress,none}, -t {java,nodejs,redis,mysql,ingress,none}
                        应用程序类型
  --port PORT, -P PORT  应用程序的端口，默认是80
```

`type` 选项是用来预填充 `application` 编排物的内容，实际上就是把我们之前在 [sp-push][3] 中的编排模板拿过来就行了适当修改。
当前主要是针对 `java` 开发和 `nodejs` 开发设定了模板，如果你只是需要一个空的目录架构，选择 `none` 也可以。

[1]: https://argo-cd.readthedocs.io/en/stable/
[2]: https://kubernetes.io/zh/docs/tasks/manage-kubernetes-objects/kustomization/
[3]: https://github.com/wgzhao/sp-push
