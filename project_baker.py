#!/usr/bin/env python3
import os
import sys
import argparse
from argparse import RawTextHelpFormatter
from string import Template

DTYPE = ['java', 'nodejs', 'none']
# if you want to use your own registry, please set it here
REGISTRY = ""

def create_application(args):
    # check appliction exists or not
    if os.path.isdir(args.ns) and os.path.isdir(os.path.join(args.ns, args.dpath)):
        print("application {}/{} has exists".format(args.ns, args.app))
        sys.exit(1)
    base_dir = os.path.join(args.ns, args.dpath)

    # image combine
    args.image = '{}/{}/{}:test'.format(REGISTRY, args.ns, args.dpath)
    os.makedirs(base_dir)
    service_yaml = Template(
        open('.template/service.yaml', 'r').read()).substitute(vars(args))
    deployment_yaml = Template(
        open('.template/deployment.yaml', 'r').read()).substitute(vars(args))

    kustom_yaml = Template(
        open('.template/kustomization.yaml', 'r').read()).substitute(vars(args))

    if 'none' == args.dtype:
        # cleanup deployment content
        deployment_yaml = ''

    curpath = os.path.join(base_dir, 'base')
    os.mkdir(curpath)
    open(os.path.join(curpath, 'deployment.yaml'), 'w').write(deployment_yaml)
    open(os.path.join(curpath, 'kustomization.yaml'), 'w').write(kustom_yaml)
    open(os.path.join(curpath, 'service.yaml'), 'w').write(service_yaml)

    # create test overlays
    curpath = os.path.join(base_dir, 'overlays', 'test')
    os.makedirs(curpath)
    with open(os.path.join(curpath, 'kustomization.yaml'), 'w') as f:
        f.write("namespace: {}\n".format(args.ns))
        f.write("resources:\n  - ../../base\n")
        if 'java' == args.dtype:
            # add spring profile active env
            patch = Template(open('.template/patch.yaml', 'r').read()
                             ).substitute({'project': args.app, 'profile': 'test'})
            f.write(patch)

    # create prod overlays
    curpath = os.path.join(base_dir, 'overlays', 'prod')
    os.makedirs(curpath)
    with open(os.path.join(curpath, 'kustomization.yaml'), 'w') as f:
        f.write("namespace: {}\n".format(args.ns))
        f.write("resources:\n  - ../../base\n")
        if 'java' == args.dtype:
            # add spring profile active env
            patch = Template(open('.template/patch.yaml', 'r').read()
                             ).substitute({'project': args.app, 'profile': 'prod'})
            f.write(patch)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""ArgoCD 应用程序脚手架，用于快速创建一个满足 ArgoCD 规范的应用程序
       主要用于创建三类程序：Java类，nodejs类 以及空白应用程序
       比如：
       $prog -a foo -n default -t java
       则会创建 default/foo 目录，并按照 kustomization 规范创建子目录，填充 Java 类型程序的配置""",
       formatter_class=RawTextHelpFormatter)
    parser.add_argument('--application', '-a', dest='app', type=str,
                        help='ArgoCD 应用程序名', required=True)
    parser.add_argument('--namespace', '-n', dest='ns', type=str,
                        help='要部署到 k8s 集群的哪个 namespace 里', required=True)
    parser.add_argument('--project', '-p', dest='project', type=str,
                        help='该应用程序属于 ArgoCD 的哪个 project，如果不指定，则和 namespace 相同', required=False)
    parser.add_argument('--path', '-d', dest='dpath', type=str,
                        help='该应用程序在该仓库的路径名称，默认和应用程序名相同', required=False)
    parser.add_argument('--type', '-t', dest='dtype', type=str,
                        help='应用程序类型', choices=DTYPE, default='java')
    parser.add_argument('--port', '-P', dest='port', type=int,
                        help='应用程序的端口，默认是80', required=False, default=8080)
    args = parser.parse_args()

    if not args.dpath:
        args.dpath = args.app

    if not args.project:
        args.project = args.ns

    create_application(args)
