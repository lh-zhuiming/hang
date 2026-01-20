# Docker容器虚拟化

![image-20251012162941568](local_image/image-20251012162941568.png)

## 一、简介

### （1.1）概述

**容器：**隔离的、易于使用的软件程序运行环境，类似于沙箱

**虚拟化：**使用相关技术模拟出某个组件/程序的功能

**容器虚拟化：**使用相关技术模拟出一个隔离的软件程序运行环境并运行软件程序

![image-20251012163145026](local_image/image-20251012163145026.png)



### （1.2）docker介绍

#### 1.2.1 docker概念

**什么是docker？**

docker是一个容器虚拟化管理系统/平台，用来管理容器虚拟化，例如容器的创建、删除

**和传统虚拟化的区别**

![image-20251012163544135](local_image/image-20251012163544135.png)

#### 1.2.2 docker框架

Docker是一个CS架构的容器虚拟化管理平台。

![image-20251012163702280](local_image/image-20251012163702280.png)

主要组件包括：

- **客户端**

  主要用于向服务端发送命令请求，实际表现形式是一系列的shell命令，如下图

  ![图片1](local_image/图片1.png)

- **守护进程**

  默认情况下和客户端处于同一主机节点（同一个宿主机下），作用是接收客户端发送的命令请求并执行。和客户端之间通过TCP（早期）/套接文件进行数据通信

- **镜像**

  主要作用是告诉服务端按照那种环境（操作系统核心、系统环境等）来创建容器

- **容器**

  程序及程序运行的环境

- **镜像仓库**

  存储镜像的地址，默认地址是`https://hub.docker.com/`,当我们客户端发送镜像拉取命令时，服务端会到镜像仓库去搜索和拉取镜像。而当我们客户端发送镜像推送命令时，服务端会到本地镜存储到镜像

**补充：**服务端、镜像、容器的关系好比下图

![image-20251012164457286](local_image/image-20251012164457286.png)

### （1.3）docker多容器管理

一些复杂的环境往往需要多个容器才能实现。多次执行docker命令来逐一创建则效率过低同时不方便管理。因此需要使用工具同时管理多个容器的操作。这类工具，通常被称为容器编排工具

#### 1.3.1 Docker Composet 编排工具

Docker Compose是一个工具，通常会结合docker-compose.yml文件。用于定义和运行多容器Docker应用程序。它可以帮助用户将多个Docker容器组织和连接起来，以实现复杂的应用程序部署和管理。

工作流程如下图：

![image-20251012165656344](local_image/image-20251012165656344.png)

#### 1.3.2 Kubernetes集群管理工具

Kubernetes是一个开源的容器编排系统，用于自动部署、扩缩和管理容器化应用程序。它提供了一种优雅的方式来部署、管理和扩展容器化应用程序，是云原生应用的理想选择。

Kubernetes用于多个服务器上进行docker容器部署

工作架构图：

![image-20251012170144360](local_image/image-20251012170144360.png)

控制台面板

![image-20251012170128681](local_image/image-20251012170128681.png)

### （1.4）补充：镜像拉取

#### 1.4.1 代理

查找并使用支持海外镜像的国内镜像源（如Azure中国镜像`dockerhub.azk8s.cn`、中科大镜像`docker.mirrors.ustc.edu.cn`），命令如下

> 在网站`https://status.1panel.top/status/docker` 查看可以使用的镜像仓库源

```shell
tee /etc/docker/daemon.json << EOF
 {
 
  "registry-mirrors": ["http://docker.mirrors.ustc.edu.cn/"]
 
}
EOF
```

如本地有部署代理，也可修改/添加 docker配置文件`/etc/docker/daemon.json`内容如下

```json
    {
      "proxies": {
        "default": {
          "httpProxy": "http://your-proxy-address:port",
          "httpsProxy": "http://your-proxy-address:port",
          "noProxy": "localhost,127.0.0.1"
        }
      }
    }
```

来连接代理

#### 1.4.2 拉取前缀网站（快速）

如下图

![image-20251012174347027](local_image/image-20251012174347027.png)

例如：

```shell
docker pull m.daocloud.io/docker.io/library/nginx
```

#### 1.4.3 镜像转存

使用Github Action将DockerHub镜像转存到阿里云私有仓库，供国内服务器使用，免费易用，前置条件

1、创建并注册阿里云账号

`https://cn.aliyun.com/`

2、创建并Github账号

`https://github.com/`

github上有开源的自动操作项目，可以直接fork过来使用

步骤参考：

