

```shell
# 服务端
# 若未安装git, 首先安装git
sudo apt-get install git

sudo adduser git
# 系统会提示设置密码，此时请设置好你的密码,设置email之类的可以按Enter回车默认为空
 
# 将git账号加入用户组
su
chmod u+w /etc/sudoers
vi /etc/sudoers
# 在root ALL=(ALL) ALL 下面添加 git ALL=(ALL) ALL
chmod u-w /etc/sudoers
 
su git
sudo mkdir -p /home/git/.ssh
sudo vim /home/git/.ssh/authorized_keys
# 此时把你电脑里面的rsa_pub(公钥)复制到authorized_keys中保存退出
 
sudo mkdir -p /home/gitcode
# 创建一个目录作为git仓库
 
sudo chown git:git /home/gitcode/
# 把仓库所有者指定为git

sudo chown -R git:git /home/git
# 把git文件夹下所有东西的所有者都指向git

cd /home/gitcode
git init --bare gittest.git
#使用git创建一个名为gittest的空仓库
 
sudo chown -R git:git gittest.git
#指定仓库的所有者指为git用户git组
 
 
# 客户端
#pull：
git clone git@192.168.201.230:/home/gitcode/gittest.git
#密码：123456

push：
git init
git add .
git  commit -m "提交的说明注释"

git remote add origin git@192.168.201.230:/home/gitcode/gittest.git
git push --set-upstream origin master 
git push

git remote rm origin 
git remote -v


# 禁止 git 用户 ssh 登录服务器
# 编辑 /etc/passwd
# 找到：
git:x:502:504::/home/git:/bin/bash
# 修改为
git:x:502:504::/home/git:/bin/git-shell
# 此时 git 用户可以正常通过 ssh 使用 git，但无法通过 ssh 登录系统。



#其他
git rm -r --cached . 　　#不删除本地文件
git rm -r --f . 　　#删除本地文件

git 修改remote
git remote -v
git remote rm origin
git remote add origin http://admin@127.0.0.1:8080/gitlib.git
git push -u origin master
```

