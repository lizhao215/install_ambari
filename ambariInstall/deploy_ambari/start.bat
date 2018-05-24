@echo off 
set masterIP=%1
set currentPath=%~dp0
cd  %currentPath%
echo currentPath: %cd%

set pscpTool=%currentPath%\linuxConnTools\pscp.exe
set plinkTool=%currentPath%\linuxConnTools\plink.exe


rem  检查 master 机器环境安装情况
rem  pip install --upgrade pip 
rem  pip install --upgrade ansible
rem 检查 yum 是否安装

echo y |  %plinkTool% -l root -pw "root"  %masterIP%  "yum --version"
echo y |  %plinkTool% -l root -pw "root"  %masterIP%  "python --version"
echo y |  %plinkTool% -l root -pw "root"  %masterIP%  "java -version"
echo y |  %plinkTool% -l root -pw "root"  %masterIP%  "source /etc/profile ; echo $JAVA_HOME"
echo y |  %plinkTool% -l root -pw "root"  %masterIP%  "pip --version"
echo y |  %plinkTool% -l root -pw "root"  %masterIP%  "ansible --version"

rem 升级 pip ansible 版本
rem call  plinkTool -l root -pw "root"  %masterIP%  "yum install ansible"
rem echo y |  %plinkTool% -l root -pw "root"  %masterIP%  "pip install --upgrade pip"
echo y |  %plinkTool% -l root -pw "root"  %masterIP%  "pip install --upgrade ansible"

rem 安装 httpd 服务
rem 判断 httpd 服务是否安装
echo y |  %plinkTool% -l root -pw "root"  %masterIP%  "which httpd"
rem 判断 80端口是否占用
echo y |  %plinkTool% -l root -pw "root"  %masterIP%  "lsof -i:80"
echo y |  %plinkTool% -l root -pw "root"  %masterIP%  "yum -y install httpd"

echo y |  %plinkTool% -l root -pw "root"  %masterIP%  "yum -y install yum-utils"
echo y |  %plinkTool% -l root -pw "root"  %masterIP%  "yum -y install createrepo"
rem 允许 http 服务通过防火墙
echo y |  %plinkTool% -l root -pw "root"  %masterIP%  "firewall-cmd --add-service=http"
echo y |  %plinkTool% -l root -pw "root"  %masterIP%  "firewall-cmd --permanent --add-service=http"
rem 添加Apache 服务到系统层使其随系统自动启动。
echo y |  %plinkTool% -l root -pw "root"  %masterIP%  "systemctl start httpd.service"
echo y |  %plinkTool% -l root -pw "root"  %masterIP%  "systemctl enable httpd.service"

rem 复制ambari 和 HDP 和 HDP utils 文件至 master 机器 
rem pscp  -l username -pw password -r 复制子文件夹  src 本地路径  dest 目标路径

echo y |  %plinkTool% -l root -pw "root"  %masterIP%  "mkdir -pr /var/www/html/ambari"
echo y |  %plinkTool% -l root -pw "root"  %masterIP%  "mkdir -pr /var/www/html/hdp/HDP-UTILS"
echo y |  %plinkTool% -l root -pw "root"  %masterIP%  "mkdir -pr /home/tmp"
echo y |   %pscpTool% -l root -pw "root"  %currentPath%\uploadToLinuxFile\ambari*.tar.gz %masterIP%:/home/tmp
echo y |   %pscpTool% -l root -pw "root"  %currentPath%\uploadToLinuxFile\HDP*.tar.gz %masterIP%:/home/tmp
echo y |  %plinkTool% -l root -pw "root"  %masterIP%  "tar -zxvf /home/tmp/ambari*.tar.gz -C /var/www/html/ambari/"
echo y |  %plinkTool% -l root -pw "root"  %masterIP%  "tar -zxvf /home/tmp/HDP-2*.tar.gz -C /var/www/html/hdp/"
echo y |  %plinkTool% -l root -pw "root"  %masterIP%  "tar -zxvf /home/tmp/HDP-U*.tar.gz -C /var/www/html/hdp/HDP-UTILS/"

rem  配置 ambari.repo 和 hdp.repo
rem  自动更改 repo 的 url 中 的 ip
rem  %ambariVersion%  %HDPVersion%  %HDPUtilVersion%
rem 自动更改repo 文件中的版本号

echo y |   %pscpTool% -l root -pw "root"  %currentPath%\uploadToLinuxFile\HDP.repo %masterIP%:/etc/yum.repos.d/
echo y |   %pscpTool% -l root -pw "root"  %currentPath%\uploadToLinuxFile\ambari.repo %masterIP%:/etc/yum.repos.d/
rem 判断 HDP.repo 和 ambari.repo 正确性


rem 判断ambari yum 源是否正确
echo y |  %plinkTool% -l root -pw "root"  %masterIP%  "yum list | grep ambari"
echo y |  %plinkTool% -l root -pw "root"  %masterIP%  "yum list | grep HDP"

