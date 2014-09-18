#!/bin/bash
LC_ALL=C
source ~/.bashrc
logdate=$(date --date '1 days ago' '+%Y-%m-%d')
if [ $# -ne 0 ]; then
   logdate=$1
fi
rsync -avvP work@10.18.102.75:/home/work/local/orts/logs/raw1.log.$logdate ../logs/raw1.log.$logdate.log
if [ $? -ne 0 ]; then
    echo "failed to rsync log file" && exit -1
fi

grep ../logs/raw1.log.$logdate.log | python ad_install.py $logdate
