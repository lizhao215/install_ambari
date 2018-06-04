#!/bin/bash

#sudo su  最好切换至root 用户再执行脚本
#ssh -o stricthostkeychecking=no node2  ssh 免 输入yes
## 获取本机 ip
#
#
export ambariServerIP=$1


while read line
do  
#echo $line
ip=`echo $line | awk '{print $1}'`
host=`echo $line | awk '{print $2}'`
echo "ip: " $ip "host:" $host

scp  -o stricthostkeychecking=no  -pr   /home/centos/hosts.txt  root@$ip:/home/centos/
scp  -o stricthostkeychecking=no   -pr  /home/centos/hdp.repo   root@$ip:/home/centos/
scp  -o stricthostkeychecking=no   -pr  /home/centos/ambari.repo root@$ip:/home/centos/

ssh -o stricthostkeychecking=no root@$ip "cd /home; ./setHost_startAgent.sh $ambariServerIP >> /home/centos/ambari_agent_install.log"

done < /home/centos/hosts.txt

