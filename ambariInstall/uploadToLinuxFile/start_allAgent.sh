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

scp  -o stricthostkeychecking=no  /home/centos/hosts.txt centos@$ip:/home/centos/
scp  -o stricthostkeychecking=no  /home/centos/hdp.repo centos@$ip:/home/centos/
scp  -o stricthostkeychecking=no  /home/centos/ambari.repo centos@$ip:/home/centos/

ssh -o stricthostkeychecking=no centos@$ip "sudo su ; cd /home; ./setHost_startAgent.sh $ambariServerIP >> /home/centos/ambari_agent_install.log"

done < /home/centos/hosts.txt

