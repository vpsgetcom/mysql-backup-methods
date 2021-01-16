import os
import time
import json
from pySendEmail import pySendEmail
import logging

#read input variables from JSON
json_file = open("config.json")
jsonVars = json.load(json_file)
json_file.close()

print(jsonVars)


mysqluser=jsonVars["Mysql"]["user"]
mysqlhost=jsonVars["Mysql"]["host"]
mysqlpass=jsonVars["Mysql"]["pass"]
mysqldb=jsonVars["Mysql"]["db"]

#uncomment one line with slash for your OS
slash = jsonVars["slash"]
#slash = "//" #linux
#slash = "\\" #windows

localDumpFile = mysqldb + "-mysqldump.sql.gz"
localDumpFileSchema = mysqldb + "-mysqldump_schema_only.sql.gz"
os.environ["AZURE_STORAGE_KEY"] = jsonVars["Azure"]["STORAGE_KEY"]
os.environ["AZURE_STORAGE_ACCOUNT"] = jsonVars["Azure"]["STORAGE_ACCOUNT"]

logname = "pymysqldump.log"

def backup_db():

    logging.info("Backing up DB: " + mysqldb + " in script dir: " + os.getcwd() + " running cmd: ")
    #for mysqldump used on my test windows I  need to add --column-statistics=0   ; and if our DB hosted with some cPanel add:  --no-tablespaces
    #--opt || --compress --single-transaction --quick
    # --max-allowed-packet=1GB
    runcmd = 'mysqldump   --compress --single-transaction --quick   --skip-lock-tables  --column-statistics=0 --no-tablespaces --user="' + mysqluser +'"' + ' --password="' \
             + mysqlpass + '"' + ' -h ' + mysqlhost + ' ' + mysqldb + '| pigz > ' + os.getcwd() + slash + localDumpFile
    logging.info (runcmd.replace(mysqlpass, "*******")) #hide pass from logging

    try:
        retval = os.system(runcmd)
    except:
        logging.error("EXCEPTION!" + retval)

def backup_db_schema():

    logging.info("Backing up DB SCHEMA: " + mysqldb + " in script dir: " + os.getcwd() + " running cmd: ")
    runcmd = 'mysqldump  --compress --single-transaction --quick  --column-statistics=0 --no-tablespaces --no-data --user="' + mysqluser + '"' + ' --password="' \
             + mysqlpass + '"' + ' -h ' + mysqlhost + ' ' + mysqldb + '| pigz > ' + os.getcwd() + slash + localDumpFileSchema
    logging.info (runcmd.replace(mysqlpass, "*******"))
    try:
        retval = os.system(runcmd)
    except:
        logging.error("EXCEPTION!" + retval)

def azure_upload(azCtName, dumpFile):

    filePath = os.getcwd() + slash + dumpFile
    runcmd = 'az storage blob upload  -f ' + filePath + ' --container-name ' + azCtName  + ' --name ' + dumpFile
    logging.info(runcmd)
    try:
        retval = os.system(runcmd)
    except:
        logging.error("EXCEPTION!" + retval)



if __name__ == '__main__':
    logging.basicConfig(filename=logname,
                        filemode='w',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)



    logger = logging.getLogger('ndi python mysqldump example')
    start_time = time.time()
    logging.info ("---mysqldump db and scheme and put to az storage using python , mysqldump, az cli---")

    backup_time = time.time()
    backup_db()
    backup_db_schema()
    backup_time_total = time.time() - backup_time


    #upload db dump and schema:
    upload_time = time.time()
    azure_upload(jsonVars["Azure"]["CT_Name"], localDumpFile)
    azure_upload(jsonVars["Azure"]["CT_Name"], localDumpFileSchema)

    logging.info("Upload time : %s seconds " % (time.time() - upload_time))
    logging.info("Backup time : " + str(backup_time_total) + "seconds")

    logging.info("---- TOTAL EXEC TIME: %s seconds -----" % (time.time() - start_time))
    body = "Bacup log attached"
    pySendEmail(jsonVars["Smtp"]["Server"], jsonVars["Smtp"]["Port"], jsonVars["Smtp"]["Subject"], body, \
                jsonVars["Smtp"]["SenderAddress"], jsonVars["Smtp"]["ToAddress"], jsonVars["Smtp"]["Password"], \
                logname)