rem ansible 命令
rem ansible 执行远程脚本
rem 免秘钥
rem 映射hosts
rem 关闭防火墙 selinux , THP
rem 安装jdk等 配置环境变量 
rem 安装 ambari
rem 自动配置 ambari
rem 启动ambari 服务
  Installing : keyutils-libs-devel-1.5.8-3.el7.x86_64              1/16 
  Installing : libcom_err-devel-1.42.9-11.el7.x86_64               2/16 
  Installing : 2:vim-filesystem-7.4.160-4.el7.x86_64               3/16 
  Installing : 2:vim-common-7.4.160-4.el7.x86_64                   4/16 
  Installing : gpm-libs-1.20.7-5.el7.x86_64                        5/16 
  Installing : libsepol-devel-2.5-8.1.el7.x86_64                   6/16 
  Installing : libkadm5-1.15.1-19.el7.x86_64                       7/16 
  Installing : pcre-devel-8.32-17.el7.x86_64                       8/16 
  Installing : libselinux-devel-2.5-12.el7.x86_64                  9/16 
  Installing : libverto-devel-0.2.5-4.el7.x86_64                  10/16 
  Installing : krb5-devel-1.15.1-19.el7.x86_64                    11/16 
  Installing : zlib-devel-1.2.7-17.el7.x86_64                     12/16 
  Installing : 1:openssl-devel-1.0.2k-12.el7.x86_64               13/16 
  Installing : 2:vim-enhanced-7.4.160-4.el7.x86_64                14/16 
  Installing : unzip-6.0-19.el7.x86_64                            15/16 
  Installing : wget-1.14-15.el7_4.1.x86_64

  Installing : postgresql-libs-9.2.23-3.el7_4.x86_64                1/4 
  Installing : postgresql-9.2.23-3.el7_4.x86_64                     2/4 
  Installing : postgresql-server-9.2.23-3.el7_4.x86_64   
(1/17): autoconf-2.69-11.el7.noarch.rpm                              | 701 kB  00:00:00     
(2/17): gdbm-devel-1.10-8.el7.x86_64.rpm                             |  47 kB  00:00:00     
(3/17): glibc-devel-2.17-222.el7.x86_64.rpm                          | 1.1 MB  00:00:00     
(4/17): glibc-headers-2.17-222.el7.x86_64.rpm                        | 678 kB  00:00:00     
(5/17): libaio-0.3.109-13.el7.x86_64.rpm                             |  24 kB  00:00:00     
(6/17): libdb-devel-5.3.21-24.el7.x86_64.rpm                         |  38 kB  00:00:00     
(7/17): perl-Data-Dumper-2.145-3.el7.x86_64.rpm                      |  47 kB  00:00:00     
(8/17): perl-ExtUtils-Install-1.58-292.el7.noarch.rpm                |  74 kB  00:00:00     
(9/17): perl-ExtUtils-MakeMaker-6.68-3.el7.noarch.rpm                | 275 kB  00:00:00     
(10/17): perl-ExtUtils-Manifest-1.61-244.el7.noarch.rpm              |  31 kB  00:00:00     
(11/17): perl-ExtUtils-ParseXS-3.18-3.el7.noarch.rpm                 |  77 kB  00:00:00     
(12/17): perl-Test-Harness-3.28-3.el7.noarch.rpm                     | 302 kB  00:00:00     
(13/17): m4-1.4.16-10.el7.x86_64.rpm                                 | 256 kB  00:00:00     
(14/17): perl-devel-5.16.3-292.el7.x86_64.rpm                        | 453 kB  00:00:00     
(15/17): pyparsing-1.5.6-9.el7.noarch.rpm                            |  94 kB  00:00:00     
(16/17): systemtap-sdt-devel-3.2-4.el7.x86_64.rpm                    |  72 kB  00:00:00     
(17/17): kernel-headers-3.10.0-862.2.3.el7.x86_64.rpm  
  Installing : mysql-community-common-5.7.22-1.el7.x86_64         1/6 
  Installing : mysql-community-libs-5.7.22-1.el7.x86_64           2/6 
  Installing : mysql-community-client-5.7.22-1.el7.x86_64         3/6 
  Installing : mysql-community-server-5.7.22-1.el7.x86_64         4/6 
  Installing : mysql-community-libs-compat-5.7.22-1.el7.x86_64  
  
  
  Installing : apr-1.4.8-3.el7_4.1.x86_64                                                                 1/6 
  Installing : apr-util-1.5.2-6.el7.x86_64                                                                2/6 
  Installing : httpd-tools-2.4.6-80.el7.centos.x86_64                                                     3/6 
  Installing : centos-logos-70.0.6-3.el7.centos.noarch                                                    4/6 
  Installing : mailcap-2.1.41-2.el7.noarch                                                                5/6 
  Installing : httpd-2.4.6-80.el7.centos.x86_64   
  
  
ntp ntpdate
