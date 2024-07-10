From python:latest
workdir /app
add ./myspider /app
add ./scrapy.cfg /app
run cd /app
run pip install -r myspider/requirements.txt


ENTRYPOINT ['python', '/app/myspider/start.py']