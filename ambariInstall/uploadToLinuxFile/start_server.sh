#!/bin/bash
export ambariServerIP=$1

ssh -o stricthostkeychecking=no root@$ambariServerIP "cd /home/ ; ./ambari-server-install.sh"
