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



### 持久化docker的镜像或容器的方法

Docker的镜像和容器可以有两种方式来导出

- `docker save #ID or #Name`
- `docker export #ID or #Name`

### docker save和docker export的区别

- 对于Docker Save方法，会保存该镜像的所有历史记录
- 对于Docker Export 方法，不会保留历史记录，即没有commit历史
- docker save保存的是镜像（image），docker export保存的是容器（container）；
- docker load用来载入镜像包，docker import用来载入容器包，但两者都会恢复为镜像；
- docker load不能对载入的镜像重命名，而docker import可以为镜像指定新名称。



**save命令** 

------

docker save [options] images [images...]

示例 
docker save -o nginx.tar nginx:latest 
或 
docker save > nginx.tar nginx:latest 
其中-o和>表示输出到文件，nginx.tar为目标文件，nginx:latest是源镜像名（name:tag）

**load命令**

------

docker load [options]

示例
docker load -i nginx.tar
或
docker load < nginx.tar
其中-i和<表示从文件输入。会成功导入镜像及相关元数据，包括tag信息

**export命令**

------

docker export [options] container

示例
docker export -o nginx-test.tar nginx-test

\#导出为tar

docker export #ID or #Name > /home/export.tar

其中-o表示输出到文件，nginx-test.tar为目标文件，nginx-test是源容器名（name）

**import命令**

------

docker import [options] file|URL|- [REPOSITORY[:TAG]]

示例
docker import nginx-test.tar nginx:imp
或
cat nginx-test.tar | docker import - nginx:imp