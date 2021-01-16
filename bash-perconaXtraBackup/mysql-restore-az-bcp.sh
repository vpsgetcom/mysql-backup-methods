#!/bin/bash
source config.sh
echo "===Mysql restore downloaded from az blob  percona xtrabackup and restore==="

echo "---Ensure we have empty workingdir---"
rm -rf $workingdir
mkdir $workingdir

echo ".....adding environment vars.."
export AZURE_STORAGE_KEY=$AZURE_STORAGE_KEY
export AZURE_STORAGE_ACCOUNT=$AZURE_STORAGE_ACCOUNT
echo "....donwloading backup:"

az storage blob download-batch  -s $Azure_CT_Name  -d $workingdir --pattern mysqlXtrabcp/*

echo "...Decompress backup and restore:"
xtrabackup --parralel --decompress --remove-original  --target-dir="${workingdir}/mysqlXtrabcp/" 

#copy back with xtrabackup is ok if your mysql data dir is empty ; so not our case
#xtrabackup --copy-back --target-dir="${workingdir}/mysqlXtrabcp/" --data-dir=$mysqldatadir


#copy back with rsync 
rsync -rvt --exclude 'xtrabackup_checkpoints' --exclude 'xtrabackup_logfile' \
 "${workingdir}/mysqlXtrabcp/" $mysqldatadir

echo "...fix permissions and restart mysqld service:"
chown -R mysql:mysql $mysqldatadir
systemctl restart mysqld