- **【1】配置阿里云**

  登录阿里云容器镜像服务<br>
  https://cr.console.aliyun.com/<br>
  启用个人实例，创建一个命名空间（**ALIYUN_NAME_SPACE**）

  ![image-20251012171050338](local_image/image-20251012171050338.png)

  访问凭证–>获取环境变量<br>
  用户名（**ALIYUN_REGISTRY_USER**)<br>
  密码（**ALIYUN_REGISTRY_PASSWORD**)<br>
  仓库地址（**ALIYUN_REGISTRY**）<br>

  ![image-20241224112417133](local_image/image-20241224112417133.png)

- **【2】Fork项目**

  访问项目地址`https://github.com/tech-shrimp/docker_image_pusher`然后选择fork

  ![image-20251012171641104](local_image/image-20251012171641104.png)

  完成后，进入fork成功的项目，点击Action，启用Github Action功能

  进入Settings->Secret and variables->Actions->New Repository secret
  ![image-20251012172147693](local_image/image-20251012172147693.png)
  如上图，将上一步的 ALIYUN_NAME_SPACE,ALIYUN_REGISTRY_USER，ALIYUN_REGISTRY_PASSWORD，ALIYUN_REGISTRY
  的值配置成环境变量

- **【3】添加镜像**

  打开images.txt文件，添加你想要的镜像，可以带tag，也可以不用(默认latest)<br>

  ![image-20251012172524093](local_image/image-20251012172524093.png)

  ![image-20251012172536071](local_image/image-20251012172536071.png)

  文件提交后，自动进入Github Action构建

- 【4】使用镜像

  回到阿里云，镜像仓库，点击任意镜像，可查看镜像状态。(可以改成公开，拉取镜像免登录)

  ![image-20251012172625635](local_image/image-20251012172625635.png)

  在国内服务器pull镜像

  ```shell
  docker pull registry.cn-hangzhou.aliyuncs.com/shrimp-images/alpine
  ```

  registry.cn-hangzhou.aliyuncs.com 即 ALIYUN_REGISTRY<br>
  shrimp-images 即 ALIYUN_NAME_SPACE<br>
  alpine 即阿里云中显示的镜像名<br>

## 二、实操

### （2.1）安装docker

我们通过yum的方式来安装docker

执行如下命令：

```shell
#安装阿里云的docker镜像源
wget -O /etc/yum.repos.d/docker-ce.repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
#安装docker
yum -y install docker-ce
# 启动docker
systemctl start docker
# 开机启动docker
systemctl enable docker
# 查看docker运行状态
systemctl status docker
```

![image-20251012172911036](local_image/image-20251012172911036.png)

**补充（选择）：**修改docker的仓库地址

```shell
# 创建远程仓库配置文件
tee /etc/docker/daemon.json << EOF
 {
 
  "registry-mirrors": ["http://docker.mirrors.ustc.edu.cn"]
 
}
EOF
# 重启docker加载配置文件
# 重启docker服务端
systemctl daemon-reload
# 重启docker客户端
systemctl restart docker
```

### （2.2）docker操作

#### 2.2.1 拉取镜像

拉取稳定版的nginx 

执行下面命令：

```shell
#拉取镜像
docker pull m.daocloud.io/docker.io/library/nginx:stable-otel
#更名
docker tag  m.daocloud.io/docker.io/library/nginx:stable-otel nginx:stable-otel
#删除源镜像标签
docker rmi m.daocloud.io/docker.io/library/nginx:stable-otel
#查看镜像
docker images 
```

![image-20251012180433439](local_image/image-20251012180433439.png)

#### 2.2.2 启动容器

我们参考之前的中间件介绍，启动一个nginx 服务的容器，并且展示一个静态html页面

