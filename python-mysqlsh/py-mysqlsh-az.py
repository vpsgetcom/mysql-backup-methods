import os
import time
import json
from pySendEmail import pySendEmail
import logging
import shutil
import tempfile


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

localDumpFile = mysqldb + "-mysqldump.sql.gz"
#localDumpFolder = tempfile.gettempdir() +  slash + mysqldb + "-utilDump" + slash
#localDumpFolder = mysqldb + "__utilDump"
workingDir =jsonVars["workingdir"]
localDumpFileSchema = mysqldb + "-mysqldump_schema_only.sql.gz"
os.environ["AZURE_STORAGE_KEY"] = jsonVars["Azure"]["STORAGE_KEY"]
os.environ["AZURE_STORAGE_ACCOUNT"] = jsonVars["Azure"]["STORAGE_ACCOUNT"]

logname = "py-mysqsh_util.dump_instance.log"

def backup_db():

    logging.info("Backing up DB | mysqhsl>dumpInstance()| : " + mysqldb + " in script dir: " + os.getcwd() + " running cmd: ")

    # the util.instance_ dump w/o additional compability params
    #runcmd = "mysqlsh --py --mysql -u " + mysqluser + " -h " + mysqlhost + " --database=" + mysqldb+ \
    #         " -P 3306 " + "--password=" +mysqlpass +  " -e " + "util.dump_instance('" + workingDir + "')"

    #seems like this working better with non-InnoDB:_
    runcmd = "mysqlsh --py --mysql -u " + mysqluser + " -h " + mysqlhost + " --database=" + mysqldb + \
             " -P 3306 " + "--password=" + mysqlpass + " -e \"" + "util.dump_instance('" + \
             workingDir +"', {'ocimds': 'true', 'compatibility': ['strip_restricted_grants','force_innodb']})"  \
             +"\" "

    print (runcmd)
    logging.info (runcmd.replace(mysqlpass, "*******")) #hide pass from logging

    try:
        retval = os.system(runcmd)
    except:
        logging.error("EXCEPTION!" + retval)

def backup_db_schema():


    logging.info("Backing up DB SCHEMA: " + mysqldb + " in script dir: " + os.getcwd() + " running cmd: ")
    #on error try to add  --column-statistics=0 ; may be useful with some restrincted DBs, like if you using mysql on cpanel sharing hosting
    runcmd = 'mysqldump  --compress --single-transaction --quick  --no-tablespaces --no-data --user="' \
             + mysqluser + '"' + ' --password="'  + mysqlpass + '"' + ' -h ' + mysqlhost + ' ' + mysqldb + \
             '| pigz > ' + os.getcwd() + slash + localDumpFileSchema
    logging.info (runcmd.replace(mysqlpass, "*******"))
    try:
        retval = os.system(runcmd)
    except:
        logging.error("EXCEPTION!" + retval)

def azure_upload(azCtName, data, type):

    if type == "file":
        filePath = os.getcwd() + slash + data
        runcmd = 'az storage blob upload  -f ' + filePath + ' --container-name ' + azCtName  + ' --name ' + data
        logging.info(runcmd)
        try:
            retval = os.system(runcmd)
        except:
            logging.error("EXCEPTION!" + retval)
    elif type == "dir":
        runcmd = 'az storage blob upload-batch --destination ' + azCtName + ' --destination-path py-mysqlShDumpInstance --source ' + data
        print (runcmd)
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

    if os.path.exists(workingDir) and os.path.isdir(workingDir):
        shutil.rmtree(workingDir)
    os.mkdir(workingDir)


    logger = logging.getLogger('ndi python mysqhsl>dumpInstance() example')
    start_time = time.time()
    logging.info ("---BACKUP MYSQL db  with mysqhsl>dumpInstance()  and scheme with usual mysqldump ; pull backup  to az storage [using: python , mysqlsh, mysqldump, az cli] ---")

    backup_time = time.time()
    backup_db()
    backup_db_schema()
    backup_time_total = time.time() - backup_time


    #upload db dump and schema:
    upload_time = time.time()
    azure_upload(jsonVars["Azure"]["CT_Name"], workingDir, "dir")
    azure_upload(jsonVars["Azure"]["CT_Name"], localDumpFileSchema, "file")

    logging.info("Upload time : %s seconds " % (time.time() - upload_time))
    logging.info("Backup time : " + str(backup_time_total) + "seconds")

    logging.info("---- TOTAL EXEC TIME: %s seconds -----" % (time.time() - start_time))
    print ("---- TOTAL EXEC TIME: %s seconds -----" % (time.time() - start_time))
    body = "Bacup log attached"
    pySendEmail(jsonVars["Smtp"]["Server"], jsonVars["Smtp"]["Port"], jsonVars["Smtp"]["Subject"], body, \
                 jsonVars["Smtp"]["SenderAddress"], jsonVars["Smtp"]["ToAddress"], jsonVars["Smtp"]["Password"], \
                 logname)