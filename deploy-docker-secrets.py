#!/usr/bin/env python

# 1. Host에서 이미지 build, push
# 2. EC2에서 이미지 pull, run(bash)
# 3. Host -> EC2 -> Container로 secrets.json전송
# 4. Container runserver

import os
import subprocess
from pathlib import Path

DOCKER_IMAGE_TAG = 'moonpeter/wps_dabangapi'
DOCKER_OPTIONS = [
    ('--rm', ''),
    ('-it', ''),
    # background로 실행하는 옵션 추가
    ('-d', ''),
    ('-p', '80:80'),
    ('-p', '443:443'),
    ('--name', 'wps_dabangapi'),

    # Let's Encrypt volume
    ('-v', '/etc/letsencrypt:/etc/letsencrypt'),
]

USER = 'ubuntu'
HOST = '15.164.165.28'
TARGET = f'{USER}@{HOST}'
HOME = str(Path.home())
IDENTITY_FILE = os.path.join(HOME, '.ssh', 'wps12th.pem')
SOURCE = os.path.join(HOME, 'projects', 'wps12', 'WPS_DabangAPI')
SECRETS_FILE = os.path.join(SOURCE, 'secrets.json')


def run(cmd, ignore_error=False):
    process = subprocess.run(cmd, shell=True)
    if not ignore_error:
        process.check_returncode()


def ssh_run(cmd, ignore_error=False):
    run(f"ssh -o StrictHostKeyChecking=no -i {IDENTITY_FILE} {TARGET} -C {cmd}", ignore_error=ignore_error)


# 1. 호스트에서 도커 이미지 build, push
def local_build_push():
    run(f'poetry export -f requirements.txt > requirements.txt')
    run(f'docker build -t {DOCKER_IMAGE_TAG} .')
    run(f'docker push {DOCKER_IMAGE_TAG}')
    print('1111111111111111')


# 서버 초기설정
def server_init():
    ssh_run(f'sudo apt update')
    ssh_run(f'sudo DEBIAN_FRONTEND=noninteractive apt dist-upgrade -y')
    ssh_run(f'sudo apt -y install docker.io')
    print('111111111111---22222222222')


# 2. 실행중인 컨테이너 종료, pull, run
def server_pull_run():
    ssh_run(f'sudo docker stop wps_dabangapi', ignore_error=True)
    ssh_run(f'sudo docker pull {DOCKER_IMAGE_TAG}')
    ssh_run('sudo docker run {options} {tag} /bin/bash'.format(
        options=' '.join([
            f'{key} {value}' for key, value in DOCKER_OPTIONS
        ]),
        tag=DOCKER_IMAGE_TAG,
    ))
    print('22222222222222')


# 3. Host에서 EC2로 secrets.json을 전송, EC2에서 Container로 다시 전송
def copy_secrets():
    run(f'scp -i {IDENTITY_FILE} {SECRETS_FILE} {TARGET}:/tmp', ignore_error=True)
    ssh_run(f'sudo docker cp /tmp/secrets.json wps_dabangapi:/srv/WPS_DabangAPI')
    print('333333333333333')


# 4. Container에서 collectstatic, supervior실행
def sever_cmd():
    ssh_run(f'sudo docker exec wps_dabangapi nginx')
    ssh_run(f'sudo docker exec wps_dabangapi /usr/sbin/nginx -s stop', ignore_error=True)
    ssh_run(f'sudo docker exec wps_dabangapi python3 manage.py collectstatic --noinput')
    ssh_run(f'sudo docker exec -it -d wps_dabangapi '
            f'supervisord -c /srv/WPS_DabangAPI/.config/supervisord.conf -n')
    print('44444444444444444444444')


if __name__ == '__main__':
    try:
        local_build_push()
        server_init()
        server_pull_run()
        copy_secrets()
        sever_cmd()
    except subprocess.CalledProcessError as e:
        print('deploy-docker-secrets Error!')
        print(' cmd:', e.cmd)
        print(' returncode:', e.returncode)
        print(' output:', e.output)
        print(' stdout:', e.stdout)
        print(' stderr:', e.stderr)
