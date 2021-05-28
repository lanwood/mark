## docker 常用操作命令

### MYSQL

```shell
docker pull mysql:5.7   # 拉取 mysql 5.7
docker run -p 3306:3306 --name mysql_local --restart always -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.7

docker run -p 3306:3306 --name mysql_local --restart always \
-v /usr/local/docker/mysql/conf:/etc/mysql \
-v /usr/local/docker/mysql/logs:/var/log/mysql \
-v /usr/local/docker/mysql/data:/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=123456 \
-d mysql:5.7

# docker run ：根据镜像创建一个容器并运行一个命令，操作的对象是 镜像；
# docker exec ：在运行的容器中执行命令，操作的对象是 容器。

docker run -it mysql:5.7 /bin/bash
docker run --name docker-test -d platform:1.0 ping www.baidu.com
docker run -it --name yolo_env python:3.7  /bin/bash

docker exec -it mysql_local bash
# 进入 mysql_local 容器
mysql -uroot -p123456

docker commit -a '修改人' -m '备注' mysql_local  mysql:v2


```



