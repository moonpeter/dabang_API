daemon = False
chdir = '/srv/WPS_DabangAPI/app'
bind = 'unix:/run/WPS_DabangAPI.sock'
accesslog = '/var/log/gunicorn/WPS_DabangAPI-access.log'
errorlog = '/var/log/gunicorn/WPS_DabangAPI-error.log'
capture_output = True