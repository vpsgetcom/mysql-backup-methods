#!/bin/bash
source config.sh
echo "===Mysql restore downloaded from az blob API-made backup and restore==="

echo "---Ensure we have empty workingdir---"
#rm -rf $workingdir
#mkdir $workingdir

echo ".....adding environment vars.."
export AZURE_STORAGE_KEY=$AZURE_STORAGE_KEY
export AZURE_STORAGE_ACCOUNT=$AZURE_STORAGE_ACCOUNT
echo "....donwloading backup:"

#az storage blob download-batch  -s $Azure_CT_Name  -d $workingdir --pattern mysqlXtrabcp/*

echo "...Decompress backup and restore:"


echo "...Just testing (remove dryRun in order to really restore the bcp)"

#set global local_infile=ON; once better manually check this 
#mysql --user=$mysqluser --password=$mysqlpass -e 'set global local_infile=ON;'

mysqlsh --mysql -u $mysqluser -h $mysqlhost -P 3306 -e 'util.loadDump("'$workingdir'", {ignoreExistingObjects: true, threads: 8, dryRun: true})'
