## 트윗 크롤러
----------------
#### 실행환경
- OS : ubuntu 16.04(AWS EC2 )
- DB : MongoDB 
- Python 3.6(VirtualEvn) 
- Redis

#### Python, VirtualEnv 설치
root 계정으로 pip3와 virtualenv를 설치합니다.
```
$ sudo apt-get update
$ sudo apt-get install python3-pip python3-dev
$ sudo pip3 install virtualenv
```
계정을 생성하고 virtual environment를 생성합니다.

```
$ adduser {userid}
$ su -l {userid}
$ mkdir ~/{myproject}
$ cd ~/{myproject}
$ virtualenv {myprojectenv}
```
그러면 Python의 로컬 사본과 pip 가 프로젝트 디렉토리의 myprojectenv 디렉토리에 설치됩니다.

```
$ source {myprojectenv}/bin/activate
```
가상 환경에서 현재 작동 중임을 나타내는 프롬프트가 변경됩니다.

```
ex : (appenv) ssum@DISCOUNT-API-SVR:~/app$
```

#### Python lib install
python lib
```(.bash)
$ . bin/activate
$ pip install -r requirement.txt
```
Redis Check (port : 6379 open check)
```(.bash)
$ redis-cli
$ ping
return > pong
```

#### mongo install in ubuntu16.04 [link](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-mongodb-on-ubuntu-16-04)
```(.bash)
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
$ echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
$ sudo apt-get update
$ sudo apt-get install -y mongodb-org
$ sudo systemctl start mongod
$ sudo systemctl status mongodb
$ sudo systemctl enable mongodb
$ sudo ufw allow from your_other_server_ip/32 to any port 27017
$ sudo ufw status
```
#### 구동
- Worker
```(.bash)
$ celery -A twitt_crawl_worker worker -Q twitt_push --loglevel=INFO >> outFilePath 2>&1 &
```
- Task
```(.bash)
$ celery beat -A twitt_crawl_worker >> outFilePath 2>&1 &
```