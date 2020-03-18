FROM        python:3.7-slim

RUN         apt -y update && apt -y dist-upgrade && apt -y autoremove
RUN         apt -y install nginx

# poetry export로 생성된 requirements.txt를 적절히 복사
COPY        ./requirements.txt /tmp/
RUN         pip install -r /tmp/requirements.txt

# 소스코드 복사
COPY        . /srv/WPS_DabangAPI
WORKDIR     /srv/WPS_DabangAPI/app

# Nginx 설정파일을 복사, 기본 서버 설정 삭제
RUN         rm /etc/nginx/sites-enabled/default
RUN         cp /srv/WPS_DabangAPI/.config/dabangapi.nginx /etc/nginx/sites-enabled/

# 로그폴더 생성
RUN         mkdir /var/log/gunicorn

CMD         /bin/bash