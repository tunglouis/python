#!/bin/bash
sudo apt-get update
sudo apt-get build-dep nginx -y
sudo apt-get install libpcre3 libpcre3-dev
wget https://firmware.vp9.vn/release/relay_server/nginx-1.10.3.tar.gz -O /home/sysadmin/nginx-1.10.3.tar.gz
chown -R sysadmin:sysadmin nginx-1.10.3.tar*
tar xfz nginx-1.10.3.tar.gz
chown -R sysadmin:sysadmin nginx-1.10.3
cd nginx-1.10.3
./configure --prefix=/home/sysadmin/nginx  --with-http_ssl_module --with-ipv6 --http-proxy-temp-path=/dev/shm/nginx_proxy_temp --http-client-body-temp-path=/dev/shm/nginx_client_body_temp --http-fastcgi-temp-path=/dev/shm/nginx_fastcgi_temp --http-uwsgi-temp-path=/dev/shm/nginx_uwsgi_temp --http-scgi-temp-path=/dev/shm/nginx_scgi_temp
make && make install
sudo /home/sysadmin/nginx/sbin/nginx
