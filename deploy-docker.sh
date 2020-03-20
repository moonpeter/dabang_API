#!/usr/bin/env sh
IDENTITY_FILE="$HOME/.ssh/wps12th.pem"
USER="ubuntu"
HOST="15.164.165.28"
TARGET=${USER}@${HOST}
ORIGIN_SOURCE="$HOME/projects/wps12/WPS_DabangAPI"
DOCKER_REPO="moonpeter/wps_dabangapi"
SSH_CMD="ssh -i ${IDENTITY_FILE} ${TARGET}"

echo "===== Docker 배포 ====="


# 서버 초기설정
echo " ######## apt update & upgrade & autoremove"
${SSH_CMD} -C 'sudo apt update && sudo DEBIAN_FRONTEND=noninteractiv apt dist-upgrade -y && apt -y autoremove'
echo " ######## apt install docker.io"
${SSH_CMD} -C 'sudo apt -y install docker.io'


echo " ######## poetry export"
poetry export -f requirements.txt > requirements.txt

# docker build
echo " ######## docker build"
docker build -q -t ${DOCKER_REPO} -f Dockerfile "${ORIGIN_SOURCE}"

# docker push
echo " ######## docker push"
docker push ${DOCKER_REPO}

echo " ######## docker stop"
${SSH_CMD} -C "sudo docker stop wps_dabangapi"

echo " ######## docker pull"
${SSH_CMD} -C "sudo docker pull ${DOCKER_REPO}"



echo "######## screen settings"
# 실행중이던 screen 세션 종료
${SSH_CMD} -C 'screen -X -S docker quit'
# screen 실행
${SSH_CMD} -C 'screen -S docker -d -m'
# 실행중인 세션에 명령어 전달
${SSH_CMD} -C "screen -R docker -X stuff 'sudo docker run --rm -it -p 80:8000 --name=wps_dabangapi moonpeter/wps_dabangapi /bin/bash\n'"

# container에서 bash를 실행중인 screen에 runserver 명령어를 전달
${SSH_CMD} -C "screen -r docker -X stuff 'python manage.py runserver 0:8000\n'"


echo "===== finish ====="