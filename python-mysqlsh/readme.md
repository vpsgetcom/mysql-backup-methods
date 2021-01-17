install depencies: 

```
mysqlsh 
mysqldump (we are using it here only for schema bcp)
az cli (remember to login with az login first)
```

fill your data in config.json

note the slahes for win and linux config... we are using 2layer cli dive to provide the path in var 

for backup run:

```
python py-mysqlsh-az.py
```

for test restore (remove dry run param for real restore)






