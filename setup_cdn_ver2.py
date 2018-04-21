import os
import sys
import wget
import tarfile
import subprocess
import os.path
from subprocess import call
from shutil import copyfile


class enviroment():
    def main():
        os.system('sudo adduser namnd')
        os.system('sudo ufw allow 443')
        os.system('wget https://sys.vp9.vn/api/agent/cam9.py -O /home/sysadmin/cam9.py')
        file = open("/home/sysadmin/sys.sh", "w")
        file.write('''
#!/bin/bash
tmux new-session -s sys -n "Agent" -d
tmux send-keys -t sys "python /home/sysadmin/cam9.py" C-m
            ''')
        file.close
        os.system('chmod +x /home/sysadmin/sys.sh')
        with open("/etc/rc.local", 'r+') as fd:
            contents = fd.readlines()
            contents.insert(12, "sudo -u sysadmin /home/sysadmin/sys.sh") 
            fd.seek(12)
            fd.writelines(contents)

#        with open("/etc/ufw/user.rules", "r+") as file:
#            line_fw = any("-A ufw-user-input -p tcp --dport 443 -j ACCEPT" in line for line in file)
#            if not line_fw:
#                file.seek(0, os.SEEK_END)
#                file.write("-A ufw-user-input -p tcp --dport 443 -j ACCEPT\n")
#                file.close
        with open("/etc/sudoers", "r+") as file:
            line_sudoers = any('''
# See sudoers(5) for more information on "#include" directives:
%namnd ALL=(ALL:ALL) NOPASSWD:ALL
%sysadmin ALL=(ALL:ALL) NOPASSWD:ALL
                ''' in line for line in file)
            if not line_sudoers:
                file.seek(0, os.SEEK_END)
                file.write('''
# See sudoers(5) for more information on "#include" directives:
%namnd ALL=(ALL:ALL) NOPASSWD:ALL
%sysadmin ALL=(ALL:ALL) NOPASSWD:ALL\n
                    ''')
                file.close
    if __name__ == '__main__':
            main()

class nginx():
    def main():
        print('Beginning file download source.list')

        url = 'https://firmware.vp9.vn/release/relay_server/source.list'  
        wget.download(url, '/home/sysadmin/source.list')
        copyfile('/home/sysadmin/source.list', '/etc/apt/source.list')
        os.system('sudo apt update')
        os.system('chmod +x nginx.sh')
        call(['bash', 'nginx.sh'])

    if __name__ == '__main__':
        main()


while ("1"=="1"):
    domain = raw_input("Enter a domain here: ")
    if ("." in str(domain)):
        if ("." in domain[0]):
            print "Dau . dau tien, nhap lai"
            continue
        if ("." in domain[len(domain)-1]):
            print "Dau cham o cuoi, nhap lai"
            continue
#        if not ("conf" in domain):
#            print "nhap sai dinh dang, thieu .conf o cuoi, nhap lai"
#            continue
        break
    else:
        continue

class ssl():
    def main():
        print("Beginning file download letsencrypt")
        os.system('wget https://firmware.vp9.vn/release/relay_server/certbot-auto -O /home/sysadmin/certbot-auto')
        os.system('chmod a+x /home/sysadmin/certbot-auto')
        os.system('chown -R sysadmin:sysadmin certbot-auto')
        os.system('/home/sysadmin/certbot-auto certonly --standalone -d %s' % domain)

#        url = 'https://firmware.vp9.vn/release/relay_server/certbot-auto'
#        wget.download(url, '/home/sysadmin/certbot-auto')
#        os.system('chown -R sysadmin:sysadmin certbot-auto')
#        os.system('/home/sysadmin/certbot-auto certonly --standalone -d %s' % domain)

    if __name__ == '__main__':
        main()


