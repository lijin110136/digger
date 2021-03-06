#!/bin/bash
LC_ALL=C
source ~/.bashrc
logdate=$(date --date '1 days ago' '+%Y-%m-%d')
data_analysis_ip=127.0.0.1:8000
output_dir="../result/dayStats"
if [ $# -ne 0 ]; then
   logdate=$1
fi
rsync -avvP work@10.18.102.75:/home/work/local/orts/logs/raw1.log.$logdate ../logs/raw1.log.$logdate

if [ $? -ne 0 ]; then
    echo "failed to rsync log file" && exit -1
fi
if [ ! -d $output_dir ]; then
  mkdir -p $output_dir
fi

cat ../logs/raw1.log.$logdate | python digger_stat.py $logdate -o $output_dir

if [ $? -ne 0 ]; then
    echo "failed to analyze file" && exit -1
fi

#上传文件到数据分析平台
curl -F "filename=@${output_dir}/adPv_${logdate}.txt" -F "datadate=$logdate" -F "datatype=ad" ${data_analysis_ip}/digger/saveFileAsData
curl -F "filename=@${output_dir}/adGroupPv_${logdate}.txt" -F "datadate=$logdate" -F "datatype=adGroup" ${data_analysis_ip}/digger/saveFileAsData
curl -F "filename=@${output_dir}/projectPv_${logdate}.txt" -F "datadate=$logdate" -F "datatype=project" ${data_analysis_ip}/digger/saveFileAsData
curl -F "filename=@${output_dir}/productPv_${logdate}.txt" -F "datadate=$logdate" -F "datatype=product" ${data_analysis_ip}/digger/saveFileAsData
curl -F "filename=@${output_dir}/entryPv_${logdate}.txt" -F "datadate=$logdate" -F "datatype=entry" ${data_analysis_ip}/digger/saveFileAsData

if [ $? -ne 0 ]; then
    echo "failed to upload file" && exit -1
fi

