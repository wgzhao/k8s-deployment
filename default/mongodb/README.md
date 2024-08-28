# MongoDB Cluster

该集群的默认帐号为  `root`, 密码为 `EqLbNdh3QT76`

同时为 `graylog` 服务使用而创建下面的帐号： 

```
db.createUser({
    user: "graylog",
    pwd: "n5bymUNltxOc",
    roles: [
        {
            role: "dbOwner", db: "graylog"
        }
    ]
})
```