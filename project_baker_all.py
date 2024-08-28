#!/usr/bin/env python3
import os
import sys
import argparse
from argparse import RawTextHelpFormatter
from string import Template

DTYPE = ['java', 'nodejs', 'none', 'mysql', 'redis','ingress']
# if you want to use your own registry, please set it here
REGISTRY = ""

def create_application(args):

    # check project exist or not and create project crd
    if os.path.isdir(args.ns) == False:
        project_yaml = Template(
            open('.template_all/project.yaml', 'r').read()).substitute(vars(args))
        os.mkdir(args.ns)
        open(os.path.join(args.ns, args.project + '-project.yaml'), 'w').write(project_yaml)
    # check appliction exists or not
    if os.path.isdir(args.ns) and os.path.isdir(os.path.join(args.ns, args.dpath)):
        print("application {}/{} has exists".format(args.ns, args.app))
        sys.exit(1)
    base_dir = os.path.join(args.ns, args.dpath)

    # image combine
    args.image = '{}/{}/{}:test'.format(REGISTRY, args.ns, args.dpath)
    os.makedirs(base_dir)
    if args.dtype == 'mysql':
        service_yaml = Template(
            open('.template_all/service_mysql.yaml', 'r').read()).substitute(vars(args))
        deployment_yaml = Template(
            open('.template_all/deployment_mysql.yaml', 'r').read()).substitute(vars(args))
        kustom_yaml = Template(
            open('.template_all/kustomization_mysql.yaml', 'r').read()).substitute(vars(args))
        configmap_yaml = Template(
            open('.template_all/configmap_mysql.yaml', 'r').read()).substitute(vars(args))
    elif args.dtype == 'redis':
        service_yaml = Template(
            open('.template_all/service_redis.yaml', 'r').read()).substitute(vars(args))
        deployment_yaml = Template(
            open('.template_all/deployment_redis.yaml', 'r').read()).substitute(vars(args))
        kustom_yaml = Template(
            open('.template_all/kustomization_redis.yaml', 'r').read()).substitute(vars(args))
        configmap_yaml = Template(
            open('.template_all/configmap_redis.yaml', 'r').read()).substitute(vars(args))
    elif args.dtype == 'ingress':
        ingress_yaml = Template(
            open('.template_all/ingress.yaml', 'r').read()).safe_substitute(app=args.app)
        kustom_yaml = Template(
            open('.template_all/kustomization_ingress.yaml', 'r').read()).substitute(vars(args))
    else:
        service_yaml = Template(
            open('.template_all/service.yaml', 'r').read()).substitute(vars(args))
        deployment_yaml = Template(
            open('.template_all/deployment.yaml', 'r').read()).substitute(vars(args))
        kustom_yaml = Template(
            open('.template_all/kustomization.yaml', 'r').read()).substitute(vars(args))

    application_prod_yaml = Template(
        open('.template_all/application.yaml', 'r').read()).substitute(vars(args)).replace('env','prod')
    application_test_yaml = Template(
        open('.template_all/application-test.yaml', 'r').read()).substitute(vars(args)).replace('env','test')
    application_uat_yaml = Template(
        open('.template_all/application-uat.yaml', 'r').read()).substitute(vars(args)).replace('env', 'uat')

    if 'none' == args.dtype:
        # cleanup deployment content
        deployment_yaml = ''

    # create app crd fro argocd
    open(os.path.join(base_dir, args.app + '-app-prod.yaml'), 'w').write(application_prod_yaml)
    open(os.path.join(base_dir, args.app + '-app-test.yaml'), 'w').write(application_test_yaml)
    open(os.path.join(base_dir, args.app + '-app-uat.yaml'), 'w').write(application_uat_yaml)

    curpath = os.path.join(base_dir, 'base')
    os.mkdir(curpath)
    if args.dtype == 'ingress':
        open(os.path.join(curpath,'ingress.yaml'), 'w').write(ingress_yaml)
    else:
        open(os.path.join(curpath, 'deployment.yaml'), 'w').write(deployment_yaml)
        open(os.path.join(curpath, 'service.yaml'), 'w').write(service_yaml)
    open(os.path.join(curpath, 'kustomization.yaml'), 'w').write(kustom_yaml)


    if args.dtype == 'redis' or args.dtype == 'mysql':
        open(os.path.join(curpath, 'configmap.yaml'), 'w').write(configmap_yaml)

    # create test overlays
    curpath = os.path.join(base_dir, 'overlays', 'test')
    os.makedirs(curpath)
    with open(os.path.join(curpath, 'kustomization.yaml'), 'w') as f:
        f.write("namespace: {}\n".format(args.ns + "-test"))
        f.write("resources:\n  - ../../base\n")
        if 'java' == args.dtype:
            # add spring profile active env
            patch = Template(open('.template_all/patch.yaml', 'r').read()
                             ).substitute({'project': args.app, 'profile': 'test', 'ns': args.ns, 'app': args.app})
            f.write(patch)

    # create dev overlays
    curpath = os.path.join(base_dir, 'overlays', 'dev')
    os.makedirs(curpath)
    with open(os.path.join(curpath, 'kustomization.yaml'), 'w') as f:
        f.write("namespace: {}\n".format(args.ns + "-dev"))
        f.write("resources:\n  - ../../base\n")
        if 'java' == args.dtype:
            # add spring profile active env
            patch = Template(open('.template_all/patch.yaml', 'r').read()
                             ).substitute({'project': args.app, 'profile': 'dev', 'ns': args.ns, 'app': args.app})
            f.write(patch)

    # create uat overlays
    curpath = os.path.join(base_dir, 'overlays', 'uat')
    os.makedirs(curpath)
    with open(os.path.join(curpath, 'kustomization.yaml'), 'w') as f:
        f.write("namespace: {}\n".format(args.ns + "-uat"))
        f.write("resources:\n  - ../../base\n")
        if 'java' == args.dtype:
            # add spring profile active env
            patch = Template(open('.template_all/patch.yaml', 'r').read()
                             ).substitute({'project': args.app, 'profile': 'uat', 'ns': args.ns, 'app': args.app})
            f.write(patch)

    # create prod overlays
    curpath = os.path.join(base_dir, 'overlays', 'prod')
    os.makedirs(curpath)
    with open(os.path.join(curpath, 'kustomization.yaml'), 'w') as f:
        f.write("namespace: {}\n".format(args.ns))
        f.write("resources:\n  - ../../base\n")
        if 'java' == args.dtype:
            # add spring profile active env
            patch = Template(open('.template_all/patch.yaml', 'r').read()
                             ).substitute({'project': args.app, 'profile': 'prod', 'ns': args.ns, 'app': args.app})
            f.write(patch)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""ArgoCD 应用程序脚手架，用于快速创建一个满足 ArgoCD 规范的应用程序
       主要用于创建三类程序：Java类，nodejs类 以及空白应用程序
       比如：
       $prog -a foo -n default -t java
       则会创建 default/foo 目录，并按照 kustomization 规范创建子目录，填充 Java 类型程序的配置""",
       formatter_class=RawTextHelpFormatter)
    parser.add_argument('--application', '-a', dest='app', type=str,
                        help='ArgoCD 应用程序名,如果是mysql，名称建议为mysql，redis保持一样', required=True)
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
