环境：

Linux NF5270M4 5.4.0-70-generic #78~18.04.1-Ubuntu SMP Sat Mar 20 14:10:07 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux

1、ubuntu更换国内源（https://blog.csdn.net/weixin_48080013/article/details/109871439）

1.1、

```shell
sudo cp /etc/apt/sources.list /etc/apt/sources.list.backup
```

1.2、

```shell
vi /etc/apt/sources.list
```

```shell
deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
```

1.3、

```shell
sudo apt update 
sudo apt upgrade
```



2、安装docker（https://blog.csdn.net/u012798683/article/details/88052528）

```shell
sudo apt update
```

```shell
sudo apt install apt-transport-https ca-certificates curl software-properties-common
```




```shell
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

```shell
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
```




```shell
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
```

```shell
sudo add-apt-repository "deb [arch=amd64] https://mirrors.aliyun.com/docker-ce/linux/ubuntu  bionic stable"
```



```shell
sudo apt update
```

```shell
apt-cache policy docker-ce
```

```shell
sudo apt install docker-ce
```



```shell
# 修改docker根目录空间
# 查看docker 根目录空间
docker info | grep Root

sudo mkdir -p /etc/systemd/system/docker.service.d/
sudo vi /etc/systemd/system/docker.service.d/devicemapper.conf

# 录入配置信息
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd  --graph=/nginx/docker

# 更新 docker
systemctl daemon-reload
systemctl restart docker
systemctl enable docker

# 查看docker 根目录空间
docker info | grep Root
```





3、更改用户权限

```shell
sudo chmod 775 VM_PLATFORM

# 查看root组下的所有用户
grep 'root' /etc/group  # 用户组配置文件
grep ':0:' /etc/passwd   # 用户基本信息

# 查看cvteam用户所在组
groups cvteam

# 新增cvteam用户 附加群组 docker组
sudo usermod -aG docker cvteam

# 修改cvteam用户 所属群组为 root
sudo usermod -g root cvteam
newgrp docker
```



4、安装Anaconda （https://zhuanlan.zhihu.com/p/166015018?utm_source=wechat_session）

```shell
wget https://repo.anaconda.com/archive/Anaconda3-latest-Linux-x86_64.sh
bash Anaconda3-latest-Linux-x86_64.sh

# 若未配置 ~/.bashrc 文件
export PATH=$PATH:/home/vincent/anaconda3/bin

source ~/.bashrc

conda init

# 创建python环境 platform
conda create -n platform python=3.8.5

# 下载源码
git clone git@192.168.201.230:/home/gitcode/shopping_check.git
pip install -r requirements.txt


# 如果使用 miniconda, 需配置国内的镜像服务器（或直接修改 ~/.condarc，添加清华源镜像配置，如下），若还是连接不上，可将 https 改为 http 再尝试
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --set show_channel_urls yes

# 清除索引缓存
conda clean -i 
```

```shell
# 清华源镜像配置(https://mirror.tuna.tsinghua.edu.cn/help/anaconda/),特别的 pytorch系列镜像因更新过于频繁未同步，如需要，通过 -i or -f 指定搜索下载，例: pip install torch==1.7.1+cu110 -f https://download.pytorch.org/whl/torch_stable.html 或 pip install -r requirements.txt -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
channels:
  - defaults
show_channel_urls: true
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
```



5、安装数据库

```shell
docker pull mysql:5.7

docker run -p 13306:3306 --restart always --name vm_mysql -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.7

# 进入数据库
docker exec -it vm_mysql bash

# docker 内部操作
mysql -uroot -p123456

# mysql 内部操作
# 查看数据库
SHOW DATABASES;
# 创建数据库 shopping
CREATE DATABASE IF NOT EXISTS shopping DEFAULT CHARACTER SET utf8mb4;
```



6、安装 nginx

```shell
sudo apt update
sudo apt install nginx

# 获取配置文件路径 和 配置文件语法检测
sudo nginx -t
# 设置测试平台相关nginx配置文件路径
sudo vi /etc/nginx/nginx.conf
include /raid/VM_PLATFORM/nginx/shopping.conf;

```



```nginx
# shopping.conf

proxy_cache_path /raid/VM_PLATFORM/nginx/cache levels=1:2 keys_zone=platformcache:10m max_size=10g inactive=60m use_temp_path=off;