- **html页面**

  ```shell
  mkdir -p /opt/html
  cd /opt
  #生成一个html页面
  echo '<!DOCTYPE html>
  <html lang="zh-CN">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>欢迎页面</title>
      <style>
          body {
              font-family: Arial, sans-serif;
              background-color: #f0f8ff;
              margin: 0;
              padding: 0;
          }
          header {
              background-color: #4CAF50;
              color: white;
              text-align: center;
              padding: 1em 0;
          }
          nav {
              display: flex;
              justify-content: center;
              background-color: #333;
          }
          nav a {
              color: white;
              padding: 14px 20px;
              text-decoration: none;
              text-align: center;
          }
          nav a:hover {
              background-color: #ddd;
              color: black.
          }
          main {
              padding: 20px;
          }
          section {
              margin-bottom: 20px;
          }
          footer {
              text-align: center;
              padding: 1em 0;
              background-color: #333;
              color: white.
          }
      </style>
  </head>
  <body>
      <header>
          <h1>欢迎来到我们的网站</h1>
      </header>
      <nav>
          <a href="#home">首页</a>
          <a href="#about">关于我们</a>
          <a href="#services">服务</a>
          <a href="#contact">联系我们</a>
      </nav>
      <main>
          <section id="home">
              <h2>首页</h2>
              <p>这是我们网站的主页。在这里，您可以找到我们提供的最新信息和新闻。</p>
          </section>
          <section id="about">
              <h2>关于我们</h2>
              <p>我们是一家致力于提供优质服务的公司。我们的团队由经验丰富的专业人士组成，确保为客户提供最佳的解决方案。</p>
          </section>
          <section id="services">
              <h2>服务</h2>
              <p>我们提供多种服务，包括网页设计、开发、数字营销等。请联系我们了解更多信息。</p>
          </section>
          <section id="contact">
              <h2>联系我们</h2>
              <p>如果您有任何问题或需要更多信息，请通过以下方式联系我们：</p>
              <ul>
                  <li>电子邮件: example@example.com</li>
                  <li>电话: 123-456-7890</li>
              </ul>
          </section>
      </main>
      <footer>
          <p>&copy; 2025 我们的网站. 版权所有.</p>
      </footer>
  </body>
  </html>' > ./html/index.html
  ```

- **容器启动**

  根据之前拉取的镜像nginx，启动容器，一些参数关键点：

  1.访问宿主机的9000端口，就相当于访问容器的80端口，`-p 9000:80`

  2.访问宿主机的/opt/html目录，就相当于访问容器的/usr/share/nginx/html目录` -v /opt/html:/usr/share/nginx/html:ro`

  3.给容器取个名称webserver ，`--name=webserver`

  命令如下

  ```shell
  #根据nginx镜像启动容器
  docker run -d --name=webserver -p 9000:80 -v /opt/html:/usr/share/nginx/html:ro  nginx:stable-otel
  #查看容器
  docker ps -a
  ```

  ![image-20251012181133091](local_image/image-20251012181133091.png)

  访问宿主机的 9000端口

  ![image-20251012181207057](local_image/image-20251012181207057.png)

关闭容器

```shell
#停止容器运行
docker stop webserver
#删除容器
docker rm webserver
```

### （2.3）创建容器镜像

通过Dockerfile文件来生成自己的镜像

```shell
cd /opt
tee ./Dockerfile << EOF
FROM nginx:stable-otel
COPY ./html /usr/share/nginx/html
EOF
# 通过dockerfile文件创建自定义镜像
docker build -t mynginx:v1.0 -f ./Dockerfile .
# 查看生成的自定义镜像
docker images mynginx:v1.0

```

![image-20251012182424193](local_image/image-20251012182424193.png)

运行镜像

```shell
docker run -d --name=myweb -p 9001:80 mynginx:v1.0
```

访问9001端口

![image-20251012182546701](local_image/image-20251012182546701.png)

停止容器

```shell
docker stop myweb && docker rm myweb
```

### （2.4）多容器管理

使用docker compose管理多个容器

#### 2.3.1 安装docker-compose

直接下载二进制文件安装即可，如下命令：

```shell
# 从github下载文件
curl -L https://github.com/docker/compose/releases/download/v2.12.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
#查看安装效果
docker-compose -v
```

![image-20251012182649928](local_image/image-20251012182649928.png)

#### 2.3.2 配置文件

生成一个docker-compose.yml文件，分别从镜像nginx:stable-otel和mynginx:v1.0启动容器：

```shell

mkdir -p /opt/dockercompose
cd /opt/dockercompose
tee ./docker-compose.yml << EOF
version: "2"
services:
  web1:
    image: nginx:stable-otel
    container_name: webserver
    ports:
      - "7000:80"
  web2:
    image: mynginx:v1.0
    container_name: myserver
    ports:
      - "7001:80"
EOF
```

#### 2.3.3 启动容器

根据docker-compose.yml同时启动2个容器，命令如下：

```shell
docker-compose -p webs -f ./docker-compose.yml up -d
docker ps -a
```

![image-20251012183347326](local_image/image-20251012183347326.png)

分别访问7000和7001端口

![image-20251012183403059](local_image/image-20251012183403059.png)

![image-20251012183409493](local_image/image-20251012183409493.png)



## 今日作业：

**使用docker-compose部署简单web服务**

请根据以下要求，完成需要的操作

1.安装docker和docker-compose

2.拉取nginx镜像到本地

3.使用docker-compose启动web服务

**提交内容：**请提交docker-compose运行结果截图和网站访问截图，两个截图请合并到一个PDF文件内

如下范例

![image-20251012183736292](local_image/image-20251012183736292.png)

![image-20251012183812602](local_image/image-20251012183812602.png)

