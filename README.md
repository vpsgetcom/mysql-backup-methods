**I'll show the examples of doing mysql backup  based on  mysql-sh, percona xtrabackup and mysqldump.**

There also exists mysqbackup utility from mysql official but it's possible to use it only for Oracle Enterprice license so I'm unable to compare mysqlbackup utulity speed at this point.


You may find the time metrics based on 950MB database hosted on 4 cpu , 4GB RAM Virtual Test server with pure ssd storage in file 
```
time-metrics-tests.txt 
```

In short: mysqldump operate in a single thread and for a big databases in production  better go with mysql-sh util or percona xtrabackup  - both able to multithread and compress out of the box. (physical backup techs vs logical mysqldump)

The suggested way is mysql-sh using util.dump_instance() method.
But the percona xtrabackup is little bit faster. SO if you have 1TB GB DB I suggest you to give a try with percona xtrabackup.
Brief compare (run on mysql server): 

```
mysqlsh  util.dumpInstance  : 11.248s
percona xtrabackup          : 7.108s
mysqldump +pigz             : 24.483s
```

//The execution time differ will increase exponentially (I assume so) with increasing DB size as well as we'll use more powerful sql server/cluster for a huge DB with more cpus threads, ram, IO subsystem speed 


Definitely I also  suggest to run scripts on the exact mysql server instance as this will speedup backup process for sure. (no NW  data transfer). However you may use any script locally and backup remote DB.

I do not imlementing the SSH tunneling  as all we know how to do it and we have rather differ focus here.


The python scripts may run on Windows or Linux. The bash script you should run on Linux. (windows linux subsystem should be also ok but I did not tested it)



***So here is the depencies example install on Centos7 OS for all methods***


```
yum update
yum install epel-release nano git pigz
```

Install mysql (we need mysqldump)

```
rpm -Uvh https://repo.mysql.com/mysql80-community-release-el7-3.noarch.rpm
sed -i 's/enabled=1/enabled=0/' /etc/yum.repos.d/mysql-community.repo
yum --enablerepo=mysql80-community install mysql
```

Install mysql-sh
```
yum --enablerepo=mysql-tools-community install mysql-shell
```


Install Azure CLI

```
rpm --import https://packages.microsoft.com/keys/microsoft.asc

echo -e "[azure-cli]
name=Azure CLI
baseurl=https://packages.microsoft.com/yumrepos/azure-cli
enabled=1
gpgcheck=1
gpgkey=https://packages.microsoft.com/keys/microsoft.asc" | sudo tee /etc/yum.repos.d/azure-cli.repo


yum install azure-cli
```

Login to AZ CLL: 
```
az login    #procced with login
```

**Running python scripts**
from **<python-mysqlsh>** dir
 
Remember to set your config in config.json and tun script after:

python3 py-mysqlsh-az.py


**Running bash scripts ** 

from <bash-*> dir
In order to use mysql-sh bash script solution you  need to install the  depencies related to the proper mailsend: 

yum install epel-release
yum install ssmtp
yum install sharutils ##for uuencode used to encode attachement

Set  your config in config.sh and set your email settings in /etc/ssmtp/ssmtp.conf . My example of lines to change in ssmtp.conf provided (for my own mail server).
I suggest to run bash scripts on the exact mysql server instance so in this way you may do not store the password in config or anywhere.
The bash script  provided  w/o specifying  --password=$mysqlpass  in mysqlsh argument list, feel free to add it and also set password in config.sh

Esure you set exec attribute on *.sh files, provided config in config.sh , ssmtp.conf and run:

./run-notify.sh 


**Percona XtraBackup**

For percona xtrabackup you need to install percona xtrabackup util. The util version depend on your mysql server version.
Refer to the officvial docs : 
https://www.percona.com/doc/percona-xtrabackup

For my test I've used the next: 
https://www.percona.com/doc/percona-xtrabackup/2.4/installation/yum_repo.htm

Please note that percona xtrabackup do not support mariadb









 