server
    {
        listen 8998;
        server_name localhost;

        charset 'utf-8';

        gzip  on;
        gzip_min_length 1k;
        gzip_buffers 4 16k;
        gzip_http_version 1.0;
        gzip_comp_level 2;
        gzip_types text/plain application/javascript application/css  text/css application/xml text/javascript application/x-httpd-php image/jpeg image/gif image/png;
        gzip_vary off;
        gzip_disable "MSIE [1-6]\.";

        access_log /raid/VM_PLATFORM/nginx/logs/access.log;
        error_log /raid/VM_PLATFORM/nginx/logs/error.log;

        location /logs
        {
            alias /data_disk/vmdata/TASK/;
        }
        location /orders
        {
            alias /data_disk/vmdata/ORDERS/;
            proxy_cache platformcache;
        }
        location /images
        {
            alias /data_disk/vmdata/IMAGES/;
            proxy_cache platformcache;
        }
        location /api
        {
            proxy_pass http://172.30.232.103:8999;
        }
        location /
        {
            root /raid/VM_PLATFORM/nginx/dist;
            index index.html;
            proxy_cache platformcache;
        }
    }
```



7、线上订单数据迁移

```shell
# rsync 可实现增量同步  例: rsync -r cvteam@172.30.232.103:/home/cvteam/shopping/RAW/*_MZ202104* /data_disk/vmdata/RAW/
scp -r cvteam@172.30.232.103:/home/cvteam/shopping/RAW/*_MZ202104* /data_disk/vmdata/RAW/

scp -r cvteam@172.30.232.103:/home/cvteam/shopping/ORDERS/*_MZ202104* /data_disk/vmdata/ORDERS/

scp -r cvteam@172.30.232.103:/home/cvteam/shopping/PICTURE/*_MZ202104* /data_disk/vmdata/PICTURE/

scp -r cvteam@172.30.232.103:/home/cvteam/shopping/IMAGES/*_MZ202104* /data_disk/vmdata/IMAGES/

scp -r cvteam@172.30.232.103:/home/cvteam/shopping/TASK/* /data_disk/vmdata/TASK/

scp -r cvteam@172.30.232.103:/media/cvteam/ALLSKUIMAGE/* /data_disk/vmdata/ALLSKU/
```



8、安装 grpc client

```shell
docker load -i grpc_server_up.tar

# Configure.ini文件迁移
scp cvteam@172.30.232.103:/media/cvteam/GRPC_AUTO_TEST/DATA_SEND/Configure.ini /raid/VM_PLATFORM/GRPC/DATA_SEND

docker run -it --net host --ipc host  --rm  --cap-add sys_ptrace -v /raid/VM_PLATFORM/GRPC/:/home/ubt -w /home/ubt/DATA_SEND/  grpc_server_up /bin/bash -c '/home/ubt/grpcclient/build/grpcclient 0.0.0.0:50000 test.zip'
```



9、数据库迁移

```shell
python3 manage.py migrate   # 创建表结构

# 后续
python3 manage.py makemigrations mark  # model变更
python3 manage.py migrate mark   # 表结构迁移

# 数据库数据迁移
```



10、项目启动

```shell
conda activate platform
python manage.py runserver 0.0.0.0:8999
```



```shell
apt install screen
screen -v
screen -ls

screen -S platform (screen -R platform)
screen -ls
screen -r $pid

ctrl+a d
screen -d $pid

screen kill $pid
ctrl+a k
exit

kill -9 $pid
screen -wipe
```

11、linux 常用指令
```shell
# gpu 状态查询
nvidia-smi | grep 'MiB' | grep 'Default' | awk '{print $9, $11, $13}'

# 查询gpu使用情况
nvidia-smi | grep 'MiB' | grep -v 'Default' | awk '{print $2, $3, $5}'

```


12、 线上标注工具

```shell
docker pull dorowu/ubuntu-desktop-lxde-vnc

docker run --restart=always -p 36000:80 -e RESOLUTION=1920x1080 --name defect_360 -d -v /raid/huayan_nfs/:/raid/huayan_nfs/ -v /raid/defect/dataset/tools/:/tools/ dorowu/ubuntu-desktop-lxde-vnc


# 进入 defect_360 容器, 打开 ternimal (快捷键 F4)
# labelImg 源码： https://github.com/tzutalin/labelImg
apt updtae
apt install python3-pip

apt-get install pyqt5-dev-tools
pip3 install -r requirements/requirements-linux-python3.txt # 如果报错sip包版本不符，先删除原环境下的sip包(pip uninstall sip)再执行该命令

pip install Pillow==7.2.0

make qt5py3
python3 labelImg.py
python3 labelImg.py [IMAGE_PATH] [PRE-DEFINED CLASS FILE]
# 制作桌面入口文件 labelImg.sh
python /tools/labelImg/labelImg.py

# 容器保存
docker commit -a '修改人' -m '备注' defect_360  labelimg-nvc:v1
```

