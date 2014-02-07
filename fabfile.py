from fabric.api import *

# the user to use for the remote commands
env.user = 'root'
# the servers where the commands are executed
# env.hosts = ['192.241.196.189']

#aliyun
# env.hosts = ['115.29.187.10']

#rms
env.hosts = ['biubiubiu.me']

def start():
    with cd('server-hearthstone'):
        run("bash kill.sh")
        run('./manage.py server --port 30010', pty=False, shell_escape=False)

def db():
    #clear remote db
    run('mongo hearthstone --eval "db.dropDatabase()"')
    
    # Migrate db file.
    local('mongodump --out /tmp/db && tar -cvf /tmp/db.tar /tmp/db')
    put('/tmp/db.tar', '/tmp/db.tar')
    with cd('/tmp'):
        run('tar -xvf /tmp/db.tar')
        run('mongorestore /tmp/tmp/db/hearthstone/ -d hearthstone')
        
