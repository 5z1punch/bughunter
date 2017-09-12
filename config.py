#coding:utf-8
#数据库配置
redis_server = "127.0.0.1"
redis_port = 6379
redis_password = "1"
redis_nmap_dbname ="nmap"
redis_dbname ="servicescan"
delimit_sign = "|"
mysql_server = "127.0.0.1"
mysql_port = 3306
mysql_user = "fscan"
mysql_pass = "fscan123"
mysql_db = "blog"
global_options = '-n -sT -P0 -sV -O --script=banner -p T:21-25,80-89,110,143,443,513,873,1080,1433,1521,1158,3306-3308,3389,3690,4848,5900,6379,7001,8000-9001,9418,27017-27019,50060,111,11211,2049,1099,1090,9200,2375,3128,6081,3500,53,5555,9230'
