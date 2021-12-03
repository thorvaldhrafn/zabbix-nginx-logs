# zabbix-nginx-logs

### On host

_Nginx logs monitoring for zabbix_

Download full project to server

`git clone https://github.com/thorvaldhrafn/zabbix-nginx-logs.git`

Make subdirectory for scripts (if not exists) and copy script

`mkdir /etc/zabbix/scripts/ && cp zabbix-nginx-logs/scripts/nginx_acc_logs.py
`

Set permissions for script

`chown zabbix /etc/zabbix/scripts/nginx_acc_logs.py && chmod +x /etc/zabbix/scripts/nginx_acc_logs.py`

Add script to nginx conf

`echo 'UserParameter=nginx.logs.access,/etc/zabbix/scripts/nginx_acc_logs.py' >> /etc/zabbix/zabbix_agentd.conf`

Install the necessary python libraries

`pip3 install crossplane dnspython`

Restart zabbix agent

`systemctl restart zabbix-agent`

### In zabbix web-interface

Go to _Configuration > Templates_ 

Import template file _zabbix-nginx-logs.json_

Apply template **"Template nginx logs monitoring"** to your host 