import os
import time
import json

#remove dryRun  in  order to make real restore.

json_file = open("config.json")
jsonVars = json.load(json_file)
json_file.close()

print(jsonVars)


mysqluser=jsonVars["Mysql"]["user"]
mysqlhost=jsonVars["Mysql"]["host"]
mysqlpass=jsonVars["Mysql"]["pass"]
mysqldb=jsonVars["Mysql"]["db"]
workingDir =jsonVars["workingdir"]

#uncomment one line with slash for your OS
slash = jsonVars["slash"]
#slash = "//" #linux


azDumpFile = mysqldb + "-mysqldump.sql"
azDumpFileSchema = mysqldb + "-mysqldump_schema_only.sql"
os.environ["AZURE_STORAGE_KEY"] = jsonVars["Azure"]["STORAGE_KEY"]
os.environ["AZURE_STORAGE_ACCOUNT"] = jsonVars["Azure"]["STORAGE_ACCOUNT"]


def azure_download(azCtName, filePath):
    #runcmd = 'az storage blob download -f ' + filePath + ' --container-name ' + azCtName + ' --name ' + sqlDumpFile
    runcmd = 'az storage blob download -f ' + filePath + ' --container-name ' + azCtName + ' --name ' + azDumpFile
    print(runcmd)
    try:
        retval = os.system(runcmd)
    except:
        print("EXCEPTION!" + retval)

def restore_db():
    print("Restoring DB   [DRY RUN, IgnoreExisting Objects]: " + mysqldb + " in script dir: " + os.getcwd() + " running cmd: ")
    #runcmd = 'mysql  --user="' + mysqluser +'"' + ' --password="' + mysqlpass + '"' + ' -h ' + mysqlhost + \
    #         ' ' + mysqldb + ' < ' + os.getcwd() + slash + azDumpFile

    runcmd = "mysqlsh --py --mysql -u " + mysqluser + " -h " + mysqlhost + " --database=" + mysqldb + \
             " -P 3306 " + "--password=" + mysqlpass + " -e \"" + "util.load_dump('" + \
             workingDir + "', {'ignoreExistingObjects': 'true', 'dryRun': 'true'})" \
             + "\" "
    print (runcmd)
    try:
        retval = os.system(runcmd)
    except:
        print("EXCEPTION!" + retval)


if __name__ == '__main__':
    print("download from azure  and restore dump... ")
    filePath = os.getcwd() + slash + azDumpFile
    azure_download(jsonVars["Azure"]["CT_Name"], filePath)
    restore_db()
