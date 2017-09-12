#爆破
http-basic

# 中间件

> shiro

> struts

> weblogic

> jboss

> jenkins

> tomcat   后台弱口令

# 系统

> elasticsearch

> supervisord



# CMS
> wordpress   指纹识别 + 爆破

> discuz      指纹识别 + SSRF

> redmine未授权

#信息泄露
> 域传送

> 443证书


===============================
指纹识别,github上的项目
> https://github.com/CL-Shang/whatweb-plugins-new/tree/master/my-plugins

----------------------
postmessage 跨域自动检测
https://github.com/lcatro/cross_domain_postmessage_vuln_dig

===========================
目录爆破

> https://github.com/OJ/gobuster

> https://github.com/lijiejie/BBScan
> 同一类型的目录泄露应该不超过两个,比如不可能同时出现www.tar.gz和www.zip
> 所有的敏感文件加起来应该也不会超过10个


> nginx空白页,用五位字符字典爆破. 待测试爆破时间

> # 查看服务

> select service,count(service) from scan_scan_port group by service order by count(service);

> # 非常用端口的web服务

> select comment,port from scan_scan_port where service="http" and port!="80" and port!="443" and port!="8080";

