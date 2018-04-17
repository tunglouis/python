import os
import sys
import subprocess
from subprocess import call

class env():
    def main():
        os.system('sudo adduser namnd')
        with open("/etc/ufw/user.rules", "r+") as file:
            line_fw = any("-A ufw-user-input -p tcp --dport 443 -j ACCEPT" in line for line in file)
            if not line_fw:
                file.seek(0, os.SEEK_END)
                file.write("-A ufw-user-input -p tcp --dport 443 -j ACCEPT\n")
                file.close
        with open("/etc/sudoers", "r+") as file:
            line_sudoers = any('''
# See sudoers(5) for more information on "#include" directives:
%namnd ALL=(ALL:ALL) NOPASSWD:ALL
                ''' in line for line in file)
            if not line_fw:
                file.seek(0, os.SEEK_END)
                file.write('''
# See sudoers(5) for more information on "#include" directives:
%namnd ALL=(ALL:ALL) NOPASSWD:ALL\n
                    ''')
                file.close
    if __name__ == '__main__':
            main()

class nginx():
    def main():
        with open("/etc/apt/sources.list", "r+") as file:
            sources_list = any('''
deb http://mirror.vp9.tv/ubuntu/ xenial main restricted universe multiverse
deb http://mirror.vp9.tv/ffmpeg/ xenial main
deb http://mirror.vp9.tv/ubuntu/ xenial-security main restricted universe multiverse
deb http://mirror.vp9.tv/ubuntu/ xenial-updates main restricted universe multiverse
deb-src http://mirror.vp9.tv/ubuntu/ xenial main restricted universe multiverse
deb-src http://mirror.vp9.tv/ffmpeg/ xenial main
deb-src http://mirror.vp9.tv/ubuntu/ xenial-security main restricted universe multiverse
deb-src http://mirror.vp9.tv/ubuntu/ xenial-updates main restricted universe multiverse
deb http://mirror.vp9.tv/ubuntu/ xenial-proposed main restricted universe multiverse
deb http://mirror.vp9.tv/ubuntu/ xenial-backports main restricted universe multiverse
                ''' in line for line in file)
            if not sources_list:
                file.seek(0, os.SEEK_END)
                file.write('''
deb http://mirror.vp9.tv/ubuntu/ xenial main restricted universe multiverse
deb http://mirror.vp9.tv/ffmpeg/ xenial main
deb http://mirror.vp9.tv/ubuntu/ xenial-security main restricted universe multiverse
deb http://mirror.vp9.tv/ubuntu/ xenial-updates main restricted universe multiverse
deb-src http://mirror.vp9.tv/ubuntu/ xenial main restricted universe multiverse
deb-src http://mirror.vp9.tv/ffmpeg/ xenial main
deb-src http://mirror.vp9.tv/ubuntu/ xenial-security main restricted universe multiverse
deb-src http://mirror.vp9.tv/ubuntu/ xenial-updates main restricted universe multiverse
deb http://mirror.vp9.tv/ubuntu/ xenial-proposed main restricted universe multiverse
deb http://mirror.vp9.tv/ubuntu/ xenial-backports main restricted universe multiverse\n
            ''')
        file.close

    if __name__ == '__main__':
        main()

os.system('sudo apt update')
os.system('chmod +x nginx.sh')
call(['bash', 'nginx.sh'])

domain = raw_input("Enter a domain here: ")

os.system('wget https://firmware.vp9.vn/release/relay_server/certbot-auto -O /home/sysadmin/certbot-auto')
os.system('chmod a+x /home/sysadmin/certbot-auto')
os.system('/home/sysadmin/certbot-auto certonly --standalone -d %s' % domain)

