#基于的基础镜像
FROM python:3.7
 
 
#语言编码设置
RUN localedef -c -f UTF-8 -i zh_CN zh_CN.utf8
ENV LC_ALL zh_CN.UTF-8

 
#将项目目录文件复制到镜像中,CODE_DIR是在基础镜像中定义的
COPY ./platform_scale $CODE_DIR/platform_scale/
 
#用国内源加速大包的安装
# COPY pip.conf /etc/pip.conf
RUN pip3 config set global.index-url http://mirrors.aliyun.com/pypi/simple
RUN pip3 config set global.timeout 60000
RUN pip3 config set install.trusted-host mirrors.aliyun.com
 
#安装项目依赖包
RUN pip3 install -r $CODE_DIR/platform_scale/requirements.txt
 
#暴露端口
EXPOSE 9832
  
#启动项目
CMD ["python3", "/opt/platform_scale/websocket.py"]