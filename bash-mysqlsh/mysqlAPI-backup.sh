#!/bin/bash
source config.sh


###
echo "===Mysql backup with mysqlsh dumpInstance  and upload backup to azure blob storage==="
echo "---Ensure we have empty workingdir---"
rm -rf $workingdir
mkdir $workingdir

echo "API backup Instance"
#mysqlsh --mysql -u $mysqluser  -h $mysqlhost -P 3306 -e  'util.dumpInstance("'$workingdir'",{ocimds: true,compatibility: ["strip_restricted_grants","force_innodb"]})'


echo "API backup $mysqldb schema separately:"
echo "---Ensure we have empty schema workingdir---"
schemasdir="${workingdir}schemas/"
rm -rf $schemasdir
mkdir $schemasdir
echo $schemasdir

mysqlsh --mysql -u $mysqluser  -h $mysqlhost -P 3306 -e  'util.dumpSchemas(["'$mysqldb'"],"'$schemasdir'",{ocimds: true,compatibility: ["strip_restricted_grants","force_innodb"]})'



echo "---Uploading backup instance  dump to Azure Blob---"
echo ".....adding environment vars:"
export AZURE_STORAGE_KEY=$AZURE_STORAGE_KEY
export AZURE_STORAGE_ACCOUNT=$AZURE_STORAGE_ACCOUNT

 time sh -c \
     "az storage blob upload-batch  --destination $Azure_CT_Name  --destination-path mysqlAPIbackup --source $workingdir"