class cdn():

    def createFolder(directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print ('Error: Creating directory. ' +  directory)
            
    # Create folder sites
    createFolder('/home/sysadmin/nginx/conf/sites')

    def main():
        file = open("/home/sysadmin/nginx/nginx.conf", "w+")
        file.write('''
            user  sysadmin;
            worker_processes  16;

            error_log  logs/error.log;
            #error_log  logs/error.log  notice;
            #error_log  logs/error.log  info;

            #pid        logs/nginx.pid;


            events {
                worker_connections  1024;
            }


            http {
                include       mime.types;
                default_type  application/octet-stream;

                log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                                  '$status $body_bytes_sent "$http_referer" '
                                  '"$http_user_agent" "$http_x_forwarded_for"';

                #access_log  logs/access.log  main;
                access_log off;
                sendfile        on;
                #tcp_nopush     on;

                #keepalive_timeout  0;
                keepalive_timeout  900;
                server_tokens off;
                gzip on;
                gzip_disable "msie6";
                client_max_body_size 200M;
                map $http_upgrade $connection_upgrade {
                            default upgrade;
                            '' close;
                }
            #    server {
            #       listen 443;
            #       listen 80;
            #       server_name _;
            #       return 301 https://$host:443$request_uri;
            #    }
                include /home/sysadmin/nginx/conf/sites/*.conf;
            }
            ''')
        file.close

        file = open("/home/sysadmin/nginx/conf/sites/%s.conf" % domain, "w+")
        file.write('''     
            map $http_upgrade $connection_upgrade {
                            default upgrade;
                            '' close;
                }
            upstream clipper {
                server 127.0.0.1:82;
            }
            upstream centralserver {
                    server 127.0.0.1:4444;
            }
            upstream namcdn {
                    hash $chn_name consistent;
                server 127.0.0.1:8001 max_fails=0 fail_timeout=1s;
                server 127.0.0.1:8002 max_fails=0 fail_timeout=1s;
                server 127.0.0.1:8003 max_fails=0 fail_timeout=1s;
                server 127.0.0.1:8004 max_fails=0 fail_timeout=1s;
                server 127.0.0.1:8005 max_fails=0 fail_timeout=1s;
                server 127.0.0.1:8006 max_fails=0 fail_timeout=1s;
                server 127.0.0.1:8007 max_fails=0 fail_timeout=1s;
                server 127.0.0.1:8008 max_fails=0 fail_timeout=1s;
                server 127.0.0.1:8009 max_fails=0 fail_timeout=1s;
                server 127.0.0.1:8010 max_fails=0 fail_timeout=1s;
                server 127.0.0.1:8011 max_fails=0 fail_timeout=1s;
                server 127.0.0.1:8012 max_fails=0 fail_timeout=1s;
                server 127.0.0.1:8013 max_fails=0 fail_timeout=1s;
                server 127.0.0.1:8014 max_fails=0 fail_timeout=1s;
                server 127.0.0.1:8015 max_fails=0 fail_timeout=1s;
                server 127.0.0.1:8016 max_fails=0 fail_timeout=1s;
            }
            server {
                    listen 80;
                    listen 443 ssl;
                    server_name  %s;
                    ssl_certificate /etc/letsencrypt/live/%s/fullchain.pem;
                    ssl_certificate_key /etc/letsencrypt/live/%s/privkey.pem;
                    ssl_session_timeout 5m;
                    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
                    ssl_ciphers "HIGH:!aNULL:!MD5 or HIGH:!aNULL:!MD5:!3DES";
                    ssl_prefer_server_ciphers on;
                    charset utf-8;
                    #access_log  /dev/shm/1v1.access.log  main;
                access_log off;
                
                proxy_next_upstream off;

                location /clipper/ {
                    proxy_set_header Host $http_host;
                            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                            proxy_set_header X-Forwarded-Proto http;
                            proxy_set_header X-Real-IP $remote_addr;
                            proxy_set_header X-Scheme $scheme;
                            proxy_pass http://clipper$uri$is_args$args;
                }
                location ~ idle\/.*\/(?<idle_chn>.*) {
                    set $chn_name $idle_chn;
                    proxy_connect_timeout 1d;
                            proxy_read_timeout 1d;
                            proxy_send_timeout 1d;
                            proxy_http_version 1.1;
                            proxy_buffering off;
                            proxy_set_header Upgrade $http_upgrade;
                            proxy_set_header Connection $connection_upgrade;
                            proxy_pass http://namcdn$request_uri;
                }
                location ~ nbtp\/.*\/(?<idle_chn>.*) {
                            set $chn_name $idle_chn;
                            proxy_connect_timeout 1d;
                            proxy_read_timeout 1d;
                            proxy_send_timeout 1d;
                            proxy_http_version 1.1;
                            proxy_buffering off;
                            proxy_set_header Upgrade $http_upgrade;
                            proxy_set_header Connection $connection_upgrade;
                            proxy_pass http://namcdn$request_uri;
                    }
                location ~ evup\/.*\/(?<idle_chn>.*) {
                            set $chn_name $idle_chn;
                            proxy_connect_timeout 1d;
                            proxy_read_timeout 1d;
                            proxy_send_timeout 1d;
                            proxy_http_version 1.1;
                            proxy_buffering off;
                            proxy_set_header Upgrade $http_upgrade;
                            proxy_set_header Connection $connection_upgrade;
                            proxy_pass http://namcdn$request_uri;
                    }
                location ~ live\/nal\/0\/(?<live_chn>.*) {
                            set $chn_name $live_chn;
                            proxy_pass http://namcdn$request_uri;
                    }
                location ~ live\/g\/(?<live_chn>.*)\/(\d*) {
                    set $chn_name $live_chn;
                            proxy_pass http://namcdn$request_uri;
                    }
                location ~ live\/snap\/(?<snap_chn>.*) {
                            set $chn_name $snap_chn;
                            proxy_pass http://namcdn$request_uri;
                    }
                location ~ snap\/(?<snap_chn>.*)_.*_\d*\.mp4 {
                            set $chn_name $snap_chn;
                            proxy_pass http://namcdn$request_uri;
                    }
                location ~ rec\/hls\/(?<rec_chn>.*)_(\d*)_(\d*)\.m3u8 {
                            set $chn_name $rec_chn;
                            proxy_pass http://namcdn$request_uri;
                    }
                    location ~ rec\/hls\/(?<rec_chn>.*)_(\d*)_(\d*)_h264\.m3u8 {
                            add_header Access-Control-Allow-Origin *;
                    set $chn_name $rec_chn;
                            proxy_pass http://namcdn$request_uri;
                    }
                location ~ rec\/hls\/(.*)(\.)(?<rec_chn>.*)(\.)(.*) {
                    add_header Access-Control-Allow-Origin *;
                    set $chn_name $rec_chn;
                            proxy_pass http://namcdn$request_uri;
                    }
                    location ~ evup\/.*[_][\d]*\/(?<evup_chn>.*)$ {
                    set $chn_name $evup_chn;
                            proxy_connect_timeout 1d;
                            proxy_read_timeout 1d;
                            proxy_send_timeout 1d;
                            proxy_http_version 1.1;
                            proxy_buffering off;
                            proxy_set_header Upgrade $http_upgrade;
                            proxy_set_header Connection $connection_upgrade;
                            proxy_pass http://namcdn$request_uri;
                    }
                location ~ rec\/dts\/(?<rec_chn>.*)(\.)(.*) {
                            #add_header Access-Control-Allow-Origin *;
                            set $chn_name $rec_chn;
                            proxy_pass http://namcdn$request_uri;
                    }
                location ~ users\/proxy\/(?<chn>.*)\/\d*\/.*\/\d* {
                           # add_header Access-Control-Allow-Origin *;
                            set $chn_name $chn;
                            proxy_pass http://namcdn$request_uri;
                    }
                location ~ users\/trigger\/restart\/(?<chn>.*)\/(.*) {
                           # add_header Access-Control-Allow-Origin *;
                            set $chn_name $chn;
                            proxy_pass http://namcdn$request_uri;
                    }
                # Central
                    location /user {
                            proxy_connect_timeout 1d;
                            proxy_read_timeout 1d;
                            proxy_send_timeout 1d;
                            proxy_http_version 1.1;
                            proxy_buffering off;
                            proxy_set_header Upgrade $http_upgrade;
                            proxy_set_header Connection "Upgrade";
                            proxy_set_header X-Forwarded-For $remote_addr;
                            proxy_pass http://centralserver/user;
                    }
                    location /central {
                            proxy_connect_timeout 1d;
                            proxy_read_timeout 1d;
                            proxy_send_timeout 1d;
                            proxy_http_version 1.1;
                            proxy_buffering off;
                            proxy_set_header Upgrade $http_upgrade;
                            proxy_set_header Connection "Upgrade";
                            proxy_set_header X-Forwarded-For $remote_addr;
                            proxy_pass http://centralserver/central;
                    }
                location /speedtest/ {
                    root /home/sysadmin/;
                }
                location / {
                    add_header Content-Type text/plain;
                    #   root   /home/sysadmin/;       
                 return 403;
                }
                }
            ''' %(domain,domain,domain))
        file.close

    if __name__ == '__main__':
        main()
os.system('chown -R sysadmin:sysadmin /home/sysadmin/nginx/')
#call(['bash', 'deamontool.sh'])
os.system('sudo apt install daemontools daemontools-run')
os.system('sudo systemctl enable daemontools.service')
os.system('sudo systemctl start daemontools.service')

class service():
    for m in range(8001, 8016):
        def createFolder(directory):
            try:
                if not os.path.exists(directory):
                    os.makedirs(directory)
            except OSError:
                print ('Error: Creating directory. ' +  directory)

        # Create folder sites

        createFolder('/etc/service/namcdn%d' % m)
        file = open('/etc/service/namcdn%d/run' % m,"w+")
        file.write('''
#!/bin/sh
exec 2>&1
            exec setuidgid namnd node --stack-size=16000 /home/namnd/namcdn/obfuscate/app.js --config=local%d.json
                    ''' %(m))
        file.close
        os.system('chmod +x /etc/service/namcdn%d/run' % m)
        createFolder('/etc/service/central')
        file = open('/etc/service/central/run', "w+")
        file.write('''
#!/bin/bash
exec setuidgid sysadmin node /home/sysadmin/cms3.0_CentralServer/nodejs/central_server.js
                    ''')
        os.system('sudo svc -d /etc/service/*')
        os.system('sudo svc -u /etc/service/*')
        os.system('sudo svc -t /etc/service/*')
#        os.system('sudo svstat /etc/service/*')
#        os.system('su - namnd')
#        os.system('cd /home/namnd/namcdn/config')
        createFolder('/home/namnd/namcdn/config')
        file = open('/home/namnd/namcdn/config/local%d.json' % m,"w+")
        file.write('''
{
  "central_server":"$domain:443",
  "http_port":%d,
  "priv_key": "-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQDmPd1GH/rh+jW1+jArPhbtBsCe6J1d70+yJyNVdw3OOE1JDtxm\nRWAXLn6+qW3DLDbDplGG5A/zSCMwV8Q4iIfRGs5RAxx2NRpnV3HDhOeO8+mHYRP1\nllKqVcoO+81KhgSmZmrcd4lXPAwU/GJwx/AspHkU6S34U9+nZgsXTunr3QIDAQAB\nAoGAbrpF1lm+8DrC5feifslngSqELGg2dlyG+Wi1J38QFqMhGAebm1u18LAdqFgX\nP4vd8o3kG3lG6ntA4Rj0dzPCDLa6vHMz6EgIP2l+MCgTW3Ur5a3cBLtjXkhkzYuv\nMfyWOGnQJ6kCgmqav//dDwwGIOv+Ti0JZtta1FCLTETPSoECQQD5e395G+LoF3+Y\nDVVTP0v8++jMHCTzE/1/iVS86YPWQg8e6UIDtoaSyL4UvfqZuODTaPGWR5w0Gq6G\n1ugiXEqRAkEA7EGv4W2hUgr7vzeESNvPTFDFJhWSCRT6SyQKNtveHPixoL/8uSux\nxV+E43mmRbI+l61FfeL/gcra/JwgnjA6jQJABnPSPTCicrxA2Y7muQt3DKj7QWQs\n9Hh84vKLVYN4nG8C8xq3UV9EJcG5YNH1DErCzdT2ApwBhzt1bhla0aCvcQJBAL1b\nPIuSobyvHu04oub+flytVAZdPYnX7XAyN5mWiaRw03WCyxzi333RPCJSCylLXo2V\nC+CFAsLVgsT6oc4H27UCQF+OIFOGpeOko5lTPkrAUXitP7y+kL0wnvTme66fL+Qo\nhmvsPI2TwVrYSAP8gON1hfUI69nCIUgbmWjnTgHz5+c=\n-----END RSA PRIVATE KEY-----"
}
            ''' % m)
        file.close
        os.system('chown -R namnd:namnd /home/namnd/namcdn/config/local%d.json' % m)
        os.system('sudo svc -u /etc/service/namcdn80*')

os.system('wget https://firmware.vp9.vn/release/relay_server/central.tar.gz -O /home/sysadmin/central.tar.gz')
os.system('tar -xzvf /home/sysadmin/central.tar.gz -C /home/sysadmin/')
os.system('chown -R sysadmin:sysadmin /home/sysadmin/cms3.0_CentralServer/')
os.system('sudo svc -u /etc/service/central/')


print "congratulations installation successfully completed"








