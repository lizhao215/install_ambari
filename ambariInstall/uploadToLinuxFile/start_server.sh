#!/bin/bash
export ambariServerIP=$1

ssh -o stricthostkeychecking=no centos@$ambariServerIP "sudo su ; cd /home/ ; ./ambari-server-install.sh >> /home/centos/ambari_server_install.log"
