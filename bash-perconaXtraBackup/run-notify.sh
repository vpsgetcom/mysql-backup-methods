#!/bin/bash
source config.sh

#run main script, collect logs and send email with notification

echo "running...."

nohup mysql-az-xtrabcp.sh 2> backuplog.txt 

echo "sending email ..."
echo -e "Subject: Backup Details\n\nLog Attached"| (cat - && uuencode backuplog.txt backuplog.txt) | \
       (cat - && uuencode nohup.out azCt.txt)  | ssmtp $EmailTo -f $EmailFrom -F "MySQLxtraBackup"