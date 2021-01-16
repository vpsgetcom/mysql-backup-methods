#!/bin/bash
source config.sh


###
echo "===Mysql backup with percona xtrabackup and upload backup to azure blob storage==="
echo "---Ensure we have empty workingdir---"
rm -rf $workingdir
mkdir $workingdir

echo "---Running percona xtrabcp with compress---"

 time sh -c \
    "xtrabackup --databases=$mysqldb --parallel=4 --compress --compress-threads=4  --backup  --user=$mysqluser --password=$mysqlpass \
               --datadir=$mysqldatadir --target-dir=$workingdir --host=$mysqlhost"

echo "---Uploading to Azure Blob---"
echo ".....adding environment vars:"
export AZURE_STORAGE_KEY=$AZURE_STORAGE_KEY
export AZURE_STORAGE_ACCOUNT=$AZURE_STORAGE_ACCOUNT

 time sh -c \
     "az storage blob upload-batch  --destination $Azure_CT_Name  --destination-path mysqlXtrabcp --source $workingdir"