class config():

    def createFolder(directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print ('Error: Creating directory. ' +  directory)
            
    # Create folder sites
    createFolder('/home/sysadmin/nginx/conf/sites')

    def main():
        print("Config nginx.conf")

        url = 'https://firmware.vp9.vn/release/relay_server/nginx.conf'
        wget.download(url, '/home/sysadmin/nginx/nginx.conf')

        print("Config domain sites")
        url = 'https://firmware.vp9.vn/release/relay_server/domain.conf'
        wget.download(url, '/home/sysadmin/nginx/conf/sites/%s.conf' % domain)

        with open("/home/sysadmin/nginx/conf/sites/%s.conf" % domain,"r+") as file:
            filedata = file.read()
            filedata = filedata.replace('domain', '%s' % domain)
        with open("/home/sysadmin/nginx/conf/sites/%s.conf" % domain, "w") as file:
            file.write(filedata)

    if __name__ == '__main__':
        main()

class nodejs():
    def main():
        print("Beginning file download nodejs")
        os.system('curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -')
        os.system('sudo aptitude install nodejs')
        os.system('curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"')
        os.system('sudo python get-pip.py')
        os.system('sudo pip install requests==2.13.0')
        # install deamontool
        os.system('chown -R sysadmin:sysadmin /home/sysadmin/nginx/')
        os.system('sudo apt install daemontools daemontools-run')
        os.system('sudo systemctl enable daemontools.service')
        os.system('sudo systemctl start daemontools.service')
#        os.system('sudo apt-get install python-software-properties')
#        os.system('sudo add-apt-repository -y -r ppa:chris-lea/node.js')
#        os.system('sudo curl --silent https://deb.nodesource.com/gpgkey/nodesource.gpg.key | sudo apt-key add -')
#        os.system('VERSION=node_7.x')
#        os.system('DISTRO="$(lsb_release -s -c)"')
#        os.system('sudo echo "deb https://deb.nodesource.com/$VERSION $DISTRO main" | sudo tee /etc/apt/sources.list.d/nodesource.list')
#        os.system('sudo echo "deb-src https://deb.nodesource.com/$VERSION $DISTRO main" | sudo tee -a /etc/apt/sources.list.d/nodesource.list')
#        os.system('sudo apt-get update')
#        os.system('sudo apt-get install nodejs')
#        os.system('sudo npm install -g npm')
#        os.system('sudo npm install -g n')
#        os.system('sudo n stable')

    if __name__ == '__main__':
        main()

class service():
    for m in range(8001, 8017):
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
    print("Beginning file download namcdn")
#        url = 'https://firmware.vp9.vn/release/relay_server/namcdn/namcdn-20180412.tar.gz'
#        wget.download(url, '/home/namnd/namcdn/namcdn-20180412.tar.gz')
    os.system('wget https://firmware.vp9.vn/release/relay_server/namcdn/namcdn-20180412.tar.gz -O /home/namnd/namcdn/namcdn-20180412.tar.gz')
    os.system('tar -xzvf /home/namnd/namcdn/namcdn-20180412.tar.gz -C /home/namnd/namcdn/')
    os.system('chown -R namnd:namnd /home/namnd/namcdn')
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
  "central_server":"%s:443",
  "http_port":%d,
  "priv_key": "-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQDmPd1GH/rh+jW1+jArPhbtBsCe6J1d70+yJyNVdw3OOE1JDtxm\nRWAXLn6+qW3DLDbDplGG5A/zSCMwV8Q4iIfRGs5RAxx2NRpnV3HDhOeO8+mHYRP1\nllKqVcoO+81KhgSmZmrcd4lXPAwU/GJwx/AspHkU6S34U9+nZgsXTunr3QIDAQAB\nAoGAbrpF1lm+8DrC5feifslngSqELGg2dlyG+Wi1J38QFqMhGAebm1u18LAdqFgX\nP4vd8o3kG3lG6ntA4Rj0dzPCDLa6vHMz6EgIP2l+MCgTW3Ur5a3cBLtjXkhkzYuv\nMfyWOGnQJ6kCgmqav//dDwwGIOv+Ti0JZtta1FCLTETPSoECQQD5e395G+LoF3+Y\nDVVTP0v8++jMHCTzE/1/iVS86YPWQg8e6UIDtoaSyL4UvfqZuODTaPGWR5w0Gq6G\n1ugiXEqRAkEA7EGv4W2hUgr7vzeESNvPTFDFJhWSCRT6SyQKNtveHPixoL/8uSux\nxV+E43mmRbI+l61FfeL/gcra/JwgnjA6jQJABnPSPTCicrxA2Y7muQt3DKj7QWQs\n9Hh84vKLVYN4nG8C8xq3UV9EJcG5YNH1DErCzdT2ApwBhzt1bhla0aCvcQJBAL1b\nPIuSobyvHu04oub+flytVAZdPYnX7XAyN5mWiaRw03WCyxzi333RPCJSCylLXo2V\nC+CFAsLVgsT6oc4H27UCQF+OIFOGpeOko5lTPkrAUXitP7y+kL0wnvTme66fL+Qo\nhmvsPI2TwVrYSAP8gON1hfUI69nCIUgbmWjnTgHz5+c=\n-----END RSA PRIVATE KEY-----"
}
            ''' % (domain,m))
    file.close
    os.system('chown -R namnd:namnd /home/namnd/namcdn/config/local%d.json' % m)
    os.system('sudo svc -u /etc/service/namcdn80*')

#        os.system('wget https://firmware.vp9.vn/release/relay_server/central.tar.gz -O /home/sysadmin/central.tar.gz')
    url = 'https://firmware.vp9.vn/release/relay_server/central.tar.gz'
    wget.download(url, '/home/sysadmin/central.tar.gz')
    os.system('tar -xzvf /home/sysadmin/central.tar.gz -C /home/sysadmin/')
    os.system('chown -R sysadmin:sysadmin /home/sysadmin/cms3.0_CentralServer/')
    os.system('sudo svc -u /etc/service/central/')
    os.system('chown -R namnd:namnd /home/namnd/namcdn/')


print "congratulations installation successfully completed"